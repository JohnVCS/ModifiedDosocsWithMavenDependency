## System Description

  fossologyFunTime is a tool that provides features that will be merged into DoSOCSv2 to persist dependency information in the DoSOCSv2 database.
  
fossologyFunTime works by accepting a POM.xml file and the project artifact from a user. The POM.xml is passed to a python script that uses Maven. Maven allows the ability to get the transitive dependency hierarchy metadata from the passed POM.xml file. It also has the ability to grab transitive dependencies from maven central. These two features will be invoked using our python script. The transitive dependencies will be placed into a temporary directory to be scanned by DoSOCSv2, and the transitive dependency hierarchy metadata will passed to a DoSOCSv2 Maven Dependency plugin which will facilitate DoSOCSv2’s ability to persist the HAS_PREREQUISITE and PREREQUISITE_FOR relationships defined in the relationship_types SPDX schema.

  Eventually fossologyFunTime will be merged with the DOSOCSv2 project. It'll work in series of steps. First the project will be scanned by DoSOCS and a document will be generated. From here DoSOCSv2 will request the dependency source achieves into a temporary directory. The dependency source archives will be scanned and documents will be created for them. After all the documents are created the dependency hierarchy metadata will be persisted in its affiliated document via package identifiers. These dependency relationships will be seen at the project artifact document via external document references.


### Atribution for implementation ideas
Thomas T Gurney helped in the decision to use external document references to get depedency relationships across different namespaces. 

## Development Environment
OS 
 * (John)   -  Ubuntu 14.04 
 * (Jesse)  -  Ubuntu Gnome 15.10
 
IDE
* Eclipse/Pydev

Language(s)
* Python 2.7.x

Dependency
* Maven 3.3.3 - https://gist.github.com/ervinb/34203f0cc54c1e7f982b (Link on how to install for ubuntu 14.04 - You also need to create a directory called .semaphore-cache)

## Use Case
```
        title
                Developer submits pom.xml and artifact to generate spdx document that shows depdency relationships for legal and security purposes.
        primary actor
                external entity - developer
        goal in context
                Developer wants to generate spdx document with depedency information for legal and security purposes.
        stakeholders and interests
                decision maker/manager - want to see spdx information for legal and security purposes
                lawyer/legal professionals -  want to see spdx information for legal and security purposes
                spdx community - want to see spdx information for legal and security purposes
                IT auditing companies -  want to see spdx information for legal and security purposes
        preconditions
          Valid pom file and prebuilt artifact
          Proper connections with dosocs db and maven central
        success scenario
                Depedency relationship information is persisted in the dosocs database.
                Valid spdx document is printable.
        failed end condition
                can't connect to maven central
                can't connect to dosocs
                non-valid pom
                non-valid artifact
                  artifact/depedencies don't contain sources - this is needed for the license scanner
        trigger
                pom.xml/project artifact
```

## Communication Management Plan
Your Team -
Jesse and John communicate through phone/email and in person. We are both taking the same classes currently, and we schedule a face-to-face meeting at PKI every weekend. In addition, we are also using Github's issue tracker as another means of communication.

* Your Community 
  * irc
    * freenode
      * #spdx
* DoSOCSv2
  * Thomas T Gurney <ttg@tuta.io>  
* SPDX

## Data Flow Diagram of the System
The list is for the external references.
!["Data Flow Diagram"](https://raw.githubusercontent.com/JohnVCS/fossologyFunTime/master/SchemaAndDataFlowImages/Diagram2.png)

## DoSOCSv2 Schema
!["DoSOCSv2 Schema"](https://raw.githubusercontent.com/JohnVCS/fossologyFunTime/master/SchemaAndDataFlowImages/SchemaDiagramDoSocs.png)
!["DoSOCSv2 Schema Partial"](https://raw.githubusercontent.com/JohnVCS/fossologyFunTime/master/SchemaAndDataFlowImages/schemaPartial.png)


## Dependencies
DoSOCSv2 - https://github.com/DoSOCSv2/DoSOCSv2

networkx



##Usage
```python
usage: main.py [-h] [-db DATABASE] [-d DIRECTORY] [-u USERNAME] [-p PASSWORD]

processes licenses and throws into DB

optional arguments:
  -h, --help            show this help message and exit
  -db DATABASE, --database DATABASE
                        database name
  -d DIRECTORY, --directory DIRECTORY
                        directory path to package
  -u USERNAME, --username USERNAME
                        your username
  -p PASSWORD, --password PASSWORD
                        your password
```

dosocs2 
=======

branch | status
--- | ---
master | [![Build Status](https://travis-ci.org/DoSOCSv2/DoSOCSv2.svg?branch=master)](https://travis-ci.org/DoSOCSv2/DoSOCSv2)
dev | [![Build Status](https://travis-ci.org/DoSOCSv2/DoSOCSv2.svg?branch=dev)](https://travis-ci.org/DoSOCSv2/DoSOCSv2)

dosocs2 is a command-line tool for managing SPDX 2.0 documents and data. It can
scan source code distributions to produce SPDX information, store that
information in a relational database, and extract it in a plain-text format
on request.

dosocs2 enables easy creation of a "bill of materials" for any software package,
and can even be used in the creation and continuous maintenance of an inventory
of all open-source software used in an organization.

[SPDX](http://www.spdx.org) is a standard format for communicating information
about the contents of a software package, including license and copyright
information. dosocs2 supports the SPDX 2.0 standard, released in May 2015.

dosocs2 is under heavy development; expect frequent backwards-incompatible
changes until a 1.x.x release!

### Current deviations from SPDX 2.0 specification

* Exactly one package per document is required. (SPDX 2.0 allows zero or more
  packages per document.)
* Files in a document can only exist within a package. (SPDX 2.0 allows files
  to exist outside of a package.)
* Checksums are always assumed to be SHA-1. (SPDX 2.0 permits SHA-1, SHA-256,
  and MD5)
* A file may be an artifact of only one project.
* License expression syntax is not parsed; license expressions are interpreted as license
  names that are not on the SPDX license list.
* Deprecated fields from SPDX 1.2 (reviewer info and file dependencies) are not supported.


License and Copyright
---------------------

Copyright © 2015 University of Nebraska at Omaha

dosocs2 is free software: you can redistribute it and/or modify it under the
terms of the GNU General Public License as published by the Free Software
Foundation, either version 2 of the License, or (at your option) any later
version. See the file LICENSE for more details.

All associated documentation is licensed under the terms of the Creative
Commons Attribution Share-Alike 3.0 license. See the file CC-BY-SA-3.0 for more
details.


Dependencies
------------

- Python 2.7.x

Optional:
- PostgreSQL 8.x or later version (can be on a separate machine)

Python libraries:
- All Python dependencies are handled automatically by `pip`.


Installation
------------

### Step 1 - Download and install

[Grab the source tarball for the latest
release](https://github.com/ttgurney/dosocs2/releases) and use `pip` to install
it as a package. Replace `0.x.x` with the latest release version number.

I recommend doing this inside a Python
[virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/), but it
is not a requirement. If you are not inside a virtualenv you may have to run
`pip` as root (not recommended!).


    $ tar xf 0.x.x.tar.gz
    $ pip install ./DoSOCSv2-0.x.x

Then run the install script for the default license scanner:

    $ ./DoSOCSv2-0.x.x/scripts/install-nomos.sh

### Step 2 (Optional) - Change the default configuration

Not required, but strongly recommended, is to generate an initial config
file:

    $ dosocs2 newconfig
    dosocs2: wrote config file to /home/tom/.config/dosocs2/dosocs2.conf

The default config points to a SQLite database stored in your home directory.
For example, for user `tom`, this database would be created at
`/home/tom/.config/dosocs2/dosocs2.sqlite3`. If you like, you can open the
config file and change the `connection_uri` variable to use a different
location for the database.


### Step 3 (Optional) - Add PostgreSQL configuration

Follow this step if you want to use PostgreSQL instead of SQLite for the
SPDX database.

You will have to create the `spdx` (or whatever name you want) role and
database yourself.  I recommend setting a different password than the
one given...:

    $ sudo -u postgres psql
    psql (9.3.9)
    Type "help" for help.

    postgres=# create role spdx with login password 'spdx';
    CREATE ROLE
    postgres=# create database spdx with owner spdx;
    CREATE DATABASE

Then change the `connection_uri` variable in your `dosocs2.conf`:

    # connection_uri = postgresql://user:pass@host:port/database
    connection_uri = postgresql://spdx:spdx@localhost:5432/spdx


### Step 4 - Database setup

Finally, to create all necessary tables and views in the database:

    $ dosocs2 dbinit

You only need to do this once. **This command will drop all
existing tables from your SPDX database, so be careful!**

Usage
-----

The simplest use case is scanning a package, generating a
document, and printing an SPDX document in one shot:

    $ dosocs2 oneshot package.tar.gz
    dosocs2: package.tar.gz: package_id: 1
    dosocs2: running nomos on package 1
    dosocs2: package.tar.gz: document_id: 1
    [... document output here ...]

Also works on directories:

    $ dosocs2 oneshot ./path/to/directory

The scan results and other collected metadata are saved in the database
so that subsequent document generations will be much faster.

To just scan a package and store its information in the database:

    $ dosocs2 scan package.tar.gz
    dosocs2: package_tar_gz: package_id: 456
    dosocs2: running nomos on package 456

In the default configuration, if a scanner is not specified, only `nomos`
is run by default. It gathers license information, but is a bit slow.
One can use the `-s` option to explicitly specify which scanners to run:

    $ dosocs2 scan -s nomos_deep,dummy package.tar.gz
    dosocs2: package_tar_gz: package_id: 456
    dosocs2: running nomos_deep on package 456
    dosocs2: running dummy on package 456

After `dosocs2 scan`, no SPDX document has yet been created.
To create one in the database (specifying the package ID):

    $ dosocs2 generate 456
    dosocs2: (package_id 456): document_id: 123

Then, to compile and output the document in tag-value format:

    $ dosocs2 print 123
    [... document output here ...]

Use `dosocs2 --help` to get the full help text. The `doc` directory
here also provides more detailed information about how `dosocs2` works
and how to use it.


History
-------

dosocs2 owes its name and concept to the
[DoSOCS](https://github.com/socs-dev-env/DoSOCS) tool created by Zac
McFarland, which in turn was spun off from the [do_spdx](https://github.com/ttgurney/yocto-spdx/blob/master/src/spdx.bbclass) plugin for Yocto
Project, created by Jake Cloyd and Liang Cao.

dosocs2 aims to fill the same role as DoSOCS, but with support for SPDX 2.x, a
larger feature set, and a more modular implementation, among other changes.


Maintainers
-----------

[DoSOCSv2 organization](https://github.com/DoSOCSv2)


(This work has been funded through the National Science Foundation VOSS-IOS Grant: 1122642.)
