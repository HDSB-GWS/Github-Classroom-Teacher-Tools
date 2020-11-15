# Python 3
#HomeworkCheck.py
#Grabs/Updates all repos and prints out the last commit date

# Requires SSH key paired with GitHub Account
#   Step 1: https://inchoo.net/dev-talk/how-to-generate-ssh-keys-for-git-authorization/
#   Step 2: https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/adding-a-new-ssh-key-to-your-github-account

import os
import sys
import subprocess

#Classroom Info
classroomName = 'HDSB-GWS-XXXXXXXXXX'   #The name of your github organization
rosterPath = 'roster.txt'                   #Path to your class roster (one github username per line)

#Assignment Info
assignmentName = 'final-project'            #The repo assignment name in github classroom
repoPath = 'final-project-repos'            #The path to save the repos that are downloaded


startingPath = os.getcwd()

with open(rosterPath) as f:
    names = f.read().splitlines()

for name in names:
    print(name)
    
    folderName = f'{assignmentName}-{name}'

    if os.path.exists(f'{repoPath}/{folderName}'):
        resetCmd = 'git reset --hard'         #Blow away any unstaged changes (permanently)
        pullCmd = 'git pull --rebase origin'  #Pull all changes using a rebase
        lastCommitDateCmd = 'git log -1 --format=%cd' #Get the date and time of most recent commit
        
        os.chdir(f'{repoPath}/{folderName}')  #Change the dir to the repo's folder
        os.system(resetCmd)                   #Run the commands
        os.system(pullCmd)
        lastCommitDate = subprocess.check_output(lastCommitDateCmd, shell=True);
        #lastCommitDate = os.system(lastCommitDateCmd)  #doesn't save output
        print('Last Commit: ',lastCommitDate.decode("utf-8"))
        os.chdir(startingPath)                #Reset the path back to the starting folder
    else:
        cloneCmd = "git clone git@github.com:{}/{} {}/{}".format(classroomName, folderName, repoPath, folderName)
        print(cloneCmd)
        os.system(cloneCmd)
        
print("Finished!")

