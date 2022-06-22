# AutoF settings handler
from datetime import datetime
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import sqlite3
from cryptography.fernet import Fernet
import os
from win32com.client import Dispatch
from tkinter import ttk
from autologging import logged, TRACE, traced


# Help Index Complete
@traced
def indexWindow(event=None):
    try:
        os.startfile('Settings\\HTML Help\\help.chm')
    except FileNotFoundError:
        messagebox.showerror('Error!',
                             'Can not find Help file. Perhaps the install is not complete')


# About menu COMPLETE
@traced
def aboutWindow(event=None):
    about = Toplevel()
    about.title("About AutoF")
    about.geometry("600x400")
    about.resizable(width=False, height=False)
    about.grab_set()
    try:
        about.iconbitmap('settings\\ax.ico')
    except:
        messagebox.showerror('Error!',
                             'Can not find AutoF.ico file. Perhaps the install is not complete')
    aboutText = Text(about, width=70, height=20, bg="lightgrey", wrap=WORD)
    aboutText.pack(pady=10)
    aboutText.tag_config('justified', justify=CENTER)
    aboutText.insert(END, 'Copyright © 2022 AutoF\n'
                            'AutoF - Automating X-ways & Nuix.\n'
                            'This program is free software; you can redistribute it and/or\n'
                            'modify it under the terms of the GNU General Public License\n'
                            'as published by the Free Software Foundation; either version 2\n'
                            'of the License, or (at your option) any later version.\n\n'
                            'This program is distributed in the hope that it will be useful,\n'
                            'but WITHOUT ANY WARRANTY; without even the implied warranty of\n'
                            'MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n'
                            'GNU General Public License for more details.\n\n'
                            'You should have received a copy of the GNU General Public License\n'
                            'along with this program; if not, write to the Free Software\n'
                            'Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.', 'justified')
    aboutText.config(state=DISABLED, bg='white')
    aboutExit = Button(about, text='Exit', command=about.destroy)
    aboutExit.pack(pady=5)


# Jenkins settings menu COMPLETE
@traced
def jenkinsSettingsWindow(event=None):
    def storeJenkins(tool, ip, user, password, job, pool, xways):
        conn = sqlite3.connect('settings\\settings.db ')
        cur = conn.cursor()
        cur.execute("Delete FROM Node Where Tool = '" + tool + "'")
        conn.commit()
        # This should be changed before compiling
        key = bytes(b'om1np7SF2rtxOEop_Vxbg8MgMokQX0AVRhOAT1fLLkg=')
        fernet = Fernet(key)
        encPassword = fernet.encrypt(password.encode())
        cur.execute('INSERT INTO Node(Tool, IP, User, password, Job, Pool, Xways) VALUES(?,?,?,?,?,?,?)',
                    (tool, ip, user, encPassword, job, pool, xways,))
        conn.commit()

    def gatherSettings():
        if xSelect.get() == 1:
            tool = "xways"
        else:
            tool = "nuix"
        ip = jenkinsSettingsTextIP.get()
        user = jenkinsSettingsTextUser.get()
        password = jenkinsSettingsTextPassword.get()
        job = jenkinsSettingsTextJob.get()
        pool = jenkinsSettingsTextPool.get()
        xways = jenkinsSettingsTextProc.get()
        if not tool or not ip or not user or not password or not job or not xways:
            messagebox.showerror('Error!',
                                 'Information not complete')
            jenkinsSettingsWin.lift()
        else:
            storeJenkins(tool, ip, user, password, job, pool, xways)

    def toolButtonx():
        jenkinsSettingsNuix.deselect()
        jenkinsSettingsXways.select()
        xSelect.set(1)
        nSelect.set(0)
        returnSettings()

    def toolButtonn():
        jenkinsSettingsXways.deselect()
        jenkinsSettingsNuix.select()
        nSelect.set(1)
        xSelect.set(0)
        returnSettings()

    def returnSettings():
        conn = sqlite3.connect('settings\\settings.db ')
        cur = conn.cursor()
        if xSelect.get() == 1:
            query = "xways"
        else:
            query = "nuix"

        cur.execute("Select * FROM Node Where Tool = '" + query + "'")
        conn.commit()
        rows = cur.fetchall()
        if not rows:
            jenkinsSettingsTextIP.delete(0, 'end')
            jenkinsSettingsTextUser.delete(0, 'end')
            jenkinsSettingsTextJob.delete(0, 'end')
            jenkinsSettingsTextPool.delete(0, 'end')
            jenkinsSettingsTextProc.delete(0, 'end')
            jenkinsSettingsTextPassword.delete(0, 'end')
            return
        else:
            jenkinsSettingsTextIP.delete(0, 'end')
            jenkinsSettingsTextIP.insert(INSERT, rows[0][1])
            jenkinsSettingsTextUser.delete(0, 'end')
            jenkinsSettingsTextUser.insert(INSERT, rows[0][2])
            jenkinsSettingsTextPassword.delete(0, 'end')
            jenkinsSettingsTextPassword.insert(INSERT, '')
            jenkinsSettingsTextJob.delete(0, 'end')
            jenkinsSettingsTextJob.insert(INSERT, rows[0][4])
            jenkinsSettingsTextPool.delete(0, 'end')
            jenkinsSettingsTextPool.insert(INSERT, rows[0][5])
            jenkinsSettingsTextProc.delete(0, 'end')
            jenkinsSettingsTextProc.insert(INSERT, rows[0][7])

    jenkinsSettingsWin = Toplevel()
    jenkinsSettingsWin.title("Jenkins Settings")
    jenkinsSettingsWin.geometry("300x450")
    jenkinsSettingsWin.resizable(width=False, height=False)
    jenkinsSettingsWin.grab_set()
    try:
        jenkinsSettingsWin.iconbitmap('settings\\ax.ico')
    except:
        messagebox.showerror('Error!',
                             'Can not find AutoF.ico file. Perhaps the install is not complete')
    jenkinsSettingsLabelIP = Label(jenkinsSettingsWin, text="Jenkins Address:")
    jenkinsSettingsLabelIP.pack(pady=5)
    jenkinsSettingsTextIP = Entry(jenkinsSettingsWin, width=40, bg="white")
    jenkinsSettingsTextIP.pack(pady=1)

    jenkinsSettingsLabelUser = Label(jenkinsSettingsWin, text="Jenkins User name:")
    jenkinsSettingsLabelUser.pack(pady=5)
    jenkinsSettingsTextUser = Entry(jenkinsSettingsWin, width=40, bg="white")
    jenkinsSettingsTextUser.pack(pady=1)

    jenkinsSettingsLabelPassword = Label(jenkinsSettingsWin, text="Jenkins password:")
    jenkinsSettingsLabelPassword.pack(pady=5)
    jenkinsSettingsTextPassword = Entry(jenkinsSettingsWin, show="*", width=40, bg="white")
    jenkinsSettingsTextPassword.pack(pady=1)

    jenkinsSettingsLabelJob = Label(jenkinsSettingsWin, text="Jenkins Job:")
    jenkinsSettingsLabelJob.pack(pady=5)
    jenkinsSettingsTextJob = Entry(jenkinsSettingsWin, width=40, bg="white")
    jenkinsSettingsTextJob.pack(pady=1)

    jenkinsSettingsLabelPool = Label(jenkinsSettingsWin, text="Jenkins Node pool:")
    jenkinsSettingsLabelPool.pack(pady=5)
    jenkinsSettingsTextPool = Entry(jenkinsSettingsWin, width=40, bg="white")
    jenkinsSettingsTextPool.pack(pady=1)

    jenkinsSettingsLabelProc = Label(jenkinsSettingsWin, text="Jenkins processing tool path:")
    jenkinsSettingsLabelProc.pack(pady=5)
    jenkinsSettingsTextProc = Entry(jenkinsSettingsWin, width=40, bg="white")
    jenkinsSettingsTextProc.pack(pady=1)

    nSelect = tk.BooleanVar()
    jenkinsSettingsNuix = Checkbutton(jenkinsSettingsWin, text="Nuix", variable=nSelect, onvalue=1, offvalue=0,
                                      command=toolButtonn)
    jenkinsSettingsNuix.place(x=100, y=325)

    xSelect = tk.BooleanVar()
    jenkinsSettingsXways = Checkbutton(jenkinsSettingsWin, text="X-Ways", variable=xSelect, onvalue=1, offvalue=0,
                                       command=toolButtonx)
    jenkinsSettingsXways.place(x=30, y=325)

    jenkinsSettingsSave = Button(jenkinsSettingsWin, text='Save', command=gatherSettings)
    jenkinsSettingsSave.pack(padx=25, side=RIGHT)
    jenkinsSettingsExit = Button(jenkinsSettingsWin, text='Exit', command=jenkinsSettingsWin.destroy)
    jenkinsSettingsExit.pack(padx=25, side=LEFT)
    jenkinsSettingsWin.grab_set()


# Gets password from database tp login to Jenkins
def getPassword():
    conn = sqlite3.connect('settings\\settings.db ')
    cur = conn.cursor()
    cur.execute("SELECT Password FROM Node")
    encPassword = cur.fetchall()
    password = bytes(*encPassword[0])
    key = bytes(b'om1np7SF2rtxOEop_Vxbg8MgMokQX0AVRhOAT1fLLkg=')
    fernet = Fernet(key)
    decPassword = fernet.decrypt(password).decode()
    return decPassword


# Date and time COMPLETE
@traced
def now():
    rightNow = datetime.now()
    timeNow = rightNow.strftime("%d-%m-%Y %H-%M-%S")
    return timeNow

# converts path for Windows COMPLETE
@traced
def convertPath(path):
    return path.replace('/', '\\')


# Get X-Ways installs
@traced
def getXways():
    # Version lists
    installs = []
    versions = []
    cfgLocations = []
    conn = sqlite3.connect('settings\\settings.db ')
    cur = conn.cursor()

    # Gets all cfg locations
    cur.execute("SELECT * FROM CFG")
    cfgs = cur.fetchall()

    # adds cfg locations to list
    for cfg in cfgs:
        cfgLocations.append(cfg)
    cfgTest = 0

    # validates cfg
    if len(cfgLocations) == 0:
        cfgTest = 0
    else:
        for row in cfgLocations:
            if os.path.isfile(row[0]):
                cfgTest = 1
            else:
                cfgTest = 0
                break
    # gets all versions from x-ways table
    cur.execute("SELECT * FROM Xways")
    rows = cur.fetchall()

    pathTest = ''
    # adds table data to lists
    for row in rows:
        installs.append(row[0])
        versions.append(row[1])

    # validates installs
    if len(installs) == 0:
        pathTest = 0
    else:
        for row in installs:
            if os.path.isfile(row):
                pathTest = 1
            else:
                pathTest = 0
                break

    # if installs validated breaks from function, otherwise wipes table and rescans for x-ways
    if pathTest == 1 and cfgTest == 1:
        return installs, versions, cfgLocations
    else:
        cur.execute("DELETE FROM Xways")
        conn.commit()
        cur.execute("DELETE FROM CFG")
        conn.commit()
    # Creates window for scanning of xways
    settings = Tk()
    settings.update_idletasks()
    installs.clear()
    versions.clear()
    cfgLocations.clear()
    fileScan = Label(settings, text="Scanning for Xways")
    fileScan.place(x=25, y=20)
    settings.title("X-Ways Scan")
    settings.geometry("200x75")
    settings.resizable(width=False, height=False)
    # Searches the C drive for x-ways .exes and adds to a list
    sconn = sqlite3.connect('settings\\settings.db ')
    scur = sconn.cursor()
    scur.execute("Select ScanDrives FROM Settings")
    sconn.commit()
    rows = scur.fetchall()
    drives = str(rows[0][0])
    drives = drives.split(',')
    for i in drives:
        for iRoot, directories, files in os.walk(i, topdown=False):
            settings.update_idletasks()
            for name in files:
                if '$' not in os.path.join(iRoot, name) and (name.endswith('xwforensics64.exe') or name.endswith('xwforensics.exe') \
                        or name.endswith('nuix_console.exe')):
                    fileScan.config(text='Found: ' + name)
                    installs.append(convertPath(os.path.join(iRoot, name)))
                elif 'WinHex.cfg.lnk' not in name and '$' not in os.path.join(iRoot, name) and 'WinHex.cfg' in name:
                    cfgLocations.append(os.path.join(iRoot, name))
    # checks the version and appends to a list
    for line in installs:
        settings.update_idletasks()
        ver_parser = Dispatch('Scripting.FileSystemObject')
        info = ver_parser.GetFileVersion(line)
        if 'xwforensics64.exe' in line:
            versions.append('X-ways ' + info + ' 64Bit')
        elif 'xwforensics.exe' in line:
            versions.append('X-ways ' + info + ' 32Bit')
        elif 'nuix_console.exe' in line:
            versions.append('Nuix ' + info)

    # Checks lists if - 0 then warn and instruct as x-ways not found
    if len(installs) == 0 or len(versions) == 0:
        messagebox.showerror('Error!', 'X-ways not found! Change the drive to scan in settings and run Force Scan')
        installs.append('Error')
        versions.append('Check scan drive')

    # Populate SQLite settings database with cfg paths for use next time
    count = 0
    while count < len(cfgLocations):
        cur = conn.cursor()
        value = str(cfgLocations[count])
        cur.execute('INSERT INTO CFG(path) VALUES(?)', (value,))
        conn.commit()
        count = count + 1

    # Populate SQLite settings database with xways paths for use next time
    count = 0
    while count < len(versions):
        cur = conn.cursor()
        sql = 'INSERT INTO Xways(Location, Version) VALUES(?,?);'
        values = installs[count], versions[count]
        cur.execute(sql, values)
        conn.commit()
        count = count + 1
    cfgLocations.clear()
    # Gets all cfg locations done for consistent storage in list
    cur.execute("SELECT * FROM CFG")
    cfgs = cur.fetchall()

    # adds cfg locations to list
    for cfg in cfgs:
        cfgLocations.append(cfg)

    settings.destroy()
    return installs, versions, cfgLocations


# Selects images compatible with x-ways or Nuix
@traced
def imageXSort(folderskip, mypath, tool, ufdr):
    images = []
    if 'X-ways' in tool and ufdr == 0:
        for iRoot, directories, files in os.walk(mypath, topdown=False):
            for name in files:
                if '.e01' in name[-4:] or '.001' in name[-4:] or '.E01' in name[-4:] or '.dd' in name[
                                                                                                 -3:] or '.img' in name[
                                                                                                 -4:] or '.ctr' in name[
                                                                                                 -4:] or '.vhd' in name[
                                                                                                 -4:] or '.vhdx' in name[
                                                                                                 -5:] or '.vdmk' in name[
                                                                                                 -5:] or '.vdi' in name[
                                                                                                 -4:]:
                    images.append(convertPath(os.path.join(iRoot, name)))
    elif ufdr == 1:
        for iRoot, directories, files in os.walk(mypath, topdown=False):
            for name in files:
                if '.ufdr' in name[-5:]:
                    images.append(convertPath(os.path.join(iRoot, name)))
    else:
        for iRoot, directories, files in os.walk(mypath, topdown=False):
            for name in files:
                if '.e01' in name[-4:] or '.001' in name[-4:] or '.E01' in name[-4:] or '.dd' in name[
                                                                                                 -3:] or '.img' in name[
                                                                                                 -4:] or '.ctr' in name[
                                                                                                 -4:] or '.vhd' in name[
                                                                                                 -4:] or '.vhdx' in name[
                                                                                                 -5:] or '.vdmk' in name[
                                                                                                 -5:] or '.vdi' in name[
                                                                                                 -4:] or '.L01' in name[
                                                                                                 -4:]:
                    images.append(convertPath(os.path.join(iRoot, name)))
    # Removes any images from the list that hit the skip terms
    if len(folderskip) > 0:
        for f in folderskip:
            count = 0
            while count != len(images):
                if f.lower() in images[count].lower():
                    images.pop(count)
                    continue
                count = count + 1

    return images


# General options window
@traced
def generalOptionsWindow(event=None):
    def end():
        generalOptionsWin.destroy()

    def save():
        def storeSettings(scanDrives, nuixLicense):
            conn = sqlite3.connect('settings\\settings.db ')
            cur = conn.cursor()
            cur.execute("Delete FROM Settings")
            conn.commit()
            cur.execute('INSERT INTO Settings(ScanDrives, NuixLicense) VALUES(?,?)',
                        (scanDrives, nuixLicense,))
            conn.commit()

        scanDrives = optionsDriveText.get()

        nuixLicense = nuixLicenseText.get()

        if not scanDrives:
            messagebox.showerror('Error!',
                                 'You must include drives to scan.')
            generalOptionsWin.lift()
        else:
            storeSettings(scanDrives, nuixLicense)

    def readSettings():
        sconn = sqlite3.connect('settings\\settings.db ')
        scur = sconn.cursor()
        scur.execute("Select * FROM Settings")
        sconn.commit()
        rows = scur.fetchall()

        if not rows:
            optionsDriveText.delete(0, 'end')


        else:
            optionsDriveText.delete(0, 'end')
            optionsDriveText.insert(INSERT, rows[0][0])

            nuixLicenseText.delete(0, 'end')
            nuixLicenseText.insert(INSERT, rows[0][4])

    generalOptionsWin = Toplevel()
    generalOptionsWin.title("General Options")
    generalOptionsWin.geometry("300x250")
    generalOptionsWin.resizable(width=False, height=False)
    generalOptionsWin.grab_set()

    optionsDriveLabel = Label(generalOptionsWin, text="Drives to scan for forensic tools:")
    optionsDriveLabel.pack(pady=5)
    optionsDriveText = Entry(generalOptionsWin, width=20, bg="white")
    optionsDriveText.pack(pady=10)

    nuixLicenseLabel = Label(generalOptionsWin, text="Nuix License info:")
    nuixLicenseLabel.pack(pady=5)
    nuixLicenseText = Entry(generalOptionsWin, width=40, bg="white")
    nuixLicenseText.pack(pady=10)


    sep = ttk.Separator(generalOptionsWin, orient='horizontal')
    sep.pack(pady=4, fill='x')



    optionsSave = Button(generalOptionsWin, text='Save', command=save)
    optionsSave.pack(padx=25, side=RIGHT)
    optionsExit = Button(generalOptionsWin, text='Exit', command=end)
    optionsExit.pack(padx=25, side=LEFT)
    generalOptionsWin.grab_set()

    readSettings()
