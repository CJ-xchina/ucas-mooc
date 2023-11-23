@echo off
setlocal

REM 设置变量
set COMMIT_MESSAGE=fix some bugs
set LOG_FILE=log.txt

REM 初始化仓库
echo Initializing repository...
git init

REM 添加文件到暂存区
echo Adding files to staging area...
git add .

REM 提交到本地仓库
echo Committing changes to local repository...
git commit -m "%COMMIT_MESSAGE%"

REM 拉取远程代码
echo Pulling changes from GitHub...
git pull origin main
IF %ERRORLEVEL% NEQ 0 (
    echo Pull failed. Resolve conflicts and run the script again.
    exit /b %ERRORLEVEL%
)

REM 检查远程仓库是否已存在
git remote -v | findstr "origin"
IF %ERRORLEVEL% EQU 0 (
    echo Remote origin already exists. Skipping remote add.
) ELSE (
    REM 添加远程仓库
    echo Adding remote repository...
    git remote add origin https://github.com/CJ-xchina/ucas-mooc.git
)

REM 推送到GitHub
echo Pushing changes to GitHub...
git push --set-upstream origin main
IF %ERRORLEVEL% NEQ 0 (
    echo Push failed. Check your credentials and try again.
    exit /b %ERRORLEVEL%
)
