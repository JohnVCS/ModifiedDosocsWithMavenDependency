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
    