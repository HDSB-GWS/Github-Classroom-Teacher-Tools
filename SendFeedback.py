# Python 3
# SendFeedback.py
# Uses github cli and git command line to create a commit of all changes and then push it as a pull request back to the student

# NOTE:Requires SSH key paired with GitHub Account
# DEPENDENCY: Requires Github CLI to be installed: https://cli.github.com/

# WARNING: This script is NOT super resiliant and does not check for all edge cases.  Use at your own risk. You may have to fix the odd
# merge conflict after running this.

import os
import sys
import subprocess
import re
import time

isQuiet = False     #This script really spams the console so os.system commands replaced with subprocess and can be muted via isQuiet

def noisy(noiseIn): #Only allow console output for noisy commands if not isQuiet
    if not isQuiet:
        print(noiseIn.decode("utf-8"))

commitMessage = ' "Feedback Commit"'

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
    print(f'\r\n {name}')
    
    folderName = f'{assignmentName}-{name}'
    print(f'{repoPath}\\{folderName}')
    
    #Find if default branch is master or main
    defaultBranch = ""
    
    checkBranchCmd = f'git ls-remote --heads git@github.com:{orgName}/{folderName} '
    try:  #This can likely be removed in a few years once everyone has transitioned to main instead of master
            
        if (len(subprocess.check_output(checkBranchCmd + "main", shell=True)) > 0):
            defaultBranch = 'main'
        elif (len(subprocess.check_output(checkBranchCmd + "master", shell=True)) > 0):
            defaultBranch = 'master'
        else:
            print("Whoa, something is really wrong.  Go see why there isn't a main/master branch")
            break
    except subprocess.CalledProcessError as e:
        if e.returncode == 128: #Repo does not exist, or incorrect permissions
            print( f'Error: {orgName}/{folderName} does not exist')
            continue            #Skip everything else!
        else:
            print(e)
            raise e  
    
    
    if os.path.exists(f'{repoPath}\\{folderName}'):   #Check to see if the project has been cloned before
        
        os.chdir(f'{repoPath}/{folderName}')          #Change the dir to the repo's folder
        
        #Check to see if Feedback branch exists
        
        checkBranchCmd = f'git ls-remote --heads git@github.com:{orgName}/{folderName} '
        if (len(subprocess.check_output(checkBranchCmd + "feedback", shell=True)) != 0):  #check if feedback branch exists.
        
            noisy(subprocess.check_output('git add --all', shell=True))       #Stage all (new, modified, deleted) files
            #os.system('git commit -m '+ commitMessage)                        #Commit all staged changes  #NB: git reset HEAD~ If you want to undo a commit that is local.
            try:
                noisy(subprocess.check_output('git commit -m '+ commitMessage, shell=True))                #Commit all (new, modified, deleted) files
            except subprocess.CalledProcessError as e:  #If nothing to commit this command errors out with a return value of 1
                if e.returncode != 1:                   #So catch the error unless it's not 1, then let it through
                    print(e)
                    raise e
                
            noisy(subprocess.check_output('git push', shell=True))                #Push Changes (if none exist this command does nothing)  <--This should probaby be after the commit in the try except, but don't want to spend the time to test the change to make sure nothing breaks.  It works as is.

          
            
            #print(int(subprocess.check_output('git rev-list --count main...feedback', shell=True))) 
            if (int(subprocess.check_output('git rev-list --count main...feedback', shell=True)) > 0):  #If feedback branch is ahead
                
                try:
                    noisy(subprocess.check_output('gh pr close feedback', shell=True))  #Close the current pull request if any exist
                except subprocess.CalledProcessError as e:  #If no PR exists this command errors out with a return value of 1
                    if e.returncode != 1:                   #So catch the error unless it's not 1, then let it through
                        print(e)
                        raise e

                try:#Oringally this just made a single pull request, but I wanted to backup each branch just in case it was needed later
                    #To do that the feedback branch is renamed based on the current date/time and a PR is created from the renamed branch
                    
                    noisy(subprocess.check_output('git checkout feedback', shell=True))   #Ensure we are on feedback (probably not needed)
                    backup_name = f'feedback_{round(time.time())}'
                                    
                    noisy(subprocess.check_output(f'git branch -m {backup_name}', shell=True))#Rename local feedback branch
                    noisy(subprocess.check_output(f'git push origin -u {backup_name}', shell=True))#Push renamed branch to cloud
                    
                    noisy(subprocess.check_output('gh pr create --fill --title "Feedback from Mr. Brooks"', shell=True))    #Create new Pull Request
                                    
                    noisy(subprocess.check_output('git push origin --delete feedback', shell=True))#Delete the feedback branch now that we are done with it
                    noisy(subprocess.check_output('git checkout '+defaultBranch, shell=True))   #Check out the default branch
                    
                    
                except Exception as e:
                    print("Something unexpected happened, check to see what happened while creating the pull request and renaming the old branch")
                    print(e)
                    raise e
                    
                
            else:
                print('No changes found - no Pull Request created')
                
        else:
            print('Feedback branch does not exist - no Pull Request created')
         
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


