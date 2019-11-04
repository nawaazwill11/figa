import os

def logExists():
    if ('log.txt' in os.listdir('.')):
        return True
    return False

def logFile(mode=None):
    if mode is None:
        if (not logExists()):
            mode = 'w'
        else:
            mode = 'a'    
    file = open('log.txt', mode)
    return file

def addToLog(line):
    file = logFile()
    file.write(line + '\n')
    file.close()

def emptyLog():
    file = logFile('w')
    file.write('')
    file.close()
    
    
