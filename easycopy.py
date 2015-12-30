#!/usr/bin/python

import os
import sys
import time;
from time import sleep,ctime
import shutil
import threading
import tkinter

filesnum = 0
separator = "\\" if sys.platform == 'win32' else "/"
StartedCopy = False

class MyThread(threading.Thread):
    def __init__(self,func,args,name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args

    def getResult(self):
        return self.res

    def run(self):
       self.func(*self.args)

class EasyCopyScreen(object):
    def __init__(self,filepath_sour,const_source_folder,filepath_dest,extend_name_group):
        global StartedCopy
        self.filepath_sour = filepath_sour
        self.const_source_folder = const_source_folder
        self.filepath_dest = filepath_dest
        self.extend_name_group = extend_name_group
        StartedCopy = False
        
        self.funcs = [self.start_copyfiles]
        self.nfuncs = range(len(self.funcs))
        self.threads = []

        for i in self.nfuncs:
            t = MyThread(self.funcs[i],(self.filepath_sour,self.const_source_folder,self.filepath_dest,self.extend_name_group), self.funcs[i].__name__)
            self.threads.append(t)

        top=tkinter.Tk()
        label=tkinter.Label(top,text='EasyCopy')
        b_start=tkinter.Button(top,text='Start Copy',command=self.button_start_copyfiles)
        b_stop=tkinter.Button(top,text='Stop Copy',command=self.button_cancel_copyfile)
        label.pack()
        b_start.pack()
        b_stop.pack()
        tkinter.mainloop()

    def start_copyfiles(self,filepath_sour,const_source_folder,filepath_dest,extend_name_group):
        copyfiles(self.filepath_sour,self.const_source_folder,self.filepath_dest,self.extend_name_group)


    def button_start_copyfiles(self):
        global StartedCopy
        if not StartedCopy:
            StartedCopy = True

            # for i in self.nfuncs:
                # self.threads[i].setDaemon(True)

            for i in self.nfuncs:
                self.threads[i].start()

            #for i in self.nfuncs:
            #    self.threads[i].join()
                


    def button_cancel_copyfile(self):
        global StartedCopy
        StartedCopy = False
        for i in self.nfuncs:
            self.threads[i].join()
        # top.destroy


def copyfiles(filepath_sour,const_source_folder,filepath_dest,extend_name_group):
    global filesnum

    if not StartedCopy:
        return

    filelist = os.listdir(filepath_sour)  
    for num in range(len(filelist)):  
        filename=filelist[num]  
        if os.path.isdir(filepath_sour + separator + filename):
            copyfiles(filepath_sour + separator + filename,const_source_folder,filepath_dest,extend_name_group)
        else:
            extend = os.path.splitext(filename)
            if extend[-1] == '' or extend[-1] in extend_name_group or extend_name_group[0] == ".*":
                dest_path = filepath_dest + separator + const_source_folder.split(separator)[-1] + filepath_sour.replace(const_source_folder,"")
                dest_file = dest_path + separator + filename

                if not os.path.isdir(dest_path):
                    os.makedirs(dest_path)

                shutil.copy(filepath_sour + separator + filename,dest_file)
                filesnum += 1
                print("copy the ",filepath_sour + separator + filename," to ", dest_file)

def main():
    sourcepath = input("Enter your source path: ")
    destinationpath = input("Enter your destination path: ")
    extend_type_groups = [".txt",".doc",".pdf",".htm",".html",".jpg",".xls",".c",".h"]
    # extend_type_groups = [".*"]

    b_sourcepath = os.path.isdir(sourcepath)
    b_destpath = os.path.isdir(destinationpath)

    if b_sourcepath == False:
        print ("invalid path:", sourcepath)

    if b_destpath == False:
        print ("invalid path:", destinationpath)

    if sourcepath == destinationpath:
        print("source path can't same with the destination path.")
    elif (b_sourcepath == True and b_destpath == True):
        print("start at:", ctime())
        
        d = EasyCopyScreen(sourcepath,sourcepath,destinationpath,extend_type_groups)

        # copyfiles(sourcepath,sourcepath,destinationpath,extend_type_groups)
        print("Copy ", filesnum , " files.")
        print("Copy is over, at:", ctime())
    else:
        print ("End")

if __name__ == '__main__':
    main()
