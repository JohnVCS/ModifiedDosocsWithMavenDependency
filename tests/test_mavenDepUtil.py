def test_createTempDirectoryIfDoesntExist():
    from dosocs2 import mavenDepUtil
    import os
    mavenDepUtil.createTempDirectoryIfDoesntExist()
    assert os.path.exists(r'/tmp/mydep')