# Github-Teacher-Tools

## HomeworkCheck.py

Python 3 utility to check last update of student repositories created using [GitHub Classroom](https://classroom.github.com).

### Pre-state

There must exist a GitHub classroom assignment.

The user must have a plain text file (.txt or .csv) with the GitHub usernames of all students separated by new lines.

### Usage




## MossSetup-nonCMD.py

**NOTE: This script does not yet handle multiple branches in an assignment**

Python3 command line utility to clone all repositories from an assignment created using [GitHub Classroom](https://classroom.github.com) and prepare them for evaluation using [MOSS plagiarism detection](https://theory.stanford.edu/~aiken/moss/).

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

### Usage

