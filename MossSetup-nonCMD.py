# Python3
# MossSetup-nonCMD.py 
# Autors: C. Cannon, C. Brooks-Prenger
# Requires SSH key paired with GitHub Account
import os
import sys
import subprocess
import shutil

# Validates command line arguments, outputs instructions if they are invalid
classroomName = 'HDSB-GWS-XXXXXXXXXXXX'
assignmentName = 'final-project'
rosterPath = os.getcwd()+'\\roster.txt'
cloneAssignmentScriptPath = os.getcwd()+'\\Github-Classroom-Utilities\\CloneAssignment.py'
destinationPath = os.getcwd()
extensionType = '.py'


# Make a directory to hold all student submissions, clone all submissions
os.chdir(destinationPath)
os.mkdir("GitHub-Repos")
os.chdir("GitHub-Repos")
cloneAllCommand = "python {} {} {} {}".format(cloneAssignmentScriptPath, classroomName, assignmentName, rosterPath)
print(cloneAllCommand)
subprocess.call(cloneAllCommand, shell=True)

# Make a directory to hold the MOSS formatted source files
os.chdir(destinationPath)
os.mkdir("Moss-Directory")

# Create a directory for each student, with their GitHub username from roster
os.chdir("Moss-Directory")
with open(rosterPath) as f:
    names = f.read().splitlines()
for name in names:
    os.mkdir(name)

# Go through each repository, transfer every .java file to the appropriate MOS directory
os.chdir(os.path.join(destinationPath, "GitHub-Repos"))
for root, dir, files in os.walk(os.getcwd()):
    for file in files :
        if extensionType in file :
            for name in names:
                if name in root :
                    shutil.copy(os.path.join(root, file), os.path.join(destinationPath, "Moss-Directory", name))

print("Done!")