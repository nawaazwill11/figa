import os
import errno

def validPath(path):
    if(os.path.exists(path)):
        return True
    else:
        return (FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), path))