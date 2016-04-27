#awesome test
from dosocs2 import mavenDepUtil
import os

def test_directory_get_created_in_tmp_createTempDirectoryIfDoesntExist():
    mavenDepUtil.createTempDirectoryIfDoesntExist()
    assert os.path.exists(r'/tmp/mydep')

def test_directory_deletes_contents_in_tmp_mydep_createTempDirectoryIfDoesntExist():
    #create mydep directory
    mavenDepUtil.createTempDirectoryIfDoesntExist()
    
    #create file1 in mydep directory
    filename="/tmp/mydep/file1"
    with open(filename, 'a'):
        os.utime(filename, None)
        
    assert os.path.exists(r'/tmp/mydep')
    assert os.path.isfile(r'/tmp/mydep/file1')
    
    
    #contents of directory should be deleted after method is ran
    mavenDepUtil.createTempDirectoryIfDoesntExist()
    assert not os.path.isfile(r'/tmp/mydep/file1')
    
def test_createGraphMl():
    mavenDepUtil.createGraphMl(r'sample_project_and_pom/pom.xml')
    assert os.path.isfile(r'/tmp/test.graphml')
    
    from xml.etree import ElementTree as ET
    xmlstr=open(r'/tmp/test.graphml','r').read()
    x = ET.fromstring(xmlstr)
    #test to see whether x throws excpetion
    assert x != None 

def test_parseGraphMl():
    mavenDepUtil.createGraphMl(r'sample_project_and_pom/pom.xml')
    assert os.path.isfile(r'/tmp/test.graphml')

    parsed=mavenDepUtil.parseGraphMl()
#     expected_parsed=[('commons-dbcp:commons-dbcp:jar:1.2.1:compile', 'xerces:xercesImpl:jar:2.0.2:compile'), ('commons-dbcp:commons-dbcp:jar:1.2.1:compile', 'commons-pool:commons-pool:jar:1.2:compile'), ('quartz:quartz:jar:1.5.2', 'javax.servlet:servlet-api:jar:2.4:provided'), ('quartz:quartz:jar:1.5.2', 'commons-beanutils:commons-beanutils-bean-collections:jar:1.7.0:compile'), ('quartz:quartz:jar:1.5.2', 'commons-dbcp:commons-dbcp:jar:1.2.1:compile'), ('quartz:quartz:jar:1.5.2', 'commons-logging:commons-logging:jar:1.0.4:compile'), ('quartz:quartz:jar:1.5.2', 'commons-digester:commons-digester:jar:1.7:compile'), ('commons-digester:commons-digester:jar:1.7:compile', 'commons-beanutils:commons-beanutils:jar:1.6:compile'), ('commons-digester:commons-digester:jar:1.7:compile', 'xml-apis:xml-apis:jar:1.0.b2:compile'), ('commons-digester:commons-digester:jar:1.7:compile', 'commons-collections:commons-collections:jar:2.1:compile')]
    expected_parsed=[('commons-digester:commons-digester:jar:1.7:compile', 'xml-apis:xml-apis:jar:1.0.b2:compile'), ('commons-digester:commons-digester:jar:1.7:compile', 'commons-beanutils:commons-beanutils:jar:1.6:compile'), ('commons-digester:commons-digester:jar:1.7:compile', 'commons-collections:commons-collections:jar:2.1:compile'), ('quartz:quartz:jar:1.5.2', 'javax.servlet:servlet-api:jar:2.4:provided'), ('quartz:quartz:jar:1.5.2', 'commons-logging:commons-logging:jar:1.0.4:compile'), ('quartz:quartz:jar:1.5.2', 'commons-digester:commons-digester:jar:1.7:compile'), ('quartz:quartz:jar:1.5.2', 'commons-dbcp:commons-dbcp:jar:1.2.1:compile'), ('quartz:quartz:jar:1.5.2', 'commons-beanutils:commons-beanutils-bean-collections:jar:1.7.0:compile'), ('commons-dbcp:commons-dbcp:jar:1.2.1:compile', 'commons-pool:commons-pool:jar:1.2:compile'), ('commons-dbcp:commons-dbcp:jar:1.2.1:compile', 'xerces:xercesImpl:jar:2.0.2:compile')]
    
    for tupple in parsed:
        assert tupple in expected_parsed