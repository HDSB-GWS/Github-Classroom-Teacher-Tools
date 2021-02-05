# Python 3
# GetReadyForGrading.py
# If Repo not already cloned: Clones repo and creates feedback branch
# If Repo exists, stashes all uncommited changes, updates feedback branch from main branch, and restores stash

# WARNING: This script is NOT super resiliant and does not check for all edge cases.  Use at your own risk.

# Requires SSH key paired with GitHub Account

import os
import sys
import subprocess

isQuiet = False      #This script really spams the console so os.system commands replaced with subprocess and can be muted via isQuiet

def noisy(noiseIn): #Only allow console output for noisy commands if not isQuiet
    if not isQuiet:
        print(noiseIn.decode("utf-8"))

#Classroom Info
# orgName = 'HDSB-GWS-XXXXX'                 #The name of your github organization
# rosterPath = r'C:\SOMEPATH\ics2oq2.txt'    #Path to your class roster (one github username per line)

orgName = 'HDSB-GWS-ICS2-202021-Q2'   #The name of your github organization
rosterPath = r'C:\Users\chris\Documents\GitHub\ics2o\ics2oq2_test.txt'                   #Path to your class roster (one github username per line)

#Assignment Info
# assignmentName = 'example-repo'            #The repo assignment name in github classroom
# repoPath = r'C:\SOMEPATH\ExampleRepo'      #The path to save the repos that are downloaded

#House Construction Game Assignment
assignmentName = 'house-construction'            #The repo assignment name in github classroom
repoPath = r'C:\Users\chris\Documents\GitHub\ics2o\ScriptTest-HouseConstruction'            #The path to save the repos that are downloaded


startingPath = os.getcwd()

with open(rosterPath) as f:
    names = f.read().splitlines()

for name in names:
    print(name)
    
    folderName = f'{assignmentName}-{name}'
    
    #Find if default branch is master or main
    defaultBranch = ""
    
    checkBranchCmd = f'git ls-remote --heads git@github.com:{orgName}/{folderName} '
    if (len(subprocess.check_output(checkBranchCmd + "main", shell=True)) > 0):
        defaultBranch = 'main'
    elif (len(subprocess.check_output(checkBranchCmd + "master", shell=True)) > 0):
        defaultBranch = 'master'
    else:
        print("Whoa, something is really wrong.  Go see why there isn't a main/master branch")
        break
    
    print(f'{repoPath}\\{folderName}')
    if os.path.exists(f'{repoPath}\\{folderName}'):   #Check to see if the project has been cloned before
        
        os.chdir(f'{repoPath}/{folderName}')          #Set correct repo path
        
        #os.system('git stash -u')
        print("pre")
        noisy(subprocess.check_output('git pull' , shell=True))                   #Pull any changes from feedback branch
        print("post")
        noisy(subprocess.check_output('git stash -u', shell=True))                #Stash current changes
        noisy(subprocess.check_output('git checkout '+defaultBranch , shell=True))#Switch to default (aka student) branch
        noisy(subprocess.check_output('git pull' , shell=True))                   #Pull any changes from default branch
        noisy(subprocess.check_output('git checkout feedback' , shell=True))      #Switch back to feedback branch
        noisy(subprocess.check_output('git merge '+defaultBranch , shell=True))   #Merge in any changes made by student in default branch
        noisy(subprocess.check_output('git push' , shell=True))                   #Push the changes into the remote server
        try:
            noisy(subprocess.check_output('git stash apply' , shell=True))            #Reapply all stashed changes
        except subprocess.CalledProcessError as e:  #If there is no stash to apply, this returns an error code of 1
            if e.returncode != 1:                   #So catch the error unless it's not 1, then let it through
                raise e                             #TODO: Add a check to only reapply the stash if files were stashed

        lastCommitDateCmd = 'git log -1 --format=%cd' #Get the date and time of most recent commit
        lastCommitDate = subprocess.check_output(lastCommitDateCmd, shell=True);  #Save the result for use later
        print(f'Last Commit by {name} : {lastCommitDate.decode("utf-8")}')
        os.chdir(startingPath)                        #Reset the path back to the starting folder
        
    else:     #Project has not been cloned before, so grab it.
                                                      #Clone Repo
        cloneCmd = f'git clone git@github.com:{orgName}/{folderName} {repoPath}\\{folderName}'
        print(cloneCmd)
        os.system(cloneCmd)
            
        os.chdir(f'{repoPath}/{folderName}')         #Set correct repo path
        
        if (len(subprocess.check_output(checkBranchCmd + "feedback", shell=True)) == 0):  #check if feedback branch, if not create it.
            print('Create and Push branch')
            noisy(subprocess.check_output('git checkout -b feedback' , shell=True)) 
            noisy(subprocess.check_output('git push -u origin feedback' , shell=True)) 
        else:
            print('Set feeback to current branch')
            noisy(subprocess.check_output('git checkout feedback' , shell=True)) 
        
        os.chdir(startingPath)                        #Reset the path back to the starting folder

        
print("Finished!")



