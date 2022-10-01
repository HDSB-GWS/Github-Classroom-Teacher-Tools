import os
import shutil
import subprocess
import random
import time
from pathlib import Path


delayTime = 30  #Time to wait between refreshes so that we don't hammer the git api too quickly (Don't want to get rate limited)
isQuiet = True  #This script really spams the console so os.system commands replaced with subprocess and can be muted via isQuiet
debug = False   #Enable debugging output    

#Questions title is added before the list of questions to the readme.md file in the repo.
#The script also uses this title to see if questions have already been added to a repo.
#questionsTitle = '## Exam Questions\n' 
questionsTitle = '## Quiz Questions\n'
commitMessage = "Uploading Quiz Questions"

def noisy(noiseIn): #Only allow console output for noisy commands if not isQuiet
    if not isQuiet:
        print(noiseIn.decode("utf-8"))

#Load all of the files in from a given path and select one randomly.  
#Return the full path of the selected file
def chooseRandomFile(path, fileExtension):
    fileList = []
    for file in os.listdir(path):
        if file.endswith(f'.{fileExtension}'):
            fileList.append(file)
    return path+'\\'+random.choice(fileList)


#Google Classroom Info
orgName = 'HDSB-GWS-XXXXX'                 #The name of your github organization
rosterPath = r'C:\SOMEPATH\ics2oq2.txt'    #Path to your class roster (one github username per line)

#Assignment Info
assignmentName = 'example-repo'            #The repo assignment name in github classroom
repoPath = r'C:\SOMEPATH\ExampleRepo'      #The path to save the repos that are downloaded

#Question setup
#The script will randomly select and move numQuestionsPerFolder questions from each folder in the list 
# questionFolders. It will then commit and push the questions online for the student to complete.
numQuestionsPerFolder = 1
questionFolders = []

#Folder Setup
#Append a path and file extension pair for questionFolders for each folder you want to pull questions from
questionFolders.append([r'C:\some\example\path1', 'java'])
questionFolders.append([r'C:\some\example\path2', 'py'])
questionFolders.append([r'C:\some\example\path3', 'anyOtherExtension'])



   
#Start of the actual script
startingPath = os.getcwd()

with open(rosterPath) as f:
    names = f.read().splitlines()

roundNum = 0  #To count the number of rounds this script completes
while (len(names) > 0):
    futureTime = delayTime + time.time()

    for name in names:
        print(name)
        
        folderName = f'{assignmentName}-{name}'
        

        #Find if default branch is master or main
        defaultBranch = ""
        
        checkBranchCmd = f'git ls-remote --heads git@github.com:{orgName}/{folderName} '
        
        try:
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
                raise e

        
        print(f'{repoPath}/{folderName}')
        if os.path.exists(f'{repoPath}/{folderName}'):   #Check to see if the project has been cloned before
            
            os.chdir(f'{repoPath}/{folderName}')          #Set correct repo path

            noisy(subprocess.check_output('git checkout '+defaultBranch , shell=True))#Switch to default (aka student) branch
            
            readmePath = f'{repoPath}/{folderName}/README.md'
            try: 
                f = open(readmePath, 'r')
            except FileNotFoundError as e:
                #If file does not exist, let's make it
                filename = Path(readmePath)
                filename.touch(exist_ok=True)  
                f = open(filename)

            fileContents = f.readlines()
            f.close()

            #Check to see if this repo has already been processed by checking for content in readme.
            if questionsTitle in fileContents:
                print(f"{name} already had questions added to thier repo - removing from the list")
                names.remove(name)
                continue
                
            #Collect all the file paths to submit
            filePaths = []
            for path, fileExtension in questionFolders:
                numOfFiles = 0
                while numOfFiles < numQuestionsPerFolder:
                    #Grab a random file from folder
                    filePath = chooseRandomFile(path, fileExtension)
                    if filePath in filePaths:
                        continue #We already have this file included, so try again.
                        #TODO: Fix this laziness - Terrible way to do this - will get a never ending loop if there are not enough files to choose from in the folder
                    filePaths.append(filePath)
                    numOfFiles += 1
                    
            if (debug): print(filePaths)
 
            #Copy the files to the repo folder and update the readme.
            f = open(readmePath, 'a')
            f.write("\n")
            f.write(questionsTitle)
            for filePath in filePaths:
                #Copy to repo folder
                noisy(subprocess.check_output(f'copy "{filePath}" .' , shell=True))#Switch to default (aka student) branch
                #Write the file to the readme
                f.write(f'- {os.path.basename(filePath)}\n')
            f.close()
                
            
            #Make a commit to the repo with the questions.
            noisy(subprocess.check_output('git add --all', shell=True))       #Stage all (new, modified, deleted) files
            try:
                noisy(subprocess.check_output(f'git commit -m "{commitMessage}"', shell=True))                #Commit all (new, modified, deleted) files
            except subprocess.CalledProcessError as e:  #If nothing to commit this command errors out with a return value of 1
                if e.returncode != 1: #So catch the error unless it's not 1, then let it through
                    print(f"ERROR - {name} repo will not commit correctly as there is nothing to commit. Removing from the list, but need to manually check to see what's wrong")
                    names.remove(name)
                    continue
                else:                   
                    print(e)
                    raise e
            
            #Push the commit    
            noisy(subprocess.check_output('git push', shell=True))                #Push Changes (if none exist this command does nothing)  <--This should probaby be after the commit in the try except, but don't want to spend the time to test the change to make sure nothing breaks.  It works as is.
          
            print(f"{name} is done - questions added to repo - removing from the list")
            names.remove(name)
            
        else:#Project has not been cloned before, so grab it.
            #Clone Repo
            cloneCmd = f'git clone git@github.com:{orgName}/{folderName} {repoPath}\\{folderName}'
            
            if (debug): print(cloneCmd)
            os.system(cloneCmd)

            #The script will grab and upload the questions in the next pass
    


    print(f'The following students have not been fully processed:')
    for name in names:
        print(name)
    
    

    #Ensure there's a bit of a delay bewteen the next round so we are not hammering the servers
    waitTime = futureTime - time.time()
    roundNum += 1    
    print(f'Round {roundNum} completed, waiting {waitTime} seconds until the next round')
    
    if (waitTime > 0):
        time.sleep(waitTime)

    if (debug):
        #Break after a few rounds
        if roundNum > 5:
            break;

print("All names removed from list! Finished!")

  



