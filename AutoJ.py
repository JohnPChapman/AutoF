# AutoF Jenkins handler
from tkinter import messagebox
import sqlite3
import jenkins
from AutoS import getPassword, convertPath, now
import os
from shutil import copyfile
from autologging import logged, TRACE, traced


# Node mode, runs processing via Jenkins MORE TO DO
@traced
def xnodeMode(tool, mode, cases, images, caseSaveText, compoundCaseName, profile):
    conn = sqlite3.connect('settings\\settings.db ')
    cur = conn.cursor()
    cur.execute("Select * FROM Node Where Tool = '" + tool + "'")
    conn.commit()
    rows = cur.fetchall()
    if not rows:
        return
    else:

        IP = rows[0][1]
        User = rows[0][2]
        Job = rows[0][4]
        Pool = rows[0][5]
        path = rows[0][7]
        password = getPassword()
        server = jenkins.Jenkins(IP, username=User, password=password)

    try:
        user = server.get_whoami()
    except jenkins.BadHTTPException:
        messagebox.showerror('BadHTTPException!',
                             'Jenkins bad HTTP exception! Check configuration.')
        return
    except jenkins.JenkinsException:
        messagebox.showerror('JenkinsException!',
                             'Jenkins Exception! Check configuration.')
        return
    copyPath = ''
    if 'xwforensics64.exe' in path.lower():
        copyPath = path.replace('xwforensics64.exe', '')
        copyPath = copyPath.replace('"', '')

    elif 'xwforensics.exe' in path.lower():
        copyPath = path.replace('xwforensics.exe', '')
        copyPath = copyPath.replace('"', '')

    if mode == 'individual' and tool == 'xways':
        count = 0
        while count < len(images):
            caseName = os.path.split(images[count])
            copyProfile = os.path.splitext(caseName[1])[0] + " " + now()
            if not os.path.exists(caseSaveText + '/' + 'X-ways profiles/'):
                os.mkdir(caseSaveText + '/' + 'X-ways profiles/')
            jenkinsProfile = caseSaveText + '/' + 'X-ways profiles/' + copyProfile + ".cfg"
            copyfile('Settings\\X-ways profiles\\' + profile, jenkinsProfile)

            case = convertPath(caseSaveText + '/') + os.path.splitext(caseName[1])[0] + "\\" + os.path.splitext(caseName[1])[0]

            if os.path.exists(case):
                case = '"' + convertPath(caseSaveText+ '/') + os.path.splitext(caseName[1])[
                    0] + ' ' + now() + "\\" + os.path.splitext(caseName[1])[0] + '"'
            else:
                case = '"' + convertPath(caseSaveText + '/') + os.path.splitext(caseName[1])[0] + "\\" + \
                       os.path.splitext(caseName[1])[0] + '"'

            server.build_job(Job, {'profile': convertPath(jenkinsProfile),'copypath': copyPath,'xways': path, 'CasePath': case, 'Image': '"' + convertPath(
                    images[count]) + '"'})

            count = count + 1
    elif mode == 'compound' and tool == 'xways':
        count = 0
        exhibitList = []
        copyProfile = compoundCaseName + " " + now()
        if not os.path.exists(caseSaveText + '/' + 'X-ways profiles/'):
            os.mkdir(caseSaveText + '/' + 'X-ways profiles/')
        jenkinsProfile = caseSaveText + '/' + 'X-ways profiles/' + copyProfile + ".cfg"
        copyfile('Settings\\X-ways profiles\\' + profile, jenkinsProfile)
        while count < len(images):
            exhibitList.append('"' + str(images[count]) + '"')
            exhibitList.append(' AddImage:')
            count = count + 1
        exhibitList.pop()
        allExhibits = ''.join(exhibitList)
        case = convertPath(caseSaveText + '/') + compoundCaseName + "\\" + compoundCaseName
        if os.path.exists(case):
            case = '"' + convertPath(caseSaveText + '/') + compoundCaseName + now() +"\\" + compoundCaseName + '"'
        else:
            case = '"' + convertPath(caseSaveText + '/') + compoundCaseName + "\\" + compoundCaseName + '"'
        server.build_job(Job, {'profile': convertPath(jenkinsProfile),'copypath': copyPath,'xways': path, 'CasePath': case, 'Image': convertPath(allExhibits)})

    elif mode == 'individual' and tool == 'nuix':
        count = 0
        while count < len(images):
            caseName = os.path.split(images[count])
            caseName = caseName[1]
            caseName = caseName.split(".")
            caseName = caseName[0]
            ct = now()
            cpath = caseSaveText + '/' + caseName
            newScript = caseSaveText + '/Nuix Scripts/' + str(caseName) + ".rb"
            if os.path.exists(newScript):
                newScript = caseSaveText + '/Nuix Scripts/' + str(caseName) + " " + ct + ".rb"
            if os.path.exists(cpath):
                cpath = cpath + " " + ct
            if not os.path.exists(caseSaveText + '/Nuix Scripts/'):
                os.mkdir(caseSaveText + '/Nuix Scripts/')
            fin = open("Settings/Nuix/Scripts/" + profile)
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
            server.build_job(Job, {'Nuix': path, 'script': '"' + newScript + '"'})
            count = count + 1
    elif mode == 'compound' and tool == 'nuix':
        count = 0
        ct = now()
        cpath = caseSaveText + '/' + compoundCaseName
        if os.path.exists(cpath):
            cpath = cpath + " " + ct
        newScript = caseSaveText + '/Nuix Scripts/' + str(compoundCaseName) + ".rb"
        if os.path.exists(newScript):
            newScript = caseSaveText + '/Nuix Scripts/' + str(compoundCaseName) + " " + ct + ".rb"
        if not os.path.exists(caseSaveText + '/Nuix Scripts/'):
            os.mkdir(caseSaveText + '/Nuix Scripts/')
        fin = open("Settings/Nuix/Scripts/" + profile)
        fout = open(convertPath(newScript), "w+")

        for line in fin:
            if 'AUTOFCASEPATH' in line:
                fout.write(line.replace('AUTOFCASEPATH', str(cpath)))
            elif 'CASENAME' in line:
                fout.write(line.replace('CASENAME', str(compoundCaseName)))
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

        server.build_job(Job, {'Nuix': path, 'script': '"' + newScript + '"'})