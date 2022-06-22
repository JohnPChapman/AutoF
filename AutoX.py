# X-Ways Forensics case automater
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Progressbar
import subprocess
import os
from AutoS import convertPath, now
from autologging import logged, TRACE, traced
import threading, time, random
from queue import Queue

# RVS over existing cases COMPLETE
@traced
def caseMode(path, cases, caseSave):
    casesWindow = Tk()
    casesWindow.title("AutoF X-Ways Case")
    casesWindow.geometry("300x70")
    casesWindow.resizable(width=False, height=False)
    casesWindow.attributes('-disabled', True)
    progressDivide = 100 / len(cases)
    Label(casesWindow, text="Running X-ways in Case mode").place(x=25, y=5)
    progress = Progressbar(casesWindow, orient=HORIZONTAL, length=250, mode='determinate')
    progress.place(x=25, y=35)

    count = 0
    while count < len(cases):
        proc = subprocess.Popen(path + ' "' + cases[count] + '"' + " RVS:~ Override:1  auto")
        count = count + 1
        while proc.poll() is None:
            casesWindow.update()
        progress['value'] += progressDivide
    messagebox.showinfo("Complete", "Process complete.")
    casesWindow.destroy()


# Create compound case, all images in one case COMPLETE
@traced
def xCompound(path, images, caseSave, compoundName, dt):
    compoundWindow = Tk()
    compoundWindow.title("AutoF X-Ways Single Case")
    compoundWindow.geometry("300x70")
    compoundWindow.resizable(width=False, height=False)
    compoundWindow.attributes('-disabled', True)
    saveLocation = caseSave
    if saveLocation == '':
        messagebox.showinfo("ERROR", "No case save location selected")
        return None
    elif compoundName == '':
        messagebox.showinfo("ERROR", "No case Name input")
        return None
    elif len(images) == 0:
        messagebox.showinfo("ERROR", "No images selected")
        return None
    elif len(images) == 1:
        messagebox.showinfo("ERROR", "Single Case selected with only 1 image")
        return None
    Label(compoundWindow, text="Running X-ways in Single Case mode").place(x=25, y=5)
    progress = Progressbar(compoundWindow, orient=HORIZONTAL, length=250, mode='indeterminate')
    progress.place(x=25, y=35)
    compoundWindow.update_idletasks()
    count = 0
    exhibitList = []
    while count < len(images):
        exhibitList.append('"' + "AddImage:" + images[count] + '" ')
        count = count + 1
    allExhibits = ''.join(exhibitList)
    compoundWindow.update_idletasks()
    cPath = convertPath(
        caseSave + '/') + compoundName + "\\" + compoundName

    if os.path.exists(cPath):
        cPath = convertPath(
            caseSave + '/') + compoundName + ' ' + now() + "\\" + compoundName
        cPath = cPath + " " + now()
    proc = subprocess.Popen(path + ' "' + "NewCase:" + cPath + '" ' + convertPath(
        allExhibits) + "RVS:~ Override:1  auto")
    progress.start(20)
    while proc.poll() is None:
        compoundWindow.update()

    progress.stop()
    if dt == 2:
        messagebox.showinfo("Complete", "Process complete.")
        compoundWindow.destroy()
    else:
        compoundWindow.destroy()



# Process all images, individual cases by default COMPLETE
@traced
def processImages(path, images, caseSave, dt):

    imagesWindow = Tk()
    imagesWindow.title("AutoF X-Ways Image")
    imagesWindow.geometry("300x70")
    imagesWindow.resizable(width=False, height=False)
    imagesWindow.attributes('-disabled', True)
    progressDivide = 100 / len(images)
    Label(imagesWindow, text="Running X-ways in Image mode").place(x=25, y=5)
    progress = Progressbar(imagesWindow, orient=HORIZONTAL, length=250, mode='determinate')
    progress.place(x=25, y=35)
    imagesWindow.attributes('-topmost', True)
    if not caseSave:
        messagebox.showinfo("ERROR", "No case save location selected")
        return None
    elif len(images) == 0:
        messagebox.showinfo("ERROR", "No images selected")
        return None

    count = 0

    while count < len(images):
        caseName = os.path.split(images[count])
        cPath = convertPath(caseSave + '/') + os.path.splitext(caseName[1])[
                0] + "\\" + os.path.splitext(caseName[1])[0]
        if os.path.exists(cPath):
            cPath = convertPath(caseSave + '/') + os.path.splitext(caseName[1])[
                0] + ' ' + now() + "\\" + os.path.splitext(caseName[1])[0]
        proc = subprocess.Popen(
            path + ' "' + "NewCase:" + cPath + '"' + " " + '"' + "AddImage:" + convertPath(
                images[count]) + '"' + " RVS:~ Override:1  auto")

        count = count + 1
        while proc.poll() is None:
            imagesWindow.update()
        progress['value'] += progressDivide

    if dt == 2:
        messagebox.showinfo("Complete", "Process complete.")
        imagesWindow.destroy()
    else:
        imagesWindow.destroy()


# Combines x-ways cases and retains RVS
@traced
def xCombine(path, cases, saveName, caseSave):
    exhibitList = []
    count = 0
    for x in cases:
        exhibitList.append(' "' + x + '" ')
        count = count + 1
    allExhibits = ''.join(exhibitList)

    subprocess.Popen(path + ' "NewCase:' + convertPath(caseSave) + '\\' + saveName + '\\' + saveName +'"' + allExhibits + 'Override:1  auto')


# Runs in concurrent mode
@traced
def xConcurrent(path, images, caseSave, tCount):
    jobs = Queue()

    def runConc(q):
        while not q.empty():
            value = q.get()
            time.sleep(random.randint(1, 5))
            subprocess.call(value)
            q.task_done()

    # put all commands to run x-ways into queue
    for i in range(len(images)):
        caseName = os.path.split(images[i])
        cPath = convertPath(caseSave + '/') + os.path.splitext(caseName[1])[
            0] + "\\" + os.path.splitext(caseName[1])[0]
        if os.path.exists(cPath):
            cPath = convertPath(caseSave + '/') + os.path.splitext(caseName[1])[
                0] + ' ' + now() + "\\" + os.path.splitext(caseName[1])[0]
        jobs.put(
            path + ' "' + "NewCase:" + cPath + '"' + " " + '"' + "AddImage:" + convertPath(
                images[i]) + '"' + " RVS:~ Override:1 Cfg:WinHex.cfg auto")


    for i in range(int(tCount)):
        worker = threading.Thread(target=runConc, args=(jobs,))
        worker.start()

