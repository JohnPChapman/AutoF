# Forensic case automater
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext
from shutil import copyfile
import sqlite3
import ctypes
import sys
import os
from AutoS import convertPath, jenkinsSettingsWindow, aboutWindow, indexWindow, getXways, imageXSort, \
    generalOptionsWindow, now, create_settings
from AutoX import processImages, xCompound, caseMode, xCombine, xConcurrent
from AutoJ import xnodeMode
from AutoN import processImagesN, nCompound, nConcurrent
from NuixRepath import repath
from CaseInfo import caseInfo
import logging
from autologging import TRACE, traced
import win32com.client
import psutil
from pathlib import Path
from DualTool import dualTool
import re
logging.basicConfig(level=TRACE, filename=('settings\logs\RunLog ' + now() + '.txt'),
                    format="%(asctime)s:%(levelname)s:%(filename)s,%(lineno)d:%(name)s.%(funcName)s:%(message)s")


@traced
def clearAll(event=None):
    global savedPath
    global images
    global versOption
    images = []
    savedPath = ''
    caseSaveText.delete(0, END)
    imageFolderText.config(state=NORMAL)
    imageFolderText.delete(0, END)
    imageFolderText.config(state=DISABLED)
    compoundCaseName.config(state=NORMAL)
    compoundCaseName.delete(0, END)
    compoundCaseName.config(state=DISABLED)
    imageList.config(state=NORMAL)
    imageList.delete('1.0', END)
    imageList.config(state=DISABLED)
    cMode.set(0)
    nMode.set(0)
    compound.set(0)
    xComb.set(0)
    iMonitor.set(0)
    dtMode.set(0)
    ufdrFilter.set(0)
    xConc.set(0)
    imageList.config(state=NORMAL)
    compCheck.config(state=NORMAL)
    cModeCheck.config(state=NORMAL)
    nModeCheck.config(state=NORMAL)
    xCombCheck.config(state=NORMAL)
    ufdrFilterCheck.config(state=NORMAL)
    xConcCheck.config(state=NORMAL)
    versOption.config(state=NORMAL)
    profOption.config(state=NORMAL)
    versOption.destroy()
    versOption = OptionMenu(window, vers, *xVersions, command=xProfile)
    vers.set(xVersions[0])
    versOption.place(x=30, y=190)
    xProfile(profOption)
    ufdrFilter.set(0)
    threadCountSet.set(threadCount[0])
    threadMenu.config(state="disabled")

@traced
def exitAF(event=None):
    sys.exit(0)


# Checks if software is running as admin
@traced
def isAdmin():
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin


# Forces a scan for x-ways installs and CFG
@traced
def forceScan(event=None):
    global xVersions
    global xInstalls
    global xCFG
    global versOption
    MsgBox = tk.messagebox.askquestion('Force Scan', 'You are about to scan your machine '
                                                     'for all processing tools & needed config files. '
                                                     'This may take some time. Are you sure?',
                                       icon='warning')

    if MsgBox == 'yes':
        fconn = sqlite3.connect('settings\\settings.db ')
        fcur = fconn.cursor()
        fcur.execute("DELETE FROM Xways")
        fconn.commit()
        fcur.execute("DELETE FROM CFG")
        fconn.commit()
        xInstalls, xVersions, xCFG = getXways()

        versOption.destroy()
        versOption = OptionMenu(window, vers, *xVersions, command=xProfile)
        vers.set(xVersions[0])
        versOption.place(x=30, y=190)
        xProfile(profOption)
        window.update_idletasks()
        messagebox.showinfo("Force scan", "Scan complete")


# Select where to save created cases COMPLETE
@traced
def caseSaveLocation():
    caseSave = filedialog.askdirectory(title="Select Root folder to save all cases")
    if caseSave == '':
        messagebox.showinfo("ERROR", "No case save path selected!")
    else:
        caseSaveText.delete(0, END)
        caseSaveText.insert(0, caseSave)


# Select all images to process COMPLETE
@traced
def imageSelect():
    global images
    global folderSkip
    global savedPath

    myPath = filedialog.askdirectory(title="select images")
    imageFolderText.config(state=NORMAL)
    imageFolderText.delete(0, END)
    imageFolderText.insert(0, myPath)
    imageFolderText.config(state=DISABLED)

    if iMonitor.get() == 0 and dtMode.get() == 0:
        images = imageXSort(folderSkip, myPath, vers.get(), ufdrFilter.get())

        imageList.config(state=NORMAL)
        imageList.delete('1.0', END)
        for x in images:
            imageList.insert(END, x + '\n\n')
        imageList.config(state=DISABLED)
        if len(images) == 0:
            imageFolderText.config(state=NORMAL)
            imageFolderText.delete(0, END)
            imageFolderText.config(state=DISABLED)
            messagebox.showinfo('ERROR', 'No compatible images found.')


# Find x-ways profiles COMPLETE
@traced
def xProfile(self):

    global xProfiles
    global vers
    getxProfiles = []
    if 'X-ways' in vers.get():
        if os.path.exists('Settings\\X-ways profiles\\') is False:
            profRoot = tk.Tk()
            profRoot.withdraw()
            messagebox.showerror('Error!',
                                 'Profiles directory does not exist. Perhaps the install is not complete')
            sys.exit(1)
        for i in os.listdir('Settings\\X-ways profiles\\'):
            if i.endswith('.cfg'):
                getxProfiles.append(i)

    else:
        for p in os.listdir('Settings\\Nuix\\Scripts\\'):
            if '.rb' in p:
                getxProfiles.append(p)


    if len(getxProfiles) == 0:
        messagebox.showerror('Error!',
                             'No processing profiles found. AutoF will now close')

    prof.set('')
    profOption['menu'].delete(0, 'end')
    for opt in getxProfiles:
        profOption['menu'].add_command(label=opt, command=tk._setit(prof, opt))
        prof.set(getxProfiles[0])

    if imageFolderText.get() == '':
        return
    else:
        myPath = imageFolderText.get()
        if ufdrFilter.get() == 1:
            images = imageXSort(folderSkip, myPath, 'ufdr', ufdrFilter.get())
        else:
            images = imageXSort(folderSkip, myPath, vers.get(), ufdrFilter.get())

        imageList.config(state=NORMAL)
        imageList.delete('1.0', END)
        for x in images:
            imageList.insert(END, x + '\n\n')


# Manages compound tick box behaviour COMPLETE
@traced
def compoundBox():
    if xComb.get() == 1:
        messagebox.showinfo("ERROR", "Single Case Mode is not supported for xCombine!")
        compound.set(0)
    elif compound.get() == 1:
        compoundCaseName.config(state=NORMAL)

    elif compound.get() == 0:
        compoundCaseName.delete(0, END)
        compoundCaseName.config(state=DISABLED)


# Manages caseMode tick box behaviour COMPLETE
@traced
def caseModeBox():
    casePath = caseSaveText.get()
    if casePath == '':
        messagebox.showinfo("ERROR", "Select root folder of cases first")
        cMode.set(0)
        return
    # When un-ticked clears list and enable select image
    elif cMode.get() == 0:
        selectImagesButton.config(state=NORMAL)
        imageList.config(state=NORMAL)
        imageList.delete('1.0', END)
        imageList.config(state=DISABLED)
        compCheck.config(state=NORMAL)
    elif xComb.get() == 1:
        messagebox.showinfo("ERROR", "Node Mode is not supported for Case Mode!")
        cMode.set(0)
    # Disables image select button and populates case list
    elif cMode.get() == 1:
        if nMode.get() == 1:
            messagebox.showinfo("ERROR", "Case Mode is not supported for cases!")
            cMode.set(0)
            selectImagesButton.config(state=NORMAL)
            imageList.config(state=NORMAL)
            imageList.delete('1.0', END)
            imageList.config(state=DISABLED)
            compCheck.config(state=NORMAL)
            return
        version = vers.get()
        if 'nuix' in version.lower():
            messagebox.showinfo("ERROR", "Nuix is not supported for cases!")
            cMode.set(0)
            selectImagesButton.config(state=NORMAL)
            imageList.config(state=NORMAL)
            imageList.delete('1.0', END)
            imageList.config(state=DISABLED)
            compCheck.config(state=NORMAL)
            return
        global images
        images = []
        cases = []
        myPath = caseSaveText.get()
        for cRoot, directories, files in os.walk(myPath, topdown=False):
            for name in files:
                if '.xfc' in name[-4:]:
                    cases.append(convertPath(os.path.join(cRoot, name)))
        selectImagesButton.config(state=DISABLED)
        imageFolderText.config(state=NORMAL)
        imageFolderText.delete(0, END)
        imageFolderText.config(state=DISABLED)
        compoundCaseName.config(state=NORMAL)
        compoundCaseName.delete(0, END)
        compoundCaseName.config(state=DISABLED)
        compound.set(0)
        compoundBox()
        compCheck.config(state=DISABLED)
        imageList.config(state=NORMAL)
        imageList.delete('1.0', END)
        for x in cases:
            imageList.insert(END, x + '\n')
        imageList.config(state=DISABLED)


# Manages caseMode tick box behaviour COMPLETE
@traced
def nodeModeBox():
    nconn = sqlite3.connect('settings\\settings.db ')
    ncur = nconn.cursor()
    ncur.execute("Select * FROM Node")
    nconn.commit()
    nrows = ncur.fetchall()
    if not nrows:
        messagebox.showinfo("ERROR", "Jenkins settings do not exist")
        nMode.set(0)
        return
    elif cMode.get() == 1:
        messagebox.showinfo("ERROR", "Node Mode is not supported for cases!")
        nMode.set(0)
    elif xComb.get() == 1:
        messagebox.showinfo("ERROR", "Node Mode is not supported for xCombine!")
        nMode.set(0)


# Manges image monitor box
@traced
def imageMonitorBox():
    if iMonitor.get() == 1:
        cMode.set(0)
        compound.set(0)
        xComb.set(0)
        compCheck.config(state=DISABLED)
        cModeCheck.config(state=DISABLED)
        xCombCheck.config(state=DISABLED)
        compoundCaseName.config(state=NORMAL)
        compoundCaseName.delete(0, END)
        compoundCaseName.config(state=DISABLED)
        imageList.config(state=NORMAL)
        imageList.delete('1.0', END)
        imageList.config(state=DISABLED)
    elif iMonitor.get() == 0:
        compCheck.config(state=NORMAL)
        cModeCheck.config(state=NORMAL)
        xCombCheck.config(state=NORMAL)

# Managed UFDR filtering behaviour
@traced
def ufdrFilterBox():
    global images
    if ufdrFilter.get() == 1:

        myPath = imageFolderText.get()
        images = imageXSort(folderSkip, myPath, 'ufdr', ufdrFilter.get())
        imageList.config(state=NORMAL)
        imageList.delete('1.0', END)
        for x in images:
            imageList.insert(END, x + '\n\n')

    elif ufdrFilter.get() == 0:
        myPath = imageFolderText.get()
        images = imageXSort(folderSkip, myPath, vers.get(), ufdrFilter.get())
        imageList.config(state=NORMAL)
        imageList.delete('1.0', END)
        for x in images:
            imageList.insert(END, x + '\n\n')

# Manages dual tool Box
def dtBox():
    if dtMode.get() == 1:
        imageList.config(state=NORMAL)
        imageList.delete('1.0', END)
        cMode.set(0)
        nMode.set(0)
        compound.set(0)
        xComb.set(0)
        iMonitor.set(0)
        ufdrFilter.set(0)
        xConc.set(0)
        imageList.config(state=DISABLED)
        compCheck.config(state=DISABLED)
        cModeCheck.config(state=DISABLED)
        nModeCheck.config(state=DISABLED)
        xCombCheck.config(state=DISABLED)
        ufdrFilterCheck.config(state=DISABLED)
        xConcCheck.config(state=DISABLED)
        versOption.config(state=DISABLED)
        profOption.config(state=DISABLED)
        compoundCaseName.config(state=NORMAL)
        compoundCaseName.delete(0, END)
        compoundCaseName.config(state=DISABLED)
        threadCountSet.set(threadCount[0])
        threadMenu.config(state="disabled")
    elif dtMode.get() == 0:
        imageList.config(state=NORMAL)
        compCheck.config(state=NORMAL)
        cModeCheck.config(state=NORMAL)
        nModeCheck.config(state=NORMAL)
        xCombCheck.config(state=NORMAL)
        ufdrFilterCheck.config(state=NORMAL)
        xConcCheck.config(state=NORMAL)
        versOption.config(state=NORMAL)
        profOption.config(state=NORMAL)

        myPath = imageFolderText.get()
        if ufdrFilter.get() == 1:
            images = imageXSort(folderSkip, myPath, 'ufdr', ufdrFilter.get())
        else:
            images = imageXSort(folderSkip, myPath, vers.get(), ufdrFilter.get())

        imageList.config(state=NORMAL)
        imageList.delete('1.0', END)
        for x in images:
            imageList.insert(END, x + '\n\n')

# Manages concurrent box
@traced
def concurrentBox():
    if xConc.get() == 1:
        messagebox.showwarning("Warning", "This is experimental, for X-Ways special settings are required in the CFG")
        threadMenu.config(state="normal")
    else:
        threadCountSet.set(threadCount[0])
        threadMenu.config(state="disabled")

# Skip menu COMPLETE
@traced
def folderSkipWindow(event=None):
    def folderSave():
        global folderSkip
        folderSkip.clear()
        folderSkip = folderSkipText.get("1.0", END).split('\n')

        sconn = sqlite3.connect('settings\\settings.db ')
        scur = sconn.cursor()
        scur.execute("DELETE FROM Skip")
        sconn.commit()
        # Clears empty list elements
        folderSkip = list(filter(None, folderSkip))
        for line in folderSkip:
            scur.execute('INSERT INTO Skip VALUES(?)', (line,))
            sconn.commit()

    fsconn = sqlite3.connect('settings\\settings.db ')
    fscur = fsconn.cursor()
    fscur.execute("SELECT * FROM Skip")
    frows = fscur.fetchall()
    folderSkipWin = Toplevel()
    folderSkipWin.title("Folder Skip")
    folderSkipWin.geometry("300x440")
    folderSkipWin.resizable(width=False, height=False)
    folderSkipWin.grab_set()
    try:
        folderSkipWin.iconbitmap('settings\\ax.ico')
    except:
        messagebox.showerror('Error!',
                             'Can not find AutoF.ico file. Perhaps the install is not complete')
    folderSkipText = Text(folderSkipWin, width=30, height=20, bg="lightgrey", wrap=WORD)
    folderSkipText.pack(pady=10)
    folderSkipText.tag_config('justified', justify=CENTER)
    folderSkipText.config(bg='white')
    folderSkipSave = Button(folderSkipWin, text='Save', command=folderSave)
    folderSkipSave.pack(pady=5, padx=5)
    folderSkipExit = Button(folderSkipWin, text='Exit', command=folderSkipWin.destroy)
    folderSkipExit.pack(pady=5)
    for ind in frows:
        folderSkipText.insert(INSERT, ind[0] + '\n')


# manages xCombine box behaviour
@traced
def xCombineBox():

    versCheck = re.sub("[^0-9.]", "", vers.get())
    if "Nuix" in vers.get():
        messagebox.showinfo("ERROR", "Combining of cases is only supported in X-Ways version 20.3 and later")
        xComb.set(0)
        return
    versCheck = versCheck[:4]
    versCheck = float(versCheck)
    if versCheck < 20.3:
        messagebox.showinfo("ERROR", "Combining of cases is only supported in X-Ways version 20.3 and later")
        xComb.set(0)
        return
    casePath = caseSaveText.get()
    if casePath == '':
        messagebox.showinfo("ERROR", "Select root folder of cases first")
        xComb.set(0)
        return
    elif nMode.get() == 1:
        messagebox.showinfo("ERROR", "xCombine is not supported for Node Mode!")
        xComb.set(0)
    elif cMode.get() == 1:
        messagebox.showinfo("ERROR", "xCombine is not supported for Case Mode!")
        xComb.set(0)
    elif compound.get() == 1:
        messagebox.showinfo("ERROR", "xCombine is not supported for Single Case Mode!")
        xComb.set(0)
    # When un-ticked clears list and enable select image
    elif xComb.get() == 0:
        selectImagesButton.config(state=NORMAL)
        imageList.config(state=NORMAL)
        imageList.delete('1.0', END)
        imageList.config(state=DISABLED)
        compCheck.config(state=NORMAL)
        compoundCaseName.config(state=NORMAL)
        compoundCaseName.delete(0, END)
        compoundCaseName.config(state=DISABLED)
        compound.set(0)
        compoundBox()

    # Disables image select button and populates case list
    elif xComb.get() == 1:
        if nMode.get() == 1:
            messagebox.showinfo("ERROR", "Case Mode is not supported for combining X-Ways cases!")
            xComb.set(0)
            selectImagesButton.config(state=NORMAL)
            imageList.config(state=NORMAL)
            imageList.delete('1.0', END)
            imageList.config(state=DISABLED)
            compCheck.config(state=NORMAL)
            return
        version = vers.get()
        if 'nuix' in version.lower():
            messagebox.showinfo("ERROR", "Nuix is not supported for combining X-Ways cases!")
            xComb.set(0)
            selectImagesButton.config(state=NORMAL)
            imageList.config(state=NORMAL)
            imageList.delete('1.0', END)
            imageList.config(state=DISABLED)
            compCheck.config(state=NORMAL)
            return
        global images
        images = []
        cases = []
        myPath = caseSaveText.get()
        for cRoot, directories, files in os.walk(myPath, topdown=False):
            for name in files:
                if '.xfc' in name[-4:]:
                    cases.append(convertPath(os.path.join(cRoot, name)))

        selectImagesButton.config(state=DISABLED)
        imageFolderText.config(state=NORMAL)
        imageFolderText.delete(0, END)
        imageFolderText.config(state=DISABLED)
        compoundCaseName.config(state=NORMAL)
        imageList.config(state=NORMAL)
        imageList.delete('1.0', END)
        for x in cases:
            imageList.insert(END, x + '\n')
        imageList.config(state=DISABLED)


# Run Automation
@traced
def run():
    def __init__(self):
        self.__log.info("initialized")
    global xInstalls
    global xVersions
    global xCFG
    path = ''
    if dtMode.get() == 1:
        if imageFolderText.get() == '' or caseSaveText.get() == '':
            messagebox.showerror("ERROR", "Ensure image path and case path are selected")
            return
        else:
            dualTool(caseSaveText.get(),imageFolderText.get(),xInstalls,xVersions,xCFG, folderSkip)
            clearAll()
            return

    if 'Check scan drive' in vers.get():
        messagebox.showerror("ERROR", "Processing tools not found")
        return
    version = vers.get()
    if 'x-ways' in version.lower():
        tool = 'xways'
    else:
        tool = 'nuix'

    if tool == 'xways':
        vidpid =[]
        wmi = win32com.client.GetObject("winmgmts:")
        for usb in wmi.InstancesOF("win32_usbcontrollerdevice"):
            if "VID_096E"  in usb.Dependent:
                vidpid.append(usb)
        if len(vidpid) == 0:
            MsgBox = tk.messagebox.askquestion('Possible missing dongle', 'AutoF could not detect a '
                                                'license dongle, do you wish to continue? ',
                                                icon='warning')
            if MsgBox == 'no':
                return
    else:
        sconn = sqlite3.connect('settings\\settings.db ')
        scur = sconn.cursor()
        scur.execute("Select NuixLicense FROM Settings")
        sconn.commit()
        nuixLicenseSetting = scur.fetchall()
        if 'dongle' in nuixLicenseSetting[0][0]:
            drps = psutil.disk_partitions()
            drives = [dp.device for dp in drps if dp.fstype == 'FAT']
            nuixDongle = []
            for i in drives:
                nuixLicense = Path(i + 'licence.dat')
                if nuixLicense.is_file():
                    nuixDongle.append(nuixLicense)

            if len(nuixDongle) == 0:
                MsgBox = tk.messagebox.askquestion('Possible missing dongle', 'AutoF could not detect a '
                                                                              'license dongle, do you wish to continue? ',
                                                   icon='warning')
                if MsgBox == 'no':
                    return
    if caseSaveText.get() == '':
        messagebox.showerror("ERROR", "Select case save path")
        return
    if imageFolderText.get() == '' and cMode.get() == 0 and xComb.get() == 0:
        messagebox.showerror("ERROR", "Select images")
        return
    if compoundCaseName.get() == '' and compound.get() == 1:
        messagebox.showerror("ERROR", "Insert compound name")
        return
    if xComb.get() == 1:
        if compoundCaseName.get() == '':
            messagebox.showerror("ERROR", "Insert Master name in Compound field")

        else:
            for x in range(len(xVersions)):
                if str(xVersions[x]) == version:
                    path = xInstalls[x]
            cases = []
            myPath = caseSaveText.get()
            for fRoot, directories, files in os.walk(myPath, topdown=False):
                for name in files:
                    if '.xfc' in name[-4:]:
                        cases.append(convertPath(os.path.join(fRoot, name)))
            xCombine(path, cases, compoundCaseName.get(), caseSaveText.get())

        clearAll()
        return
    profile = prof.get()
    # Goes through version list and matches to select the version selected
    if nMode.get() == 0:

        for x in range(len(xVersions)):
            if str(xVersions[x]) == version:
                path = xInstalls[x]

        if 'xwforensics' in path.lower():

            for file in xCFG:
                try:
                    copyfile('Settings\\X-ways profiles\\Concurrent.dlg', os.path.dirname(file[0]) + '\\Concurrent.dlg')
                    copyfile('Settings\\X-ways profiles\\' + profile, file[0])
                except:
                    messagebox.showinfo("ERROR", "CFG failed to copy, selected profile not used.")

    # If case mode run in said mode
    if cMode.get() == 1:
        MsgBox = tk.messagebox.askquestion('Run over cases', 'You are about to run the selected '
                                                             'config over all cases selected. '
                                                             'Are you sure?',
                                           icon='warning')
        if MsgBox == 'yes':
            cases = []
            myPath = caseSaveText.get()
            for fRoot, directories, files in os.walk(myPath, topdown=False):
                for name in files:
                    if '.xfc' in name[-4:]:
                        cases.append(convertPath(os.path.join(fRoot, name)))

                window.withdraw()
                caseMode(path, cases, caseSaveText.get())
                window.deiconify()

        else:
            return
    # Check if running in node mode
    elif nMode.get() == 1:
        if compound.get() == 0:
            saveLocation = caseSaveText.get()
            if saveLocation == '':
                messagebox.showinfo("ERROR", "No case save location selected")
                return None
            elif len(images) == 0:
                messagebox.showinfo("ERROR", "No images selected")
            xnodeMode(tool, 'individual', 0, images, caseSaveText.get(), 0, profile)
        else:
            saveLocation = caseSaveText.get()
            if saveLocation == '':
                messagebox.showinfo("ERROR", "No case save location selected")
                return None
            elif compoundCaseName.get() == '':
                messagebox.showinfo("ERROR", "No case Name input")
                return None
            elif len(images) == 0:
                messagebox.showinfo("ERROR", "No images selected")
                return None
            elif len(images) == 1:
                messagebox.showinfo("ERROR", "Compound selected with only 1 image")
                return None
            xnodeMode(tool, 'compound', 0, images, caseSaveText.get(), compoundCaseName.get(), profile)

    # Check if compound, then run images individually
    elif compound.get() == 0:

        window.withdraw()
        if 'xwforensics' in path.lower():

            if xConc.get() ==1:
                xConcurrent(path, images,caseSaveText.get(), threadCountSet.get())
            else:
                processImages(path, images, caseSaveText.get(), 2)
        elif 'nuix' in path.lower():
            if xConc.get() == 1:
                nConcurrent(path, images, caseSaveText.get(), profile, threadCountSet.get())
            else:
                processImagesN(path, images, caseSaveText.get(), profile, 2)
        window.deiconify()
    # Runs compound mode
    else:
        window.withdraw()
        if 'x-ways' in path.lower():
            xCompound(path, images, caseSaveText.get(), compoundCaseName.get(),2)
        elif 'nuix' in path.lower():
            nCompound(path, images, caseSaveText.get(), profile, compoundCaseName.get(),2)
        window.deiconify()
    clearAll()


# Stops if not running as admin
if not isAdmin():
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror('Error!',
                         'You must run as Administrator')
    sys.exit(1)


# Checks for settings.db creates one if missing
settingsDbCheck = os.path.exists('Settings\\settings.db')
if settingsDbCheck == False:
    create_settings()


# scans for X-Ways
xInstalls, xVersions, xCFG = getXways()

# Image list place holder
images = []
savedPath = ''
conn = sqlite3.connect('settings\\settings.db ')
cur = conn.cursor()
cur.execute("SELECT * FROM Skip")
rows = cur.fetchall()
folderSkip = []
for i in rows:
    folderSkip.append(i[0])

# Main window
window = Tk()
window.title("AutoF")
window.geometry("800x300")
window.resizable(width=False, height=False)
try:
    window.iconbitmap('settings\\ax.ico')
except:
    window.withdraw()
    messagebox.showerror('Error!',
                         'Can not find AutoF.ico file. Perhaps the install is not complete')
    window.deiconify()


# Menu bar
menuBar = Menu(window)
fileMenu = Menu(window, tearoff=0)
fileMenu.add_command(label="Exit", command=exitAF, accelerator='Ctrl+Q')
menuBar.add_cascade(label="File", menu=fileMenu)
settingsMenu = Menu(window, tearoff=False)
settingsMenu.add_command(label="Force scan", command=forceScan, accelerator="Ctrl+F")
settingsMenu.add_command(label="Folder skip", command=folderSkipWindow, accelerator="Ctrl+S")
settingsMenu.add_command(label="Node config", command=jenkinsSettingsWindow, accelerator="Ctrl+N")
settingsMenu.add_command(label="General options", command=generalOptionsWindow, accelerator="Ctrl+G")
menuBar.add_cascade(label="Settings", menu=settingsMenu)
toolMenu = Menu(menuBar, tearoff=0)
toolMenu.add_command(label="Nuix Repath", command=repath, accelerator="Ctrl+R")
toolMenu.add_command(label="Case Info", command=caseInfo, accelerator="Ctrl+I")
menuBar.add_cascade(label="Tools", menu=toolMenu)
helpMenu = Menu(menuBar, tearoff=0)
helpMenu.add_command(label="Help Index", command=indexWindow, accelerator="Ctrl+H")
helpMenu.add_command(label="About...", command=aboutWindow, accelerator="Ctrl+I")
menuBar.add_cascade(label="Help", menu=helpMenu)


window.config(menu=menuBar)
settingsMenu.bind_all("<Control-q>", exitAF)
settingsMenu.bind_all("<Control-f>", forceScan)
settingsMenu.bind_all("<Control-s>", folderSkipWindow)
settingsMenu.bind_all("<Control-n>", jenkinsSettingsWindow)
settingsMenu.bind_all("<Control-g>", generalOptionsWindow)
settingsMenu.bind_all("<Control-h>", indexWindow)
settingsMenu.bind_all("<Control-i>", aboutWindow)
settingsMenu.bind_all("<Control-r>", repath)
settingsMenu.bind_all("<Control-i>", caseInfo)

# Image selection
Label(window, text="Image folder path:").place(x=25, y=20)
imageFolderText = Entry(window, width=20, bg="white", state=DISABLED)
imageFolderText.place(x=30, y=40)
selectImagesButton = Button(window, text="Select Images", command=imageSelect, state=tk.NORMAL)
selectImagesButton.place(x=30, y=65)

# Image Monitor
iMonitor = tk.IntVar()
iMonitorCheck = Checkbutton(window, text="Image Monitor", variable=iMonitor, onvalue=1, offvalue=0,
                            command=imageMonitorBox)
# iMonitorCheck.place(x=25, y=90)

# Image List
imageList = scrolledtext.ScrolledText(window, width=45, height=12, state=DISABLED, bg="lightgrey", wrap=WORD,
                                      font="calibre 8")
imageList.place(x=475, y=40)

# Case save location
Label(window, text="Case save location:").place(x=200, y=20)
caseSaveText = Entry(window, width=40, bg="white")
caseSaveText.place(x=205, y=40)
caseSaveButton = Button(window, text="Select save", command=caseSaveLocation)
caseSaveButton.place(x=205, y=65)

# Compound
compound = tk.IntVar()
compCheck = Checkbutton(window, text="One Case Only", variable=compound, onvalue=1, offvalue=0, command=compoundBox)
compCheck.place(x=335, y=59)
Label(window, text="Single Case Name:").place(x=195, y=100)
compoundCaseName = Entry(window, width=20, bg="white", state=DISABLED)
compoundCaseName.place(x=200, y=125)

# Profile select and Version select
vers = StringVar(window)
vers.set(xVersions[0])
prof = StringVar(window)
xProfiles = '0'

profOption = OptionMenu(window, prof, *xProfiles)
xProfile(profOption)
Label(window, text="Profile selection:").place(x=25, y=115)
profOption.place(x=30, y=135)
Label(window, text="Processing tool:").place(x=25, y=170)
versOption = OptionMenu(window, vers, *xVersions, command=xProfile)
versOption.place(x=30, y=190)

# Case mode
cMode = tk.IntVar()
cModeCheck = Checkbutton(window, text="Case mode", variable=cMode, onvalue=1, offvalue=0, command=caseModeBox)
cModeCheck.place(x=335, y=79)

# Node mode
nMode = tk.IntVar()
nModeCheck = Checkbutton(window, text="Node mode", variable=nMode, onvalue=1, offvalue=0, command=nodeModeBox)
nModeCheck.place(x=335, y=99)

# XCombine
xComb = tk.IntVar()
xCombCheck = Checkbutton(window, text="xCombine", variable=xComb, onvalue=1, offvalue=0, command=xCombineBox)
xCombCheck .place(x=335, y=119)

# UFDR Filter
ufdrFilter = tk.IntVar()
ufdrFilterCheck = Checkbutton(window, text="UFDR", variable=ufdrFilter, onvalue=1, offvalue=0, command=ufdrFilterBox)
ufdrFilterCheck.place(x=335, y=139)

# Dual Tool Mode
dtMode = tk.IntVar()
dtModeCheck = Checkbutton(window, text="Dual tool", variable=dtMode, onvalue=1, offvalue=0, command=dtBox)
dtModeCheck.place(x=335, y=159)

# Concurrent mode
xConc = tk.IntVar()
xConcCheck = Checkbutton(window, text="Concurrent", variable=xConc, onvalue=1, offvalue=0, command=concurrentBox)
xConcCheck.place(x=335, y=179)
threadCount = [2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32]
threadCountSet = StringVar(window)
threadCountSet.set(threadCount[0])
threadMenu= OptionMenu(window, threadCountSet, *threadCount)
threadMenu.config(state="disabled")
threadMenu.place(x=335, y=199)

# exit and run buttons
exitButton = Button(window, text="Exit", fg="red", command=exitAF)
exitButton.place(x=25, y=235)
clearButton = Button(window, text="Clear", fg="blue", command=clearAll)
clearButton.place(x=690, y=235)
window.bind("<Control-w>", clearAll)
runButton = Button(window, text='Run', fg="green", command=run)
runButton.place(x=735, y=235)

window.mainloop()
