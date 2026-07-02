# SETUP LOG

## Commands used during setup

### 1.Creating Folder Structure
```bash
mkdir -p task_1/src task_1/data
touch task_1/README.md task_1/requirements.txt task_1/setup_log.md task_1/linux_commands.md
touch task_1/src/hello.py task_1/data/sample.txt
touch .gitignore
```

### 2. Initialised Git
```bash
git init
git remote add origin https://github.com/YOUR_USERNAME/Synergy_TP.git
```

### 3.Creating python Virtual Environment
```bash
python -m venv venv
source venv/Scripts/activate
```

### 4.Installing Package & Generate requirements.txt
```bash
pip install numpy
pip freeze > task_1/requirements.txt
```

### 5. Ran the Python script
```bash
python task_1/src/hello.py
```

### 6.Commit change and push to GitHub
```bash
git add .
git commit -m "Add Task 1: venv setup, hello.py, linux commands"
git push origin main
```
