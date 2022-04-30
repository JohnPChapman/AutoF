# Nuix Forensics case automater
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Progressbar
import subprocess
import os
import sqlite3
from AutoS import convertPath, now
from autologging import traced


# Process all images, individual cases by default
@traced
def processImagesN(path, images, caseSave, script):
    imagesWindow = Tk()
    imagesWindow.title("AutoF Nuix Image")
    imagesWindow.geometry("300x70")
    imagesWindow.resizable(width=False, height=False)
    imagesWindow.attributes('-disabled', True)
    progressDivide = 100 / len(images)
    Label(imagesWindow, text="Running Nuix in Image mode").place(x=25, y=5)
    progress = Progressbar(imagesWindow, orient=HORIZONTAL, length=250, mode='determinate')
    progress.place(x=25, y=35)

    if not caseSave:
        messagebox.showinfo("ERROR", "No case save location selected")
        return None
    elif len(images) == 0:
        messagebox.showinfo("ERROR", "No images selected")
        return None

    count = 0

    while count < len(images):
        sconn = sqlite3.connect('settings\\settings.db ')
        scur = sconn.cursor()
        scur.execute("Select NuixLicense FROM Settings")
        sconn.commit()
        nuixLicense = scur.fetchall()
        caseName = os.path.split(images[count])
        caseName = caseName[1]
        caseName = caseName.split(".")
        caseName = caseName[0]
        ct = now()
        cpath = caseSave + '/' + caseName
        newScript = caseSave + '/Nuix Scripts/' + str(caseName) + ".rb"
        if os.path.exists(newScript):
            newScript = caseSave + '/Nuix Scripts/' + str(caseName) + " " + ct + ".rb"
        if os.path.exists(cpath):
            cpath = cpath + " " + ct
        if not os.path.exists(caseSave + '/Nuix Scripts/'):
            os.mkdir(caseSave + '/Nuix Scripts/')
        fin = open("Settings/Nuix/Scripts/" + script)
        fout = open(convertPath(newScript), "w+")

        for line in fin:
            if 'AUTOFCASEPATH' in line:
                fout.write(line.replace('AUTOFCASEPATH', str(cpath)))
            elif 'CASENAME' in line:
                fout.write(line.replace('CASENAME', str(caseName)))
            elif 'AUTOFIMAGE' in line:
                image = images[count]
                imagePath = image.replace('\\', '/')
                fout.write(line.replace('AUTOFIMAGE', imagePath))
            else:
                fout.write(line)
        fin.close()
        fout.close()
        proc = subprocess.Popen(path + ' ' + nuixLicense[0][0] + ' "' + newScript + '"')

        count = count + 1
        while proc.poll() is None:
            imagesWindow.update()
        progress['value'] += progressDivide

    messagebox.showinfo("Complete", "Process complete.")
    imagesWindow.destroy()


# Process all images into a compound
@traced
def nCompound(path, images, caseSave, script, cName):
    sconn = sqlite3.connect('settings\\settings.db ')
    scur = sconn.cursor()
    scur.execute("Select NuixLicense FROM Settings")
    sconn.commit()
    nuixLicense = scur.fetchall()
    imagesWindow = Tk()
    imagesWindow.title("AutoF Nuix Image")
    imagesWindow.geometry("300x70")
    imagesWindow.resizable(width=False, height=False)
    imagesWindow.attributes('-disabled', True)
    Label(imagesWindow, text="Running Nuix in Single Case mode").place(x=25, y=5)
    progress = Progressbar(imagesWindow, orient=HORIZONTAL, length=250, mode='indeterminate')
    progress.place(x=25, y=35)

    if not caseSave:
        messagebox.showinfo("ERROR", "No case save location selected")
        return None
    elif len(images) == 0:
        messagebox.showinfo("ERROR", "No images selected")
        return None

    count = 0

    ct = now()
    cpath = caseSave + '/' + cName
    if os.path.exists(cpath):
        cpath = cpath + " " + ct
    newScript = caseSave + '/Nuix Scripts/' + str(cName) + ".rb"
    if os.path.exists(newScript):
        newScript = caseSave + '/Nuix Scripts/' + str(cName) + " " + ct + ".rb"
    if not os.path.exists(caseSave + '/Nuix Scripts/'):
        os.mkdir(caseSave + '/Nuix Scripts/')
    fin = open("Settings/Nuix/Scripts/" + script)
    fout = open(convertPath(newScript), "w+")

    for line in fin:
        if 'AUTOFCASEPATH' in line:
            fout.write(line.replace('AUTOFCASEPATH', str(cpath)))
        elif 'CASENAME' in line:
            fout.write(line.replace('CASENAME', str(cName)))
        elif 'AUTOFIMAGE' in line:
            image = images[count]
            imagePath = image.replace('\\', '/')
            fout.write(line.replace('AUTOFIMAGE', imagePath))
            images.pop(0)
            count = 0
            while count < len(images):
                imagePath = images[count].replace('\\', '/')
                fout.write('    evidence.addFile("' + imagePath + '")\n')
                count = count + 1
        else:
            fout.write(line)
    fin.close()
    fout.close()

    proc = subprocess.Popen(path + ' ' + nuixLicense[0][0] + ' "' + newScript + '"')

    count = count + 1
    progress.start(20)
    while proc.poll() is None:
        imagesWindow.update()

    progress.stop()

    messagebox.showinfo("Complete", "Process complete.")
    imagesWindow.destroy()