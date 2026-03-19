start /B py app.py

timeout /t 10

py update_playlist.py

taskkill /im python.exe /f

git add samsung.m3u
git commit -m "auto update playlist"
git push