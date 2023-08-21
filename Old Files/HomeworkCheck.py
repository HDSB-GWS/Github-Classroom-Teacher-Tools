# Python 3
#HomeworkCheck.py
#Grabs/Updates all repos and prints out the last commit date

# Requires SSH key paired with GitHub Account

import os
import sys
import subprocess

#Classroom Info
orgName = 'HDSB-GWS-XXXXX'                 #The name of your github organization
rosterPath = r'C:\SOMEPATH\ics2oq2.txt'    #Path to your class roster (one github username per line)

#Assignment Info
assignmentName = 'example-repo'            #The repo assignment name in github classroom
repoPath = r'C:\SOMEPATH\ExampleRepo'      #The path to save the repos that are downloaded




startingPath = os.getcwd()


with open(rosterPath) as f:
    names = f.read().splitlines()

for name in names:
    print(name)
    
    folderName = f'{assignmentName}-{name}'
    print(f'{repoPath}\\{folderName}')
    if os.path.exists(f'{repoPath}\\{folderName}'):   #Check to see if the project has been cloned before
        resetCmd = 'git reset --hard'                 #Blow away any changes (permanently)
        pullCmd = 'git pull --rebase origin'          #Pull all changes using a rebase
        lastCommitDateCmd = 'git log -1 --format=%cd' #Get the date and time of most recent commit
        
        os.chdir(f'{repoPath}/{folderName}')          #Change the dir to the repo's folder
        os.system(resetCmd)                           #Run the commands
        print(pullCmd)
        os.system(pullCmd)
        lastCommitDate = subprocess.check_output(lastCommitDateCmd, shell=True);
        #lastCommitDate = os.system(lastCommitDateCmd)  #doesn't save output
        print('Last Commit: ',lastCommitDate.decode("utf-8"))
        os.chdir(startingPath)                        #Reset the path back to the starting folder
    else:                                             #Project has not been cloned before, so grab it.
        cloneCmd = "git clone git@github.com:{}/{} {}\\{}".format(orgName, folderName, repoPath, folderName)
        print(cloneCmd)
        os.system(cloneCmd)
        
print("Finished!")

