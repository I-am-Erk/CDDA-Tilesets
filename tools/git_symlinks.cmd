@echo off
echo Attention! You need to enable 'Developer mode' first.
echo Read how to do it here: 
echo.
echo https://learn.microsoft.com/en-us/windows/apps/get-started/developer-mode-features-and-debugging
echo.
echo Keep this window open, and enable this feature. Then press any key.
pause >nul
git config --global core.symlinks true
git config --unset core.symlinks
git reset --hard
echo.
echo Now you can follow symlinks in repository. 
pause