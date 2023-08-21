# Github-Teacher-Tools
This repo contains tools I use to manage my student github repos.  The scripts are written in Python 3.  These scripts are originally based on C Cannon's [Christopher Cannon](https://github.com/ccannon94/github-classroom-utilties)

### WorkFlow
- Previously I was just making changes to the main branch as students worked to provide feedback.  This occasionally caused some conflicts that had to be resolved.  I now work in a separate feedback branch and then create and merge a pull request with the feedback for the students.

**Workflow:**
1. Create Assignment in [Github Classroom](https://classroom.github.com/) and share assignment link with class.
2. Students work on Assignment by doing the following.
    * Students click link and create an assignment repo for themselves.
    * Students work on assignment in repl.it or IDE of their choice and submit work completed back to git repo (daily)
3. Teacher clones assignment, creates feedback branch and synchs with main branch as necessary. [GetReadyForGrading.py](GetReadyForGrading.py)
4. Teacher provides comments, feedback or grade in the feedback branch.
5. Teacher commits changes and sends them to students as a pull request. [SendFeedback.py](SendFeedback.py)
     * The current Feedback branch is renamed as a part of this process based on the current date/time.  This allows a backup of every feedback branch merged in to still exits with minimal risk of merge conflicts.
7. Student reviews feedback/grade and can choose to integrate back into their code base (or not).

## Requirements
- [GIT](https://git-scm.com/) 
- [GitHub CLI](https://cli.github.com/)
- Set up an SSH key in your OS and register it with Github 

## GetReadyForGrading.py
Gets and Updates all students repos to make sure they are ready for grading/feedback.

- If Repo not already cloned: Clones repo and creates feedback branch
- If Repo exists, stashes all uncommited changes, updates feedback branch from main branch, and restores stash

## SendFeedback.py
Once all repos pulled using getReadyForGrading.py have been graded, this script can be run to push the feedback to all of the students.
- Creates feedback and pushes it back to the repo as a pull request.


# Deprecated Files
All the files listed below are no longer being maintained but can be found in the Old Files directory.

## PushAllCommits.py
Pushes all commits that exist in the active branch to all repos.

## HomeworkCheck.py

(Old Workflow) Python 3 utility to check last update of student repositories created using [GitHub Classroom](https://classroom.github.com).

### Pre-state (for all above scripts)
Requires SSH key paired with GitHub Account

There must exist a GitHub classroom assignment.

The user must have a plain text file (.txt or .csv) with the GitHub usernames of all students separated by new lines.

### Getting SSH Key Set up with your github account
- **Step 1**: Install git locally if you have not already done so: https://git-scm.com/downloads
- **Step 2**: https://inchoo.net/dev-talk/how-to-generate-ssh-keys-for-git-authorization/

  *Note:* If you set up a password when creating your SSH key the scrips attached will likely not work.
- **Step 3**: https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/adding-a-new-ssh-key-to-your-github-account
- **Step 4**: Test by running the following command in the shell: ssh -T git@github.com
        If you see "Hi hdsbbrooks! You've successfully authenticated, but GitHub does not provide shell access." all is good =)

        Reference: https://gist.github.com/developius/c81f021eb5c5916013dc


---

## MossSetup-nonCMD.py

**NOTE: This script does not yet handle multiple branches in an assignment**

Python3 command line utility to clone all repositories from an assignment created using [GitHub Classroom](https://classroom.github.com) and prepare them for evaluation using [MOSS plagiarism detection](https://theory.stanford.edu/~aiken/moss/).  This is a modified script written by [Christopher Cannon](https://github.com/ccannon94/github-classroom-utilties)

### MOSS Directory Structure

The goal of this script is to transfer source files from and IDE project structure to the required MOSS file structure.

```
| - solution_directory
  | - student1
    | - classA.java
    | - classB.java
    | - ...
  | - student2
    | - ...
  | - student3
    | - ...
  | - ...
```

### Pre-state

There must exist a GitHub classroom assignment.

The user must have a plain text file (.txt or .csv) with the GitHub usernames of all students separated by new lines.

There must exist an empty directory that will hold GitHub repositories and the MOSS directory structure.

The user must have the CloneAssignment.py script from this repository on their machine.
