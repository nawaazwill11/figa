import os
from datetime import datetime
import helper
import log

class FileLister(object):

    def __init__(self):
        # self.path = path
        self.limit = 10000
        # self.main()

    
    def makeFilesList(self, path):
        valid = helper.validPath(path)
        if(valid == True):
            log.addToLog(f'Searching for files in {path}')
            files_list = self.getFilesFromPath([], path)        
            self.printFiles(files_list)
            if (len(files_list) > self.limit): 
                log.addToLog('Limit reached. You can change the limit in the settings.')
            log.addToLog(f"Total files discovered {len(files_list)}")
            log.addToLog(f"Search completed on {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        else:
            log.addToLog(str(valid))
    
    def printFiles(self, files):
        for i, file in enumerate(files):
            log.addToLog(f"{i + 1}. {file}")

    def getFilesFromPath(self, files_list, path):
        dir_list = []
        for file in os.listdir(path):
            # if file == '.speech-dispatcher': continue
            if (len(files_list) > self.limit - 1): 
                return files_list
            if path == '/':
                file_path = path + file
            else:
                file_path = path + '/' + file    
            if os.path.isdir(file_path):
                dir_list.append(file)
            else:
                files_list.append(file)

        if len(dir_list) > 0:
            for directory in dir_list:
                if path == '/':
                    dir_path = path + directory
                else:
                    dir_path = path + '/' + directory
                log.addToLog(f"Searching dir {dir_path}")
                files_list = self.getFilesFromPath(files_list, dir_path)

        return files_list
