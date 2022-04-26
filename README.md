
# AutoF

AutoF is a tool to automate digital forensic processing in X-Ways Forensics and Nuix. The tool will scan for compatible forensic images, from there you can select your own profile and process all of the images with the same settings, either as individual cases or one 'compound' case. Node mode allows you to utilise Jenkins and distributed nodes to process multiple images at once. Images can be skipped based on keywords. You can also combine X-Ways cases to a brand new case or run X-Ways profiles over pre-existing cases.

 



## Creating an EXE and folder structure
I use pyinstaller to convert to an EXE, other tools are avalible! The tested and recommended command is 'pyinstaller --onefile --noconsole -i "PATH\ax.ico" PATH\AutoF.py'.  

The following folder structure is currently needed:  

Install Folder\\  
AutoF.exe  
  
Jenkins\\  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;       nuixProcessing.xml  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;         processing.xml  
  
Settings\\  
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;     ax.ico  
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;     settings.db  
.     
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  \\HTML Help\\  
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;         help.chm  
.      
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  \\Logs\\  
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;         RunLog 07-04-2022 00-13-30.txt*  
.      
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  \\Nuix\\  
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;     \\Scripts\  
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;             Lab2.rb*  
.      
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  \\X-ways profiles\\  
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;          Default.cfg*  
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;          Hash.cfg*  
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;          Lots.cfg*  

*Denotes an example file
## Documentation

[Documentation](https://www.autof.uk/Forum/viewtopic.php?t=3)


## Feedback

If you have any feedback, please reach out to us at admin@autof.uk or post in autof.uk/Forum

