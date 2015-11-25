import os, shlex
import transaction
from BTrees.OOBTree import OOBTree
import tempfile, subprocess

def getContainer(root, containerName):
    """
    return a ZODB container, create it if not yet exists
    """
    cont = getattr(root, containerName, None)
    if not cont:
        setattr(root, containerName, OOBTree())
        transaction.commit()
        cont = getattr(root, containerName)
    return cont

def editContent(content=None):
    """ edit the content with vi editor the input
    'content' is byte, the returned one is byte also
    """
    tmpfile = tempfile.NamedTemporaryFile(delete=False)
    if content:
        tmpfile.write(content)
        tmpfile.flush()
    cmd = 'vi ' + tmpfile.name
    p = subprocess.Popen(shlex.split(cmd))
    p.communicate()
    p.wait()
    tmpfile.seek(0)
    content = tmpfile.read()
    os.unlink(tmpfile.name)
    return content

