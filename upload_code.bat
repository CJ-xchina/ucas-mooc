@echo off
setlocal

REM 设置变量
set COMMIT_MESSAGE=Initial commit
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
git pull origin master

REM 添加远程仓库
echo Adding remote repository...
git remote add origin https://github.com/CJ-xchina/ucas-mooc.git

REM 推送到GitHub
echo Pushing changes to GitHub...
git push --set-upstream origin master