import os, tkinter as tk, re 
import list_files, log, helper
from datetime import datetime
import tkinter.ttk as ttk
from PIL import Image, ImageTk

class Graphics(object):

    def __init__(self, master):
        self.master = master
        self.makeUI()

    def imagePreview(self, image):
        previewFrame = tk.Toplevel(self.master)
        previewFrame.maxsize(1200, 800)
        previewFrame.config(height=500, width=500)
        match = re.search("[0-9]+$", str(image))
        file_index = int(str(image)[match.span()[0]:]) - 1
        file = self.files_list[file_index]
        image = Image.open(file)
        tkimage = ImageTk.PhotoImage(image)
        imageLabel = tk.Label(previewFrame, image=tkimage)
        imageLabel.image = tkimage
        imageLabel.pack(fill='both', expand=True)
    
    def addElements(self):
        for file in self.files_list:
            element = tk.Frame(self.loadingAreaTxt, bd=1, relief="sunken", background='green', width=100, height=100)
            image = Image.open(file)
            tkimage = ImageTk.PhotoImage(image.resize((50, 50)))
            image_container= tk.Label(element, image=tkimage)
            image_container.bind('<Button-1>', lambda e: self.imagePreview(e.widget.image))
            image_container.image = tkimage
            image_container.pack()
            
            self.elements.append(element)
            self.loadingAreaTxt.window_create(tk.END, window=element, padx=10, pady=10)
            
    def elementLoadLayer(self):
        self.elementsframe = tk.Frame(self.mainframe, bg='blue')
        self.elementsframe.pack(side='bottom', fill='both', expand=1)

        self.loadingAreaTxt = tk.Text(self.elementsframe, wrap="char", borderwidth=0, highlightthickness=0, state="disabled", cursor='arrow', relief='flat', bg='pink')
        self.loadingAreaTxt.pack(fill="both", expand=1)
        self.elements = []
        
    
    def interactiveLayer(self):
        self.interactLayer = tk.Frame(self.mainframe, height=200, width=500, bg=self.mainframe['bg'])
        self.interactLayer.pack(fill='x', side='top')

        self.interactElements = tk.Frame(self.interactLayer, bg=self.mainframe['bg'])
        self.interactElements.pack(expand=1)
        self.pathVar = tk.StringVar()
        self.pathEntry = tk.Entry(self.interactElements, width=50, bd=2, relief='flat', textvariable=self.pathVar)
        self.pathEntry.pack(side='left',pady=10)
        self.loadButton = tk.Button(self.interactElements, text='Load', width=20, bg='#00dcff')
        self.loadButton.pack(side='right')
    
    def makeLogWindow(self):
        self.logWindow = tk.Toplevel(self.master)
        self.logWindow.title('Process logs')
        self.logText = tk.Text(self.logWindow)
        self.logText.pack(side=tk.LEFT, padx=10, pady=10)
        self.logTextScroll = ttk.Scrollbar(self.logWindow)
        self.logTextScroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.logText['yscrollcommand'] = self.logTextScroll.set
        self.logTextScroll['command'] = self.logText.yview
        self.logWindow.protocol('WM_DELETE_WINDOW', self.hideLog) # Doesn't close the window but hides it.

    def makeMenu(self):
        self.menubar = tk.Menu(self.master, relief='flat')
        self.menubar.add_command(label='Logs', command=self.showLog)
        self.master.config(menu=self.menubar)

    def makeUI(self):
        self.makeMenu()
        self.makeLogWindow()
        self.mainframe = tk.Frame(self.master, bg='white') # bg='#fff8d7'
        self.mainframe.pack(fill='both', expand=1)
        self.interactiveLayer()
        self.elementLoadLayer()

class Logic(object):

    def __init__(self):
        # self.path = path
        self.limit = 100000
        # self.main()
        log.emptyLog()

    def loadItems(self):
        path = self.pathVar.get()
        self.files_list = self.makeFilesList(path)
        self.addElements()
    
    def makeFilesList(self, path):
        valid = helper.validPath(path)
        if(valid == True):
            self.addToLog(f'Searching for files in {path}')
            files_list = self.getFilesFromPath([], path)        
            self.printFiles(files_list)
            if (len(files_list) > self.limit): 
                log.addToLog('Limit reached. You can change the limit in the settings.')
            self.addToLog(f"Total files discovered {len(files_list)}")
            self.addToLog(f"Search completed on {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            return files_list
        else:
            self.addToLog(str(valid))
            return []
        
    
    def printFiles(self, files):
        for i, file in enumerate(files):
            self.addToLog(f"{i + 1}. {file}")

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
                files_list.append(file_path)

        if len(dir_list) > 0:
            for directory in dir_list:
                if path == '/':
                    dir_path = path + directory
                else:
                    dir_path = path + '/' + directory
                self.addToLog(f"Searching dir {dir_path}")
                files_list = self.getFilesFromPath(files_list, dir_path)

        return files_list
    
    def addToLog(self, content):
        self.logText.insert(tk.END, content + '\n')
        log.addToLog(content)


class Functions(Logic):
    
    def __init__(self):
        Logic.__init__(self)
        self.bindEvents()
        self.hideLog()
    
    def bindEvents(self):
        self.loadButton['command'] = self.loadItems
    
    def showLog(self):
        self.logWindow.update()
        self.logWindow.deiconify()
    
    def hideLog(self):
        self.logWindow.update()
        self.logWindow.withdraw()


class App(Graphics, Functions):
    
    def __init__(self, master):
        Graphics.__init__(self, master)
        Functions.__init__(self)
        
root = tk.Tk()
root.title('FIGA')
style = ttk.Style()
style.theme_use('clam')
app = App(root)
root.minsize(800, 700)
root.configure(background='#fff8d7')
root.mainloop()