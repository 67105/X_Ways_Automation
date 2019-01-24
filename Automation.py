import tkinter
import os
from tkinter import filedialog
from tkinter import *
import subprocess
import ctypes

ext = (".dd",".e01",".bin",".img",".ctr",".vmdk",".vdi",".vhd")


def getImageFileList(pathIn):
    retList = []
    for root,dirs,files in os.walk(pathIn):
        for file in files:
            if file.lower().endswith(tuple(ext)):
                retList.append(os.path.join(root,file))
    return retList


class AutomationGUI:
    def __init__(self,master):
        self.master = master
        master.title("Automated X-Ways Processing")
        self.labelTitle = tkinter.Label(master,text="Select Processing Options:")
        self.labelTitle.pack()
        self.labelTitle.grid(columnspan =2, sticky=W)
        self.labelXPath = tkinter.Label(master,text="X-Ways Path:")
        self.labelXPath.grid(row=1)
        self.textXPath = tkinter.Text(master, height = 1,width =50)
        self.textXPath.insert(END, "C:\\Program Files\\X-Ways Forensics\\")
        self.textXPath.grid(row=1,column=1)
        #case name
        self.labelXName = tkinter.Label(master,text="X-Ways Case Name:")
        self.labelXName.grid(row=2)
        self.textXName = tkinter.Text(master, height = 1,width =50)
        self.textXName.insert(END, "01234-19")
        self.textXName.grid(row=2,column=1)
        #output case directory
        self.labelXLocation = tkinter.Label(master,text="X-Ways Case Directory:")
        self.labelXLocation.grid(row=3)
        self.textXLocation = tkinter.Text(master, height = 1,width =50)
        self.textXLocation.grid(row=3,column=1)
        self.buttonXLocation = Button(master, text="...",command=self.GetCaseDir)
        self.buttonXLocation.grid(row=3,column=3)
        #image file location
        self.labelILocation = tkinter.Label(master,text="Image File Directory:")
        self.labelILocation.grid(row=4)
        self.textILocation = tkinter.Text(master, height = 1,width =50)
        self.textILocation.grid(row=4,column=1)
        self.buttonILocation = Button(master, text="...",command=self.GetImagesDir)
        self.buttonILocation.grid(row=4,column=3)        
        #case config file
        self.labelXConfig = tkinter.Label(master,text="X-Ways Config File (Optional):")
        self.labelXConfig.grid(row=5)
        self.textXConfig = tkinter.Text(master, height = 1,width =50)
        self.textXConfig.grid(row=5,column=1)
        self.buttonXConfig = Button(master, text="...",command=self.GetConfigFile)
        self.buttonXConfig.grid(row=5,column=3)          
        #start button
        self.buttonStart = Button(master, text="Start",command=self.Start)
        self.buttonStart.grid(row=6, column=1)

    def Start(self):
        commandString = ""
        executeString = ""
        path = self.textILocation.get("1.0",END)
        path = path.replace('\n','\\')
        listE01 = getImageFileList(path)
        executeString = executeString +  self.textXPath.get("1.0",END).replace('\n','') + "xwforensics64.exe "
        commandString = commandString + "NewCase:\"" + self.textXLocation.get("1.0",END).replace('\n','') + '\\' + self.textXName.get("1.0",END).replace('\n','') + "\" "
        for E01 in listE01:
            commandString = commandString + "AddImage:\"" + E01 + "\" "
        optConfig = self.textXConfig.get("1.0",END)
        optConfig = optConfig.replace('\n','')
        if optConfig != "":
            commandString = commandString + "Cfg:\"" + optConfig + "\" "
        commandString = commandString + "RVS:~auto"
        print(executeString + commandString)
        ctypes.windll.shell32.ShellExecuteW(None,'open', executeString,commandString,None,1)
         
    def GetCaseDir(self):
        path = filedialog.askdirectory()
        path = path.replace('/','\\')
        path = path.replace('\n','')
        self.textXLocation.insert(END, path)

    def GetImagesDir(self):
        path = filedialog.askdirectory()
        path = path.replace('/','\\')
        path = path.replace('\n','')
        self.textILocation.insert(END, path)

    def GetConfigFile(self):
        path = filedialog.askopenfilename()
        self.textXConfig.insert(END, path)        
   

root = tkinter.Tk()
AutoGUI = AutomationGUI(root)
root.mainloop()
