# Python 3
#HomeworkCheck.py
#Grabs/Updates all repos and prints out the last commit date

# Requires SSH key paired with GitHub Account
#   Step 1: Install git locally if you have not already done so: https://git-scm.com/downloads
#   Step 2: https://inchoo.net/dev-talk/how-to-generate-ssh-keys-for-git-authorization/
#   Step 3: https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/adding-a-new-ssh-key-to-your-github-account
#   Step 4: Test by running the following command in the shell: ssh -T git@github.com
#           If you see "Hi hdsbbrooks! You've successfully authenticated, but GitHub does not provide shell access." all is good =)
#           Refrence: https://gist.github.com/developius/c81f021eb5c5916013dc

import os
import sys
import subprocess

#Classroom Info
classroomName = 'HDSB-redacted-Q2'   #The name of your github organization
rosterPath = r'C:\redacted\ics2o\example_roster.txt'                   #Path to your class roster (one github username per line)

#Assignment Info
# #Homework Repo
# assignmentName = 'homework-repo'            #The repo assignment name in github classroom
# repoPath = r'C:\redacted\ics2o\Homework'            #The path to save the repos that are downloaded

startingPath = os.getcwd()


with open(rosterPath) as f:
    names = f.read().splitlines()

for name in names:
    print(name)
    
    folderName = f'{assignmentName}-{name}'
    print(f'{repoPath}\\{folderName}')
    if os.path.exists(f'{repoPath}\\{folderName}'):   #Check to see if the project has been cloned before
        resetCmd = 'git reset --hard'                 #Blow away any unstaged changes (permanently)
        pullCmd = 'git pull --rebase origin'          #Pull all changes using a rebase
        lastCommitDateCmd = 'git log -1 --format=%cd' #Get the date and time of most recent commit
        
        os.chdir(f'{repoPath}/{folderName}')          #Change the dir to the repo's folder
        os.system(resetCmd)                           #Run the commands
        os.system(pullCmd)
        lastCommitDate = subprocess.check_output(lastCommitDateCmd, shell=True);
        #lastCommitDate = os.system(lastCommitDateCmd)  #doesn't save output
        print('Last Commit: ',lastCommitDate.decode("utf-8"))
        os.chdir(startingPath)                        #Reset the path back to the starting folder
    else:                                             #Project has not been cloned before, so grab it.
        cloneCmd = "git clone git@github.com:{}/{} {}\\{}".format(classroomName, folderName, repoPath, folderName)
        print(cloneCmd)
        os.system(cloneCmd)
        
print("Finished!")

