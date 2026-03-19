Set WshShell = CreateObject("WScript.Shell")

WshShell.Run "cmd /c cd /d C:\Users\User\Dev\samsung-tv && py app.py", 0, False