# Python 3
# PushAllCommits.py
# Mass push all commits made locally in each repo to remote

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
        pushCmd = 'git push'                 #Push any commits
                
        os.chdir(f'{repoPath}/{folderName}')          #Change the dir to the repo's folder
        
        os.system(pushCmd)
        
        os.chdir(startingPath)                        #Reset the path back to the starting folder
    else:                                             #Project has not been cloned before, so grab it.
        println(f"{assignmentName}-{name} Repo does not exist - Skipping")
                
print("Finished!")

