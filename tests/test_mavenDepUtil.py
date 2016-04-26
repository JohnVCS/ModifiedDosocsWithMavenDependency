#awesome test
from dosocs2 import mavenDepUtil
import os

def test_directory_get_created_in_tmp_createTempDirectoryIfDoesntExist():
    mavenDepUtil.createTempDirectoryIfDoesntExist()
    assert os.path.exists(r'/tmp/mydep')

def test_directory_get_created_in_tmp_createTempDirectoryIfDoesntExist():
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
    correct_output="""
<ns0:graphml xmlns:ns0="http://graphml.graphdrawing.org/xmlns" xmlns:ns2="http://www.yworks.com/xml/graphml" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">
  <ns0:key for="node" id="d0" yfiles.type="nodegraphics" /> 
  <ns0:key for="edge" id="d1" yfiles.type="edgegraphics" /> 
<ns0:graph edgedefault="directed" id="dependencies">
<ns0:node id="562685863"><ns0:data key="d0"><ns2:ShapeNode><ns2:NodeLabel>quartz:quartz:jar:1.5.2</ns2:NodeLabel></ns2:ShapeNode></ns0:data></ns0:node>
<ns0:node id="168870325"><ns0:data key="d0"><ns2:ShapeNode><ns2:NodeLabel>commons-logging:commons-logging:jar:1.0.4:compile</ns2:NodeLabel></ns2:ShapeNode></ns0:data></ns0:node>
<ns0:edge source="562685863" target="168870325"><ns0:data key="d1"><ns2:PolyLineEdge><ns2:EdgeLabel>compile</ns2:EdgeLabel></ns2:PolyLineEdge></ns0:data></ns0:edge>
<ns0:node id="1682619279"><ns0:data key="d0"><ns2:ShapeNode><ns2:NodeLabel>commons-beanutils:commons-beanutils-bean-collections:jar:1.7.0:compile</ns2:NodeLabel></ns2:ShapeNode></ns0:data></ns0:node>
<ns0:edge source="562685863" target="1682619279"><ns0:data key="d1"><ns2:PolyLineEdge><ns2:EdgeLabel>compile</ns2:EdgeLabel></ns2:PolyLineEdge></ns0:data></ns0:edge>
<ns0:node id="440472115"><ns0:data key="d0"><ns2:ShapeNode><ns2:NodeLabel>commons-digester:commons-digester:jar:1.7:compile</ns2:NodeLabel></ns2:ShapeNode></ns0:data></ns0:node>
<ns0:node id="1882348832"><ns0:data key="d0"><ns2:ShapeNode><ns2:NodeLabel>commons-beanutils:commons-beanutils:jar:1.6:compile</ns2:NodeLabel></ns2:ShapeNode></ns0:data></ns0:node>
<ns0:edge source="440472115" target="1882348832"><ns0:data key="d1"><ns2:PolyLineEdge><ns2:EdgeLabel>compile</ns2:EdgeLabel></ns2:PolyLineEdge></ns0:data></ns0:edge>
<ns0:node id="2082678778"><ns0:data key="d0"><ns2:ShapeNode><ns2:NodeLabel>commons-collections:commons-collections:jar:2.1:compile</ns2:NodeLabel></ns2:ShapeNode></ns0:data></ns0:node>
<ns0:edge source="440472115" target="2082678778"><ns0:data key="d1"><ns2:PolyLineEdge><ns2:EdgeLabel>compile</ns2:EdgeLabel></ns2:PolyLineEdge></ns0:data></ns0:edge>
<ns0:node id="1300528434"><ns0:data key="d0"><ns2:ShapeNode><ns2:NodeLabel>xml-apis:xml-apis:jar:1.0.b2:compile</ns2:NodeLabel></ns2:ShapeNode></ns0:data></ns0:node>
<ns0:edge source="440472115" target="1300528434"><ns0:data key="d1"><ns2:PolyLineEdge><ns2:EdgeLabel>compile</ns2:EdgeLabel></ns2:PolyLineEdge></ns0:data></ns0:edge>
<ns0:edge source="562685863" target="440472115"><ns0:data key="d1"><ns2:PolyLineEdge><ns2:EdgeLabel>compile</ns2:EdgeLabel></ns2:PolyLineEdge></ns0:data></ns0:edge>
<ns0:node id="1598434875"><ns0:data key="d0"><ns2:ShapeNode><ns2:NodeLabel>commons-dbcp:commons-dbcp:jar:1.2.1:compile</ns2:NodeLabel></ns2:ShapeNode></ns0:data></ns0:node>
<ns0:node id="1031775150"><ns0:data key="d0"><ns2:ShapeNode><ns2:NodeLabel>commons-pool:commons-pool:jar:1.2:compile</ns2:NodeLabel></ns2:ShapeNode></ns0:data></ns0:node>
<ns0:edge source="1598434875" target="1031775150"><ns0:data key="d1"><ns2:PolyLineEdge><ns2:EdgeLabel>compile</ns2:EdgeLabel></ns2:PolyLineEdge></ns0:data></ns0:edge>
<ns0:node id="1476812556"><ns0:data key="d0"><ns2:ShapeNode><ns2:NodeLabel>xerces:xercesImpl:jar:2.0.2:compile</ns2:NodeLabel></ns2:ShapeNode></ns0:data></ns0:node>
<ns0:edge source="1598434875" target="1476812556"><ns0:data key="d1"><ns2:PolyLineEdge><ns2:EdgeLabel>compile</ns2:EdgeLabel></ns2:PolyLineEdge></ns0:data></ns0:edge>
<ns0:edge source="562685863" target="1598434875"><ns0:data key="d1"><ns2:PolyLineEdge><ns2:EdgeLabel>compile</ns2:EdgeLabel></ns2:PolyLineEdge></ns0:data></ns0:edge>
<ns0:node id="906347731"><ns0:data key="d0"><ns2:ShapeNode><ns2:NodeLabel>javax.servlet:servlet-api:jar:2.4:provided</ns2:NodeLabel></ns2:ShapeNode></ns0:data></ns0:node>
<ns0:edge source="562685863" target="906347731"><ns0:data key="d1"><ns2:PolyLineEdge><ns2:EdgeLabel>provided</ns2:EdgeLabel></ns2:PolyLineEdge></ns0:data></ns0:edge>
</ns0:graph></ns0:graphml>
    """
    
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


    assert parsed == expected_parsed 
