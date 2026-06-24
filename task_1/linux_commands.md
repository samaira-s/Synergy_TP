# Linux Commands

## 1. pwd
**Command:** `pwd`
**What it does:** Prints the current working directory (where you are in the file system)
**Output:** `/c/Users/Samaira Singh/Synergy_TP`

## 2. ls
**Command:** `ls task_1`
**What it does:** Lists all files and folders inside a directory
**Output:** `README.md  data/  linux_commands.md  requirements.txt  setup_log.md  src/`

## 3. ls -la
**Command:** `ls -la task_1`
**What it does:** Lists all files including hidden files, with detailed info like permissions, size, and date modified
**Output:** total 10
drwxr-xr-x 1 Samaira Singh 197121   0 Jun 24 14:44 ./
drwxr-xr-x 1 Samaira Singh 197121   0 Jun 24 18:55 ../
-rw-r--r-- 1 Samaira Singh 197121 568 Jun 24 19:42 README.md
drwxr-xr-x 1 Samaira Singh 197121   0 Jun 24 14:45 data/
-rw-r--r-- 1 Samaira Singh 197121   0 Jun 24 14:44 linux_commands.md
-rw-r--r-- 1 Samaira Singh 197121  14 Jun 24 18:55 requirements.txt
-rw-r--r-- 1 Samaira Singh 197121   0 Jun 24 14:44 setup_log.md
drwxr-xr-x 1 Samaira Singh 197121   0 Jun 24 14:45 src/

## 4. cd
**Command:** `cd task_1`
**What it does:** Changes your current directory to the specified folder
**Output:** (no output, just moves you into the folder)

## 5. mkdir
**Command:** `mkdir -p task_1/src task_1/data`
**What it does:** Creates folders. `-p` creates parent folders too if they don't exist
**Output:** (no output if successful)

## 6. touch
**Command:** `touch task_1/README.md`
**What it does:** Creates an empty file
**Output:** (no output if successful)

## 7. cat
**Command:** `cat task_1/requirements.txt`
**What it does:** Prints the contents of a file to the screen
**Output:** `numpy==2.5.0`

## 8. echo
**Command:** `echo "Hello World"`
**What it does:** Prints text to the screen
**Output:** `Hello World`

## 9. cp
**Command:** `cp task_1/README.md task_1/README_backup.md`
**What it does:** Copies a file from one location to another
**Output:** (no output if successful)

## 10. mv
**Command:** `mv task_1/README_backup.md task_1/README_copy.md`
**What it does:** Moves or renames a file
**Output:** (no output if successful)

## 11. rm
**Command:** `rm task_1/README_copy.md`
**What it does:** Deletes a file permanently
**Output:** (no output if successful)

## 12. grep
**Command:** `grep "numpy" task_1/requirements.txt`
**What it does:** Searches for a pattern inside a file and prints matching lines
**Output:** `numpy==2.5.0`

## 13. find
**Command:** `find task_1 -name "*.py"`
**What it does:** Searches for files matching a pattern inside a folder
**Output:** `task_1/src/hello.py`

## 14. head
**Command:** `head task_1/requirements.txt`
**What it does:** Prints the first 10 lines of a file
**Output:** `numpy==2.5.0`

## 15. tail
**Command:** `tail task_1/requirements.txt`
**What it does:** Prints the last 10 lines of a file
**Output:** `numpy==2.5.0`

## 16. wc
**Command:** `wc task_1/requirements.txt`
**What it does:** Counts lines, words, and characters in a file
**Output:** `1  1  13 task_1/requirements.txt`

## 17. chmod
**Command:** `chmod +x task_1/src/hello.py`
**What it does:** Changes file permissions. `+x` makes the file executable
**Output:** (no output if successful)