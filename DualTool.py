# AutoF dual tool mode
import os
from shutil import copyfile
from datetime import datetime
import tkinter as tk
from tkinter import *
from autologging import traced
from AutoX import processImages, xCompound
from AutoS import imageXSort
from AutoN import processImagesN, nCompound
from tkinter import messagebox
import win32com.client
import psutil
import sqlite3
from pathlib import Path

# Date and time
@traced
def now():
    rightNow = datetime.now()
    timeNow = rightNow.strftime("%d-%m-%Y %H-%M-%S")
    return timeNow


def dualTool(casePath, imagePath, xInstalls, xVersions, xCFG, folderSkip):
    def exitDT():
        windowDualTool.destroy()
        # Manages compound tick box behaviour COMPLETE
    @traced
    def compoundBox():
        if oneCase.get() == 1:
            compoundCaseName.config(state=NORMAL)

        elif oneCase.get() == 0:
            compoundCaseName.delete(0, END)
            compoundCaseName.config(state=DISABLED)

    def runDT():
        oneCaseName =''
        images1 = imageXSort(folderSkip, imagePath, toolOneVers.get(), ufdrFilter.get())
        images2 = imageXSort(folderSkip, imagePath, toolTwoVers.get(), ufdrFilter.get())
        vers1 = toolOneVers.get()
        vers2 = toolTwoVers.get()
        profile1 = toolOneProf.get()
        profile2 = toolTwoProf.get()
        # Dongle check
        missingDongle = False
        if oneCase.get() == 1:
            oneCaseName = compoundCaseName.get()
            if len(oneCaseName) == 0:
                messagebox.showerror("ERROR", "No case name")
                return
        if 'x-ways' in vers1.lower() or 'xways' in vers2.lower():
            vidpid = []
            wmi = win32com.client.GetObject("winmgmts:")
            for usb in wmi.InstancesOF("win32_usbcontrollerdevice"):
                if "VID_096E" in usb.Dependent:
                    vidpid.append(usb)
            if len(vidpid) == 0:
                missingDongle = True
        elif 'nuix' in vers1.lower() or 'nuix' in vers2.lower():
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
                    missingDongle = True

        if missingDongle == True:
            MsgBox = tk.messagebox.askquestion('Possible missing dongle', 'AutoF could not detect a '
                                                                          'license dongle, do you wish to continue? ',
                                               icon='warning')
            if MsgBox == 'no':
                return
        for x in range(len(xVersions)):
            if str(xVersions[x]) == vers1:
                path1 = xInstalls[x]

        for x in range(len(xVersions)):
            if str(xVersions[x]) == vers2:
                path2 = xInstalls[x]

        # Tool one
        if 'xwforensics' in path1.lower():
            casePathNew = os.path.join(casePath, vers1)
            try:
                os.mkdir(casePathNew)
            except OSError as error:
                print(error)
            for file in xCFG:
                try:
                    copyfile('Settings\\X-ways profiles\\' + profile1, file[0])
                except:
                    messagebox.showinfo("ERROR", "CFG failed to copy, selected profile not used.")

            if oneCase.get() == 1:
                xCompound(path1, images1, casePathNew, oneCaseName, 0)
            else:
                processImages(path1, images1, casePathNew, 0)
        else:
            casePathNew = os.path.join(casePath, vers1)
            try:
                os.mkdir(casePathNew)
            except OSError as error:
                print(error)
            if oneCase.get() == 1:
                nCompound(path1, images1, casePathNew, toolOneProf, oneCaseName, 0)
            else:
                processImagesN(path1, images1, casePathNew, toolOneProf, 0)

        # Tool two
        if 'xwforensics' in path2.lower():
            casePathNew = os.path.join(casePath, vers2)
            try:
                os.mkdir(casePathNew)
            except OSError as error:
                print(error)
            for file in xCFG:
                try:
                    copyfile('Settings\\X-ways profiles\\' + profile2, file[0])
                except:
                    messagebox.showinfo("ERROR", "CFG failed to copy, selected profile not used.")

            if oneCase.get() == 1:
                xCompound(path2, images2, casePathNew, oneCaseName, 2)
            else:
                processImages(path2, images2, casePathNew, 2)
        else:
            casePathNew = os.path.join(casePath, vers2)
            try:
                os.mkdir(casePathNew)
            except OSError as error:
                print(error)

            if oneCase.get() == 1:
                nCompound(path2, images2, casePathNew, toolTwoProf, oneCaseName, 2)
            else:
                processImagesN(path2, images2, casePathNew, toolTwoProf, 2)
    # Find x-ways profiles COMPLETE
    @traced
    def xProfileOne(self, toolOneVers):
        getxProfilesOne = []
        if 'X-ways' in toolOneVers.get():
            for i in os.listdir('Settings\\X-ways profiles\\'):
                if i.endswith('.cfg'):
                    getxProfilesOne.append(i)
            # getxProfiles = os.listdir('Settings\\X-ways profiles\\')
        else:
            getxProfilesOne = os.listdir('Settings\\Nuix\\Scripts\\')

        toolOneProf.set('')
        toolOneprofOption['menu'].delete(0, 'end')
        for opt in getxProfilesOne:
            toolOneprofOption['menu'].add_command(label=opt, command=tk._setit(toolOneProf, opt))
            toolOneProf.set(getxProfilesOne[0])

    # Find x-ways profiles COMPLETE
    @traced
    def xProfileTwo(self, toolTwoVers):
        getxProfilesTwo = []
        if 'X-ways' in toolTwoVers.get():
            for i in os.listdir('Settings\\X-ways profiles\\'):
                if i.endswith('.cfg'):
                    getxProfilesTwo.append(i)
        else:
            getxProfilesTwo = os.listdir('Settings\\Nuix\\Scripts\\')

        toolTwoProf.set('')
        toolTwoprofOption['menu'].delete(0, 'end')
        for opt in getxProfilesTwo:
            toolTwoprofOption['menu'].add_command(label=opt, command=tk._setit(toolTwoProf, opt))
            toolTwoProf.set(getxProfilesTwo[0])

    # Main window
    windowDualTool = Toplevel()
    windowDualTool.title("Dual Tool")
    windowDualTool.geometry("375x200")
    windowDualTool.iconbitmap('settings\\ax.ico')
    windowDualTool.resizable(width=False, height=False)
    windowDualTool.lift()
    windowDualTool.attributes('-topmost', True)
    windowDualTool.grab_set()

    # toolOne
    toolOneVers = StringVar(windowDualTool)
    toolOneVers.set(xVersions[0])
    toolOneProf = StringVar(windowDualTool)
    toolOnexProfiles = '0'
    toolOneprofOption = OptionMenu(windowDualTool, toolOneProf, *toolOnexProfiles)
    xProfileOne(toolOneprofOption,toolOneVers)
    Label(windowDualTool, text="Tool one profile selection:").place(x=25, y=15)
    toolOneprofOption.place(x=30, y=35)
    Label(windowDualTool, text="Tool one processing tool:").place(x=175, y=15)
    toolOneversOption = OptionMenu(windowDualTool, toolOneVers, *xVersions, command=lambda x:xProfileOne(toolOneprofOption,toolOneVers))
    toolOneversOption.place(x=180, y=35)

    # toolTwo
    toolTwoVers = StringVar(windowDualTool)
    toolTwoVers.set(xVersions[0])
    toolTwoProf = StringVar(windowDualTool)
    toolTwoxProfiles = '0'
    toolTwoprofOption = OptionMenu(windowDualTool, toolTwoProf, *toolTwoxProfiles)
    xProfileTwo(toolTwoprofOption, toolTwoVers)
    Label(windowDualTool, text="Tool two profile selection:").place(x=25, y=75)
    toolTwoprofOption.place(x=30, y=95)
    Label(windowDualTool, text="Tool two processing tool:").place(x=175, y=75)
    toolTwoversOption = OptionMenu(windowDualTool, toolTwoVers, *xVersions, command=lambda x:xProfileTwo(toolTwoprofOption, toolTwoVers))
    toolTwoversOption.place(x=180, y=95)

    # UFDR Filter
    ufdrFilter = tk.IntVar()
    ufdrFilterCheck = Checkbutton(windowDualTool, text="UFDR", variable=ufdrFilter, onvalue=1, offvalue=0)
    ufdrFilterCheck.place(x=25, y=125)

    # One Case
    oneCase = tk.IntVar()
    oneCaseCheck = Checkbutton(windowDualTool, text="One case", variable=oneCase, onvalue=1, offvalue=0, command=compoundBox)
    oneCaseCheck.place(x=85, y=125)
    compoundCaseName = Entry(windowDualTool, width=20, bg="white", state=DISABLED)
    compoundCaseName.place(x=175, y=129)

    # exit and run buttons
    exitButton = Button(windowDualTool, text="Exit", fg="red", command=exitDT)
    exitButton.place(x=25, y=160)
    runButton = Button(windowDualTool, text='Run', fg="green", command=runDT)
    runButton.place(x=305, y=160)
