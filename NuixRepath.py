# Re-paths Nuix cases
import os
from datetime import datetime
import shutil
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import logging
import re
from autologging import traced
from tkinter.ttk import Progressbar
import webbrowser


# Date and time
@traced
def now():
    rightNow = datetime.now()
    timeNow = rightNow.strftime("%d-%m-%Y %H-%M-%S")
    return timeNow


@traced
def repath(event=None):
    @traced
    def exitNR():
        windowRepath.destroy()

    @traced
    def dirSelect():
        myPath = filedialog.askdirectory(title="Select operation folder")
        dirFolderText.config(state=NORMAL)
        dirFolderText.delete(0, END)
        dirFolderText.insert(0, myPath)
        dirFolderText.config(state=DISABLED)

    @traced
    def dirImageSelect():
        imagePath = filedialog.askdirectory(title="Select Image folder")
        altImageText.config(state=NORMAL)
        altImageText.delete(0, END)
        altImageText.insert(0, imagePath)
        altImageText.config(state=DISABLED)

    # converts path for Windows COMPLETE

    def convertPath(path):
        return path.replace('/', '\\')

    @traced
    def altImageBox():
        if altImageButton["state"] == NORMAL:
            altImageText.config(state=NORMAL)
            altImageText.delete(0, END)
            altImageText.config(state=DISABLED)
            altImageButton["state"] = DISABLED
        else:
            altImageButton["state"] = NORMAL

    def filterBox():
        if filter.get() == 1:
            filterText.config(state=NORMAL)
            filterOption.config(state="normal")
        else:
            filterText.config(state=DISABLED)
            filterOption.config(state="disabled")
    @traced
    def run():
        myPath = dirFolderText.get()
        if myPath == '':
            messagebox.showerror('Error!',
                                 'Operation root not selected!')
            return
        if filter.get() == 1 and filterText.get() != '':
            filterName = filterText.get().lower()
            filterCondition = filterOptions.get()
        elif filter.get() == 1:
            messagebox.showerror('Error!',
                                 'Filter selected but is empty!')
            return
        else:
            filterCondition = 0
        runButton.config(state=DISABLED)
        logger = logging.getLogger('NuixRe-path')
        logger.setLevel(logging.DEBUG)
        progress = Progressbar(windowRepath, orient=HORIZONTAL, length=220, mode='indeterminate')
        progress.place(x=90, y=140)
        allFiles = []
        nxml = []
        compound = []
        compoundConfirmed =[]
        imagesFound = []
        acutualCaseFiles = []

        # create file handler which logs even debug messages
        log = myPath + '\\Re-Path ' + now() + '.html'
        fh = logging.FileHandler(log)
        fh.setLevel(logging.DEBUG)
        logger.addHandler(fh)
        logger.info('<!DOCTYPE html>')
        logger.info('<html>')
        logger.info('<body>')
        logger.info('<p>------------------------------------------</p>')
        logger.info('<p>Replacements</p>')
        logger.info('<p>------------------------------------------</p>')
        # stores all files in list
        progress.start()
        if altImageButton["state"] == NORMAL and altImageText.get() != "":
            for iRoot, directories, files in os.walk(altImageText.get(), topdown=False):
                windowRepath.update()
                for file in files:
                    windowRepath.update()
                    allFiles.append(convertPath(iRoot) + '\\' + file)
        elif altImageButton["state"] == NORMAL and altImageText.get() == "":
            messagebox.showinfo("ERROR", "Alt Image ticked but not folder selected")
            return
        else:
            for iRoot, directories, files in os.walk(myPath, topdown=False):
                windowRepath.update()
                for file in files:
                    windowRepath.update()
                    allFiles.append(convertPath(iRoot) + '\\' + file)

        # Finds all xml, these contain the evidence locations
        for iRoot, directories, files in os.walk(myPath, topdown=False):
            windowRepath.update()
            for name in files:
                windowRepath.update()
                if '.xml' in name[-4:] and 'Evidence' in iRoot:
                    nxml.append(convertPath(os.path.join(iRoot, name)))
                elif 'case.fbi2' in name and '$RECYCLE.BIN' not in iRoot:
                    compound.append(convertPath(os.path.join(iRoot, name)))
        if len(compound) > 0:
            for caseFile in compound:
                cLog = 'false'
                f = open(caseFile, 'r')
                for line in f:
                    if '<caseType>COMPOUND</caseType>' in line:
                        cLog = 'true'
                f.close()
                if cLog == 'true':
                    compoundConfirmed.append(caseFile)

        # Sanitises list to ensure only nuix evidence files exist
        count = 0
        for i in nxml:
            windowRepath.update()
            nLog = 'false'
            f = open(i, 'r')
            for line in f:
                windowRepath.update()
                if 'evidence xmlns="http://nuix.com/fbi/evidence"' in line:
                    nLog = 'true'
            if nLog == 'false':
                nxml.pop(count)
            count = count + 1

        for i in nxml:
            windowRepath.update()
            found = 'false'
            f = open(i, 'r')
            rootDir = os.path.dirname(i)
            shutil.copy(i, rootDir + '\\' + os.path.basename(i)[:-4] + ' OLD ' + now())
            for line in f:
                windowRepath.update()
                if 'file location' in line:
                    # REGEX that finds everything between "" in a string that contains the above 'file location'
                    pattern = '"(.*?)"'
                    file = re.search(pattern, line).group(1)


                    if os.path.isfile(file) and filter.get() == 0:
                        logger.info('<p><a href="file:///' + os.path.dirname(file) + '">' + file + '</a>' +
                                ' Exists in correct location.' + '</p>')
                        found = 'true'
                    elif os.path.isfile(file) and (filterCondition == "Contains" and filterName in file.lower()):
                        logger.info('<p><a href="file:///' + os.path.dirname(file) + '">' + file + '</a>' +
                                ' Exists in correct location.' + '</p>')
                        found = 'true'
                    elif os.path.isfile(file) and (filterCondition == "Does not contain" and filterName not in file.lower()):
                        logger.info('<p><a href="file:///' + os.path.dirname(file) + '">' + file + '</a>' +
                                ' Exists in correct location.' + '</p>')
                        found = 'true'
                    else:

                        for name in allFiles:
                            windowRepath.update()
                            if os.path.basename(file).endswith(os.path.basename(name)) and filter.get() == 0:
                                imagesFound.append(convertPath(name))
                                fileIn = open(i, 'rt')
                                data = fileIn.read()
                                data = data.replace(file, os.path.join(name))
                                fileIn.close()
                                # Makes copy of xml before overwriting it
                                fileIn = open(i, 'wt')
                                fileIn.write(data)
                                fileIn.close()
                                logger.info('<p>evidence replaced in ' + '<a href="file:///' + os.path.dirname(i) + '">'
                                            + i + '</a></p>')
                                found = 'true'
                            elif os.path.basename(file).endswith(os.path.basename(name)) and filterCondition == "Contains" and filterName in name.lower():
                                imagesFound.append(convertPath(name))
                                fileIn = open(i, 'rt')
                                data = fileIn.read()
                                data = data.replace(file, os.path.join(name))
                                fileIn.close()
                                # Makes copy of xml before overwriting it
                                fileIn = open(i, 'wt')
                                fileIn.write(data)
                                fileIn.close()
                                logger.info('<p>evidence replaced in ' + '<a href="file:///' + os.path.dirname(i) + '">'
                                            + i + '</a></p>')
                                found = 'true'
                            elif os.path.basename(file).endswith(os.path.basename(name)) and filterCondition == "Does not contain" and filterName not in name.lower():
                                imagesFound.append(convertPath(name))
                                fileIn = open(i, 'rt')
                                data = fileIn.read()
                                data = data.replace(file, os.path.join(name))
                                fileIn.close()
                                # Makes copy of xml before overwriting it
                                fileIn = open(i, 'wt')
                                fileIn.write(data)
                                fileIn.close()
                                logger.info('<p>evidence replaced in ' + '<a href="file:///' + os.path.dirname(i) + '">'
                                            + i + '</a></p>')
                                found = 'true'
            if found == 'false':
                logger.error('<p></p>')
                logger.error('<p>' + ' Image for ' + '<a href="file:///' + os.path.dirname(i) + '">' + i + '</a> NOT FOUND</p>')
                logger.error('<p></p>')

        logger.info('<p>------------------------------------------</p>')
        logger.info('<p>Cases Found</p>')
        logger.info('<p>------------------------------------------</p>')
        for i in nxml:
            logger.info('<p><a href="file:///' + os.path.dirname(i) + '">' + i + '</a></p>')
        logger.info('<p>------------------------------------------</p>')
        logger.info('<p>Images Found</p>')
        logger.info('<p>------------------------------------------</p>')
        if len(imagesFound) == 0 and imagesFound == 'true':
            logger.info('<p>Images not searched for.</p>')
        else:
            for i in imagesFound:
                logger.info('<p><a href="file:///' + os.path.dirname(i) + '">' + i + '</a></p>')

        #Compounds
        logger.info('<p>------------------------------------------</p>')
        logger.info('<p>Compound Cases</p>')
        logger.info('<p>------------------------------------------</p>')
        for cases in compoundConfirmed:
            rootDir = os.path.dirname(cases)
            shutil.copy(cases, rootDir + '\\' + os.path.basename(cases)[:-4] + ' OLD ' + now())
            subcases = []
            allFiles = []
            case2 = []
            with open(cases, 'r') as file:
                for line in file:
                    if '<subcase location=' in line:
                        path = line.replace('    <subcase location="', '')
                        path = path.replace('" />', '')
                        subcases.append(path)
            for iRoot, directories, files in os.walk('E:\\', topdown=False):
                for file in files:
                    allFiles.append(convertPath(iRoot) + '\\' + file)

            for file in allFiles:
                if 'case.fbi2' in file:
                    case2.append(file)
            if filterCondition == 0:
                for case in subcases:
                    found = 'false'
                    newFile = []
                    afile = os.path.abspath(case.strip()) + r'\case.fbi2'
                    # for relative paths
                    if os.path.isabs(case) == False:
                        os.chdir(os.path.dirname(cases))

                        if os.path.isfile(afile):
                            logger.info('<p>Case Location correct ' + '<a href="file:///' + os.path.dirname(cases) + '">'
                                        + cases + '</a> for compound ' + cases + '</p>')
                            found = 'true'
                        else:

                            for i in case2:
                                if os.path.basename(os.path.dirname(afile)) + '\\' + os.path.basename(
                                        afile) in i and '$RECYCLE.BIN' not in i:
                                    newFile.append(os.path.dirname(i))
                            if len(newFile) > 1:
                                logger.info(
                                    '<p>More than 1 possible case location  ' + '<a href="file:///' + os.path.dirname(
                                        case) + '">'
                                    + case + '</a></p>')
                                found = 'false'
                            elif len(newFile) == 0:
                                found = 'false'
                            else:
                                fileIn = open(cases, 'rt')
                                data = fileIn.read()
                                data = data.replace(case.strip(), newFile[0])
                                fileIn.close()
                                # Makes copy of xml before overwriting it
                                fileIn = open(cases, 'wt')
                                fileIn.write(data)
                                fileIn.close()
                                logger.info('<p>evidence replaced in ' + '<a href="file:///' + os.path.dirname(case) + '">'
                                 + case + '</a> for compound ' + cases + '</p>')
                                found = 'true'
                    # For absolute paths
                    else:
                        if os.path.isfile(afile):
                            logger.info('<p>Case Location correct ' + '<a href="file:///' + os.path.dirname(case) + '">'
                                        + case + '</a> for compound ' + cases + '</p>')
                            found = 'true'
                        else:
                            for i in case2:
                                if os.path.basename(os.path.dirname(afile)) + '\\' + os.path.basename(
                                        afile) in i and '$RECYCLE.BIN' not in i:
                                    newFile.append(os.path.dirname(i))
                            if len(newFile) > 1:
                                logger.info('<p>More than 1 possible case location  ' + '<a href="file:///' + os.path.dirname(case) + '">'
                                            + case + '</a></p>')
                                found = 'false'
                            elif len(newFile) == 0:
                                found = 'false'
                            else:
                                fileIn = open(cases, 'rt')
                                data = fileIn.read()
                                data = data.replace(case.strip(), newFile[0])
                                fileIn.close()
                                # Makes copy of xml before overwriting it
                                fileIn = open(cases, 'wt')
                                fileIn.write(data)
                                fileIn.close()
                                logger.info('<p>evidence replaced in ' + '<a href="file:///' + os.path.dirname(case) + '">'
                                            + case + '</a> for compound ' + cases + '</p>')
                                found = 'true'
                    if found == 'false':
                        logger.error('<p></p>')
                        logger.error('<p>' + ' SubCase ' + '<a href="file:///' + os.path.dirname(
                            case) + '">' + case + '</a> for compound ' + cases + ' NOT FOUND</p>')
                        logger.error('<p></p>')
            elif filterCondition == "Contains":
                windowRepath.update()
                condition = filterName
                for case in subcases:
                    windowRepath.update()
                    found = 'false'
                    newFile = []
                    afile = os.path.abspath(case.strip()) + r'\case.fbi2'
                    # for relative paths
                    if os.path.isabs(case) == False:
                        os.chdir(os.path.dirname(cases))

                        if os.path.isfile(afile) and condition in afile.lower():
                            logger.info(
                                '<p>Case Location correct ' + '<a href="file:///' + os.path.dirname(cases) + '">'
                                + cases + '</a> for compound ' + cases + '</p>')
                            found = 'true'
                        else:

                            for i in case2:
                                if os.path.basename(os.path.dirname(afile)) + '\\' + os.path.basename(
                                        afile) in i and '$RECYCLE.BIN' not in i and condition in afile.lower():
                                    newFile.append(os.path.dirname(i))
                            if len(newFile) > 1:
                                logger.info(
                                    '<p>More than 1 possible case location  ' + '<a href="file:///' + os.path.dirname(
                                        case) + '">'
                                    + case + '</a></p>')
                                found = 'false'
                            elif len(newFile) == 0:
                                found = 'false'
                            else:
                                fileIn = open(cases, 'rt')
                                data = fileIn.read()
                                data = data.replace(case.strip(), newFile[0])
                                fileIn.close()
                                # Makes copy of xml before overwriting it
                                fileIn = open(cases, 'wt')
                                fileIn.write(data)
                                fileIn.close()
                                logger.info(
                                    '<p>evidence replaced in ' + '<a href="file:///' + os.path.dirname(case) + '">'
                                    + case + '</a> for compound ' + cases + '</p>')
                                found = 'true'
                    # For absolute paths
                    else:
                        if os.path.isfile(afile) and condition in afile.lower():
                            logger.info('<p>Case Location correct ' + '<a href="file:///' + os.path.dirname(case) + '">'
                                        + case + '</a> for compound ' + cases + '</p>')
                            found = 'true'
                        else:
                            for i in case2:
                                if os.path.basename(os.path.dirname(afile)) + '\\' + os.path.basename(
                                        afile) in i and '$RECYCLE.BIN' not in i and condition in afile.lower():
                                    newFile.append(os.path.dirname(i))
                            if len(newFile) > 1:
                                logger.info(
                                    '<p>More than 1 possible case location  ' + '<a href="file:///' + os.path.dirname(
                                        case) + '">'
                                    + case + '</a></p>')
                                found = 'false'
                            elif len(newFile) == 0:
                                found = 'false'
                            else:
                                fileIn = open(cases, 'rt')
                                data = fileIn.read()
                                data = data.replace(case.strip(), newFile[0])
                                fileIn.close()
                                # Makes copy of xml before overwriting it
                                fileIn = open(cases, 'wt')
                                fileIn.write(data)
                                fileIn.close()
                                logger.info(
                                    '<p>evidence replaced in ' + '<a href="file:///' + os.path.dirname(case) + '">'
                                    + case + '</a> for compound ' + cases + '</p>')
                                found = 'true'
                    if found == 'false':
                        logger.error('<p></p>')
                        logger.error('<p>' + ' SubCase ' + '<a href="file:///' + os.path.dirname(
                            case) + '">' + case + '</a> for compound ' + cases + ' NOT FOUND</p>')
                        logger.error('<p></p>')
            elif filterCondition == "Does not contain":
                windowRepath.update()
                condition = filterName
                for case in subcases:
                    found = 'false'
                    newFile = []
                    afile = os.path.abspath(case.strip()) + r'\case.fbi2'
                    # for relative paths
                    if os.path.isabs(case) == False:
                        os.chdir(os.path.dirname(cases))

                        if os.path.isfile(afile) and condition not in afile.lower():
                            logger.info(
                                '<p>Case Location correct ' + '<a href="file:///' + os.path.dirname(cases) + '">'
                                + cases + '</a> for compound ' + cases + '</p>')
                            found = 'true'
                        else:

                            for i in case2:
                                if os.path.basename(os.path.dirname(afile)) + '\\' + os.path.basename(
                                        afile) in i and '$RECYCLE.BIN' not in i and condition not in afile.lower():
                                    newFile.append(os.path.dirname(i))
                            if len(newFile) > 1:
                                logger.info(
                                    '<p>More than 1 possible case location  ' + '<a href="file:///' + os.path.dirname(
                                        case) + '">'
                                    + case + '</a></p>')
                                found = 'false'
                            elif len(newFile) == 0:
                                found = 'false'
                            else:
                                fileIn = open(cases, 'rt')
                                data = fileIn.read()
                                data = data.replace(case.strip(), newFile[0])
                                fileIn.close()
                                # Makes copy of xml before overwriting it
                                fileIn = open(cases, 'wt')
                                fileIn.write(data)
                                fileIn.close()
                                logger.info(
                                    '<p>evidence replaced in ' + '<a href="file:///' + os.path.dirname(case) + '">'
                                    + case + '</a> for compound ' + cases + '</p>')
                                found = 'true'
                    # For absolute paths
                    else:
                        if os.path.isfile(afile) and condition not in afile.lower():
                            logger.info('<p>Case Location correct ' + '<a href="file:///' + os.path.dirname(case) + '">'
                                        + case + '</a> for compound ' + cases + '</p>')
                            found = 'true'
                        else:
                            for i in case2:
                                if os.path.basename(os.path.dirname(afile)) + '\\' + os.path.basename(
                                        afile) in i and '$RECYCLE.BIN' not in i and condition not in afile.lower():
                                    newFile.append(os.path.dirname(i))
                            if len(newFile) > 1:
                                logger.info(
                                    '<p>More than 1 possible case location  ' + '<a href="file:///' + os.path.dirname(
                                        case) + '">'
                                    + case + '</a></p>')
                                found = 'false'
                            elif len(newFile) == 0:
                                found = 'false'
                            else:
                                fileIn = open(cases, 'rt')
                                data = fileIn.read()
                                data = data.replace(case.strip(), newFile[0])
                                fileIn.close()
                                # Makes copy of xml before overwriting it
                                fileIn = open(cases, 'wt')
                                fileIn.write(data)
                                fileIn.close()
                                logger.info(
                                    '<p>evidence replaced in ' + '<a href="file:///' + os.path.dirname(case) + '">'
                                    + case + '</a> for compound ' + cases + '</p>')
                                found = 'true'
                    if found == 'false':
                        logger.error('<p></p>')
                        logger.error('<p>' + ' SubCase ' + '<a href="file:///' + os.path.dirname(
                            case) + '">' + case + '</a> for compound ' + cases + ' NOT FOUND</p>')
                        logger.error('<p></p>')
        progress.stop()
        messagebox.showinfo("Complete", "Re-pathing complete.")
        webbrowser.open('file:///' + log, new=0)
        fh.close()
        progress.destroy()
        runButton.config(state=NORMAL)

    # Main window
    windowRepath = Toplevel()
    windowRepath.title("Nuix RePath")
    windowRepath.geometry("405x175")
    windowRepath.iconbitmap('settings\\ax.ico')
    windowRepath.resizable(width=False, height=False)
    windowRepath.lift()
    windowRepath.attributes('-topmost', True)
    windowRepath.grab_set()

    # Operation Selection
    dirFolderText = Entry(windowRepath, width=40, bg="white", state=DISABLED)
    dirFolderText.place(x=15, y=25)
    dirImagesButton = Button(windowRepath, text="Select Root Folder", command=dirSelect, state=tk.NORMAL)
    dirImagesButton.place(x=270, y=22)

    # Image Path selection

    altImageCheck = Checkbutton(windowRepath, text="Alternate Image Path", command=altImageBox)
    altImageCheck.place(x=12, y=0)
    altImageText = Entry(windowRepath, width=40, bg="white", state=DISABLED)
    altImageText.place(x=15, y=65)
    altImageButton = Button(windowRepath, text="Select Image Folder", command=dirImageSelect, state=DISABLED)
    altImageButton.place(x=270, y=62)

    # Filter
    options =['Contains', 'Does not contain']
    filterOptions = StringVar()
    filterOptions.set(options[0])
    filter = tk.IntVar()
    filterCheck = Checkbutton(windowRepath,variable=filter, text="Filter", command=filterBox, onvalue=1, offvalue=0,)
    filterCheck.place(x=152, y=0)
    filterText = Entry(windowRepath, width=40, bg="white", state=DISABLED)
    filterText.place(x=15, y=105)
    filterOption = OptionMenu(windowRepath,filterOptions,*options)
    filterOption.place(x=267, y=95)
    filterOption.config(state="disabled")

    # Run button

    runButton = Button(windowRepath, text='Run', fg="green", command=run)
    runButton.place(x=350, y=140)
    exitButton = Button(windowRepath, text="Exit", fg="red", command=exitNR)
    exitButton.place(x=25, y=140)
    windowRepath.mainloop()
