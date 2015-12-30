#!/usr/bin/python

import os
import sys
import shutil

batfile         = "C:\\local.bat"
strorelibdir    = "C:\\zy\\build_backup\\snap2"
missfiles       = ["bsafe.rc","nsdhelp.lib","bsafe.lbn","gsk8iccs.lbn","itp.lbn","pkcs11.lbn","pkcs12.lbn","rsa3.lbn","secure.lbn","vdasfl.lbn",
                   "desk.lbn","dtcryptotest.lbn","ebsafe.lbn","icc.lbn","nxpm.lbn","rsa.lbn","servicl.lbn","tipem.lbn","tipem2.lbn"]
nosedirstr      = "set NOTESDIR="
libpath         = "\\bin\\w32\\lib"
binpath         = "\\bin\\w32\\bin"
needcheckfile   = []

def checkfile(filename):
    if os.path.exists(filename) == False:
        print ("Can not find the:",filename)
    else:
        print ("Find the",filename)

def checkpath(path):
    if os.path.isdir(path):
        return True
    else:
        print("Can not find the ",path," path.")
        return False

def main():
    print("Check some files for notes build process.")
    try:
        localfile = open(batfile,"r")
        allline   = localfile.readlines()
        for line in allline:
            if line[0:len(nosedirstr)] == nosedirstr:
                notesdirtemp = line.split("=")[-1]
                notesdir     = notesdirtemp.split("\n")
                deslibdir    = notesdir[0] + libpath
                needcheckfile.append(notesdir[0] + libpath + "\\nnotes.lib")
                needcheckfile.append(notesdir[0] + libpath + "\\gmock.lbn")
                needcheckfile.append(notesdir[0] + binpath + "\\nnotes.dll")
                needcheckfile.append(notesdir[0] + binpath + "\\utsolr.exe")
                needcheckfile.append(notesdir[0] + binpath + "\\nxmlproc.dll")
                needcheckfile.append(notesdir[0] + binpath + "\\solrpopulator.dll")
                needcheckfile.append(notesdir[0] + binpath + "\\nsolrpopulator.exe")
                break
    finally:
        localfile.close()

    for i in needcheckfile:
        checkfile(i)

    print()
    if (checkpath(deslibdir) and checkpath(strorelibdir)):
        for i in missfiles:
            specialfile = deslibdir + "\\" + i
            if os.path.exists(specialfile) == False:
                sourmissfile = strorelibdir + "\\" + i
                print ("Can not find the " , specialfile," copy it from ",sourmissfile)
                shutil.copy(sourmissfile,deslibdir)
            else:
                print ("Find the",specialfile)

if __name__ == '__main__':
    main()
