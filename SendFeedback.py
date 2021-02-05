# Python 3
# SendFeedback.py
# Uses github cli and git command line to create a commit of all changes and then push it as a pull request back to the student

# Requires SSH key paired with GitHub Account
# Requires Github CLI to be installed: https://cli.github.com/

# WARNING: This script is NOT super resiliant and does not check for all edge cases.  Use at your own risk. You may have to fix the odd
# merge conflict after running this.

import os
import sys
import subprocess
import re

isQuiet = True     #This script really spams the console so os.system commands replaced with subprocess and can be muted via isQuiet

def noisy(noiseIn): #Only allow console output for noisy commands if not isQuiet
    if not isQuiet:
        print(noiseIn.decode("utf-8"))

commitMessage = ' "Feedback Commit"'

#Classroom Info
# orgName = 'HDSB-GWS-XXXXX'                 #The name of your github organization
# rosterPath = r'C:\SOMEPATH\ics2oq2.txt'    #Path to your class roster (one github username per line)

#Assignment Info
# assignmentName = 'example-repo'            #The repo assignment name in github classroom
# repoPath = r'C:\SOMEPATH\ExampleRepo'      #The path to save the repos that are downloaded




startingPath = os.getcwd()


with open(rosterPath) as f:
    names = f.read().splitlines()

for name in names:
    print(f'\r\n {name}')
    
    folderName = f'{assignmentName}-{name}'
    print(f'{repoPath}\\{folderName}')
    
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
    
    
    
    if os.path.exists(f'{repoPath}\\{folderName}'):   #Check to see if the project has been cloned before
        
        os.chdir(f'{repoPath}/{folderName}')          #Change the dir to the repo's folder
        
        noisy(subprocess.check_output('git add --all', shell=True))       #Stage all (new, modified, deleted) files
        #os.system('git commit -m '+ commitMessage)                        #Commit all staged changes  #NB: git reset HEAD~ If you want to undo a commit that is local.
        try:
            noisy(subprocess.check_output('git commit -m '+ commitMessage, shell=True))                #Stage all (new, modified, deleted) files
        except subprocess.CalledProcessError as e:  #If no PR exists this command errors out with a return value of 1
            if e.returncode != 1:                   #So catch the error unless it's not 1, then let it through
                raise e
            
        noisy(subprocess.check_output('git push', shell=True))                #Push Changes   

      
        
        #print(int(subprocess.check_output('git rev-list --count main...feedback', shell=True))) 
        if (int(subprocess.check_output('git rev-list --count main...feedback', shell=True)) > 0):  #If feedback branch is ahead
            
            try:
                noisy(subprocess.check_output('gh pr close feedback', shell=True))
            except subprocess.CalledProcessError as e:  #If no PR exists this command errors out with a return value of 1
                if e.returncode != 1:                   #So catch the error unless it's not 1, then let it through
                     raise e

            noisy(subprocess.check_output('gh pr create --fill --title "Feedback from Mr. Brooks"', shell=True))                #Create Pull Request
        else:
            print('No changes found - no Pull Request created')
     
        os.chdir(startingPath)                        #Reset the path back to the starting folder
        
        
    else:                                             #Project has not been cloned before, so go run the getReadyForGrading script.
        print(f"{assignmentName}-{name} Repo does not exist - Skipping")
                
print("\r\nFinished!")



# This code was an attempt to check to see if the pull request exists before closing it.
# Since it ALSO returns an error of 1 if there is no pr to view, then it seems a bit pointless
# Easier to just try to close any open PR and then catch the error as it occurs :|
#         prStatus = ''
#         try:
#             prStatus = subprocess.check_output('gh pr view feedback', shell=True)
# 
#         except subprocess.CalledProcessError as e:  #Check to see if there is a 
#             
#                 
#             if e.returncode == 1:
#                 print("no pr exists",prStatus)
#                 
#             if e.returncode != 1:                   #So catch the error unless it's not 1, then let it through
#                 raise e                             #TODO: Add a check to only reapply the stash if files were stashed
#             else:
#                 pass
#                 
#         else:
#             print("a pr exists",prStatus)
#             prPath = re.search(r"(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-&?=%.]+|$",prStatus.decode("utf-8"))[0]
#             print(prPath)
#             os.system('gh pr close ' + prPath)
#             #TODO grab the PR # and mark it closed
#         


