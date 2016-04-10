# Copyright (C) 2015 University of Nebraska at Omaha
#
# This file is part of dosocs2.
#
# dosocs2 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# dosocs2 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with dosocs2.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-2.0+

import os

from sqlalchemy.sql import select, and_

from . import queries
from . import schema as db
from . import util


def insert(conn, table, params):
    query = table.insert().values(**params)
    result = conn.execute(query)
    [pkey] = result.inserted_primary_key
    return pkey


def bulk_insert(conn, table, rows_list):
    if rows_list:
        conn.execute(table.insert(), *rows_list)


def lookup_by_sha1(conn, table, sha1):
    '''Lookup row by SHA-1 sum and return the row, or None.'''
    # Freak occurence of sha1 collision probably won't happen.
    # But if it does, this will fail with 'too many values to unpack'
    # (although, you will have bigger problems then...)
    query = (
        select([table])
        .where(table.c.sha1 == sha1)
        )
    [result] = conn.execute(query).fetchall() or [None]
    if result is None:
        return result
    else:
        return dict(**result)


def register_file(conn, path, known_sha1=None):
    sha1 = known_sha1 or util.sha1(path)
    file = lookup_by_sha1(conn, db.files, sha1)
    if file is not None:
        return file
    file_type_query = (
        select([db.file_types.c.file_type_id])
        .where(db.file_types.c.name == util.spdx_filetype(path))
        )
    file_type_id = conn.execute(file_type_query).fetchone()['file_type_id']
    file = {
        'sha1': sha1,
        'file_type_id': file_type_id,
        'copyright_text': None,
        'project_id': None,
        'comment': '',
        'notice': ''
        }
    file['file_id'] = insert(conn, db.files, file)
    return file


def get_cached_dir_pkg(conn, dir_code, ver_code):
    found_pkg_query = (
        select([db.packages])
        .where(
            and_(
                db.packages.c.dosocs2_dir_code == dir_code,
                db.packages.c.verification_code == ver_code
                )
            )
        )
    [found_pkg] = conn.execute(found_pkg_query).fetchall() or [None]
    if found_pkg is not None:
        return found_pkg


def register_package(conn, package_root, name=None, version=None, comment=None,
                     package_file_path=None):
    # Attempt to get cached package row
    if package_file_path is not None:
        # "True package" may be cached by SHA-1 of entire package
        sha1 = util.sha1(package_file_path)
        package = lookup_by_sha1(conn, db.packages, sha1)
        if package is not None:
            return package
    ver_code, hashes, dir_code = util.get_dir_hashes(package_root)
    if package_file_path is None:
        found_pkg = get_cached_dir_pkg(conn, dir_code, ver_code)
        if found_pkg is not None:
            return found_pkg
        sha1 = None
    # Create package row
    basename = os.path.basename(os.path.abspath(package_file_path or package_root))
    package = {
        'file_name': basename,
        'version': version or '',
        'supplier_id': None,
        'originator_id': None,
        'download_location': None,
        'verification_code': ver_code,
        'ver_code_excluded_file_id': None,
        'sha1': sha1, # None is permitted here
        'home_page': None,
        'source_info': '',
        'concluded_license_id': None,
        'declared_license_id': None,
        'license_comment': '',
        'copyright_text': None,
        'summary': '',
        'description': '',
        'comment': comment or '',
        'dosocs2_dir_code': None if sha1 is not None else dir_code
        }
    if package_file_path is None:
        package['name'] = name or basename
    else:
        package['name'] = name or util.package_friendly_name(os.path.basename(package_file_path))
    package['package_id'] = insert(conn, db.packages, package)
    # Create packages_files rows
    row_params = []
    for (file_path, file_sha1) in hashes.iteritems():
        fileobj = register_file(conn, file_path, known_sha1=file_sha1)
        package_file_params = {
            'package_id': package['package_id'],
            'file_id': fileobj['file_id'],
            'concluded_license_id': None,
            'file_name': util.abs_to_rel(package_root, file_path),
            'license_comment': ''
            }
        row_params.append(package_file_params)
    bulk_insert(conn, db.packages_files, row_params)
    return package


def create_document_namespace(conn, prefix, doc_name):
    suffix = util.friendly_namespace_suffix(doc_name)
    uri = prefix + suffix
    doc_namespace = {'uri': uri}
    doc_namespace['document_namespace_id'] = insert(conn, db.document_namespaces, doc_namespace)
    return doc_namespace


def create_all_identifiers(conn, doc_namespace_id, package):
    all_files_query = (
        select([
            db.packages_files.c.package_file_id,
            db.packages_files.c.file_name,
            db.files.c.sha1
            ])
        .select_from(
            db.packages_files
            .join(db.files, db.packages_files.c.file_id == db.files.c.file_id)
            )
        .where(db.packages_files.c.package_id == package['package_id'])
        )
    package_id_params = {
        'document_namespace_id': doc_namespace_id,
        'package_id': package['package_id'],
        'id_string': util.gen_id_string('package', package['file_name'], package['verification_code'])
        }
    rows_list = []
    for file in conn.execute(all_files_query):
        file_id_params = {
            'document_namespace_id': doc_namespace_id,
            'package_file_id': file['package_file_id'],
            'id_string': util.gen_id_string('file', file['file_name'], file['sha1'])
            }
        rows_list.append(file_id_params)
    bulk_insert(conn, db.identifiers, rows_list)
    insert(conn, db.identifiers, package_id_params)


def autocreate_relationships(conn, docid):
    qs = (
        queries.auto_contains(docid),
        queries.auto_contained_by(docid),
        queries.auto_describes(docid),
        queries.auto_described_by(docid)
        )
    for q in qs:
        row_params = []
        for row in conn.execute(q):
            kwargs = {
                'left_identifier_id': row['left_identifier_id'],
                'relationship_type_id': row['relationship_type_id'],
                'right_identifier_id': row['right_identifier_id'],
                'relationship_comment': ''
                }
            row_params.append(kwargs)
        bulk_insert(conn, db.relationships, row_params)

def persistDependencyHierarchy(conn):
    edges=[('org.hibernate:hibernate-core:jar:4.3.7.Final:compile', 'antlr:antlr:jar:2.7.7:compile'), ('org.hibernate:hibernate-core:jar:4.3.7.Final:compile', 'org.jboss:jandex:jar:1.1.0.Final:compile'), ('org.hibernate:hibernate-entitymanager:jar:4.3.7.Final:compile', 'org.jboss.logging:jboss-logging-annotations:jar:1.2.0.Beta1:compile'), ('org.hibernate:hibernate-entitymanager:jar:4.3.7.Final:compile', 'org.jboss.spec.javax.transaction:jboss-transaction-api_1.2_spec:jar:1.0.0.Final:compile'), ('org.hibernate:hibernate-entitymanager:jar:4.3.7.Final:compile', 'org.hibernate:hibernate-core:jar:4.3.7.Final:compile'), ('org.hibernate:hibernate-entitymanager:jar:4.3.7.Final:compile', 'org.hibernate.javax.persistence:hibernate-jpa-2.1-api:jar:1.0.0.Final:compile'), ('org.hibernate:hibernate-entitymanager:jar:4.3.7.Final:compile', 'org.jboss.logging:jboss-logging:jar:3.1.3.GA:compile'), ('org.hibernate:hibernate-entitymanager:jar:4.3.7.Final:compile', 'org.hibernate.common:hibernate-commons-annotations:jar:4.0.5.Final:compile'), ('org.hibernate:hibernate-entitymanager:jar:4.3.7.Final:compile', 'dom4j:dom4j:jar:1.6.1:compile'), ('org.springframework.data:spring-data-mongodb:jar:1.6.1.RELEASE:compile', 'org.mongodb:mongo-java-driver:jar:2.12.4:compile'), ('org.codehaus.jackson:jackson-mapper-asl:jar:1.9.13:compile', 'org.codehaus.jackson:jackson-core-asl:jar:1.9.13:compile'), ('dom4j:dom4j:jar:1.6.1:compile', 'xml-apis:xml-apis:jar:1.0.b2:compile'), ('com.zaxxer:HikariCP:jar:2.2.5:compile', 'org.javassist:javassist:jar:3.18.1-GA:compile'), ('org.hibernate:hibernate-validator:jar:5.1.3.Final:compile', 'javax.validation:validation-api:jar:1.1.0.Final:compile'), ('org.hibernate:hibernate-validator:jar:5.1.3.Final:compile', 'com.fasterxml:classmate:jar:1.0.0:compile'), ('org.springframework.data:spring-data-jpa:jar:1.7.1.RELEASE:compile', 'org.slf4j:jcl-over-slf4j:jar:1.7.8:runtime'), ('org.springframework.data:spring-data-jpa:jar:1.7.1.RELEASE:compile', 'org.aspectj:aspectjrt:jar:1.8.4:compile'), ('org.springframework.data:spring-data-jpa:jar:1.7.1.RELEASE:compile', 'org.springframework.data:spring-data-commons:jar:1.9.1.RELEASE:compile'), ('com.springMvcMongodb:SpringMVCmongoDBTest:war:0.0.1-SNAPSHOT', 'org.hamcrest:hamcrest-library:jar:1.3:test'), ('com.springMvcMongodb:SpringMVCmongoDBTest:war:0.0.1-SNAPSHOT', 'org.springframework.data:spring-data-mongodb:jar:1.6.1.RELEASE:compile'), ('com.springMvcMongodb:SpringMVCmongoDBTest:war:0.0.1-SNAPSHOT', 'org.codehaus.jackson:jackson-mapper-asl:jar:1.9.13:compile'), ('com.springMvcMongodb:SpringMVCmongoDBTest:war:0.0.1-SNAPSHOT', 'org.springframework.security:spring-security-web:jar:3.2.5.RELEASE:compile'), ('com.springMvcMongodb:SpringMVCmongoDBTest:war:0.0.1-SNAPSHOT', 'com.google.guava:guava:jar:17.0:compile'), ('com.springMvcMongodb:SpringMVCmongoDBTest:war:0.0.1-SNAPSHOT', 'org.slf4j:slf4j-api:jar:1.7.8:compile'), ('com.springMvcMongodb:SpringMVCmongoDBTest:war:0.0.1-SNAPSHOT', 'org.thymeleaf.extras:thymeleaf-extras-springsecurity3:jar:2.1.1.RELEASE:compile'), ('com.springMvcMongodb:SpringMVCmongoDBTest:war:0.0.1-SNAPSHOT', 'org.hibernate:hibernate-entitymanager:jar:4.3.7.Final:compile'), ('com.springMvcMongodb:SpringMVCmongoDBTest:war:0.0.1-SNAPSHOT', 'javax.el:javax.el-api:jar:2.2.5:test'), ('com.springMvcMongodb:SpringMVCmongoDBTest:war:0.0.1-SNAPSHOT', 'com.zaxxer:HikariCP:jar:2.2.5:compile'), ('com.springMvcMongodb:SpringMVCmongoDBTest:war:0.0.1-SNAPSHOT', 'org.hibernate:hibernate-validator:jar:5.1.3.Final:compile'), ('com.springMvcMongodb:SpringMVCmongoDBTest:war:0.0.1-SNAPSHOT', 'org.hsqldb:hsqldb:jar:2.3.2:compile'), ('com.springMvcMongodb:SpringMVCmongoDBTest:war:0.0.1-SNAPSHOT', 'org.springframework.data:spring-data-jpa:jar:1.7.1.RELEASE:compile'), ('com.springMvcMongodb:SpringMVCmongoDBTest:war:0.0.1-SNAPSHOT', 'org.springframework:spring-test:jar:4.1.4.RELEASE:test'), ('com.springMvcMongodb:SpringMVCmongoDBTest:war:0.0.1-SNAPSHOT', 'ch.qos.logback:logback-classic:jar:1.1.2:compile'), ('com.springMvcMongodb:SpringMVCmongoDBTest:war:0.0.1-SNAPSHOT', 'org.springframework:spring-orm:jar:4.1.4.RELEASE:compile'), ('com.springMvcMongodb:SpringMVCmongoDBTest:war:0.0.1-SNAPSHOT', 'javax.inject:javax.inject:jar:1:compile'), ('com.springMvcMongodb:SpringMVCmongoDBTest:war:0.0.1-SNAPSHOT', 'org.assertj:assertj-core:jar:1.5.0:test'), ('com.springMvcMongodb:SpringMVCmongoDBTest:war:0.0.1-SNAPSHOT', 'org.mockito:mockito-core:jar:1.10.8:test'), ('com.springMvcMongodb:SpringMVCmongoDBTest:war:0.0.1-SNAPSHOT', 'org.springframework:spring-webmvc:jar:4.1.4.RELEASE:compile'), ('com.springMvcMongodb:SpringMVCmongoDBTest:war:0.0.1-SNAPSHOT', 'org.springframework.security:spring-security-config:jar:3.2.5.RELEASE:compile'), ('com.springMvcMongodb:SpringMVCmongoDBTest:war:0.0.1-SNAPSHOT', 'javax.servlet:javax.servlet-api:jar:3.0.1:provided'), ('com.springMvcMongodb:SpringMVCmongoDBTest:war:0.0.1-SNAPSHOT', 'org.objenesis:objenesis:jar:2.1:test'), ('com.springMvcMongodb:SpringMVCmongoDBTest:war:0.0.1-SNAPSHOT', 'org.thymeleaf:thymeleaf-spring4:jar:2.1.4.RELEASE:compile'), ('com.springMvcMongodb:SpringMVCmongoDBTest:war:0.0.1-SNAPSHOT', 'junit:junit:jar:4.11:test'), ('com.springMvcMongodb:SpringMVCmongoDBTest:war:0.0.1-SNAPSHOT', 'org.hamcrest:hamcrest-core:jar:1.3:test'), ('org.thymeleaf:thymeleaf:jar:2.1.4.RELEASE:compile', 'org.unbescape:unbescape:jar:1.1.0.RELEASE:compile'), ('org.thymeleaf:thymeleaf:jar:2.1.4.RELEASE:compile', 'ognl:ognl:jar:3.0.8:compile'), ('ch.qos.logback:logback-classic:jar:1.1.2:compile', 'ch.qos.logback:logback-core:jar:1.1.2:compile'), ('org.springframework:spring-orm:jar:4.1.4.RELEASE:compile', 'org.springframework:spring-tx:jar:4.1.4.RELEASE:compile'), ('org.springframework:spring-orm:jar:4.1.4.RELEASE:compile', 'org.springframework:spring-jdbc:jar:4.1.4.RELEASE:compile'), ('org.springframework:spring-webmvc:jar:4.1.4.RELEASE:compile', 'org.springframework:spring-beans:jar:4.1.4.RELEASE:compile'), ('org.springframework:spring-webmvc:jar:4.1.4.RELEASE:compile', 'org.springframework:spring-core:jar:4.1.4.RELEASE:compile'), ('org.springframework:spring-webmvc:jar:4.1.4.RELEASE:compile', 'org.springframework:spring-context:jar:4.1.4.RELEASE:compile'), ('org.springframework:spring-webmvc:jar:4.1.4.RELEASE:compile', 'org.springframework:spring-web:jar:4.1.4.RELEASE:compile'), ('org.springframework:spring-webmvc:jar:4.1.4.RELEASE:compile', 'org.springframework:spring-expression:jar:4.1.4.RELEASE:compile'), ('org.springframework.security:spring-security-config:jar:3.2.5.RELEASE:compile', 'aopalliance:aopalliance:jar:1.0:compile'), ('org.springframework.security:spring-security-config:jar:3.2.5.RELEASE:compile', 'org.springframework:spring-aop:jar:4.1.4.RELEASE:compile'), ('org.springframework.security:spring-security-config:jar:3.2.5.RELEASE:compile', 'org.springframework.security:spring-security-core:jar:3.2.5.RELEASE:compile'), ('org.thymeleaf:thymeleaf-spring4:jar:2.1.4.RELEASE:compile', 'org.thymeleaf:thymeleaf:jar:2.1.4.RELEASE:compile')]
    row_params=[]
#         print(render.get_row(conn,queries.getPackageIdentifierByName("openssl-1.0.1r.tar.gz"))['left_identifier_id'])
    for edge in edges:
        (leftnode,rightnode)=edge
        splitLeftNodeName=leftnode.split(':')
        left_package_name=splitLeftNodeName[1]+'-'+splitLeftNodeName[3]+'-sources.jar'
        splitRightNodeName=rightnode.split(':')
        right_package_name=splitRightNodeName[1]+'-'+splitRightNodeName[3]+'-sources.jar'
#         print left_package_name
#         print right_package_name
        try:
            leftIdent=conn.execute(queries.getPackageIdentifierByName(left_package_name)).fetchone()
#             leftIdent=render.get_row(conn,queries.getPackageIdentifierByName(left_package_name))['left_identifier_id']
#             print 'left package name succeded'
#             print queries.getPackageIdentifierByName(right_package_name)
            rightIdent=conn.execute(queries.getPackageIdentifierByName(right_package_name)).fetchone()
            if leftIdent==None or rightIdent==None:
                print leftIdent,rightIdent
                print left_package_name,right_package_name
                print 'either the left or right identifier does not exist'
                continue
#             rightIdent=render.get_row(conn,queries.getPackageIdentifierByName(right_package_name))['left_identifier_id']
            print leftIdent,rightIdent
        except ValueError:
            print 'falure get identifier for the following edge'
            print left_package_name, right_package_name 
            continue
        kwargs = {
            'left_identifier_id': leftIdent[0],
            'relationship_type_id': 29,
            'right_identifier_id': rightIdent[0],
            'relationship_comment': ''
            }
        print 'will persist'
        print left_package_name,right_package_name
        print kwargs
        row_params.append(kwargs)
    bulk_insert(conn, db.relationships, row_params)

def create_document(conn, prefix, package, name=None, comment=None):
    data_license_query = (
        select([db.licenses.c.license_id])
        .where(db.licenses.c.short_name == 'CC0-1.0')
        )
    data_license_id = conn.execute(data_license_query).fetchone()['license_id']
    doc_name = name or package['name']
    doc_namespace_id = create_document_namespace(conn, prefix, doc_name)['document_namespace_id']
    new_document = {
        'data_license_id': data_license_id,
        'spdx_version': 'SPDX-2.0',
        'name': doc_name,
        'document_namespace_id': doc_namespace_id,
        'license_list_version': '2.2',
        'creator_comment': name or '',
        'document_comment': comment or '',
        'package_id': package['package_id']
        }
    new_document_id = insert(conn, db.documents, new_document)
    new_document['document_id'] = new_document_id
    # default creator id should always be 1, because the default is
    # always the first creator row created.
    # TODO: don't hardcode this.
    document_creator_params = {
        'document_id': new_document_id,
        'creator_id': 1
        }
    insert(conn, db.documents_creators, document_creator_params)
    document_identifier_params = {
        'document_namespace_id': doc_namespace_id,
        'document_id': new_document_id,
        'id_string': 'spdxref-document'
        }
    # create all identifiers
    insert(conn, db.identifiers, document_identifier_params)
    create_all_identifiers(conn, doc_namespace_id, package)
    # TODO: create known relationships
    autocreate_relationships(conn, new_document_id)
    return new_document

    


def fetch(conn, table, pkey):
    [c] = list(table.primary_key)
    query = select([table]).where(c == pkey)
    [result] = conn.execute(query).fetchall() or [None]
    if result is None:
        return None
    else:
        return dict(**result)


def get_doc_by_package_id(conn, package_id):
    query = select([db.documents]).where(db.documents.c.package_id == package_id)
    # could potentially return more than one
    # but that's OK
    result = conn.execute(query).fetchone()
    if result is None:
        return None
    else:
        return dict(**result)
