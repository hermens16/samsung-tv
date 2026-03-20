Set WshShell = CreateObject("WScript.Shell")

WshShell.CurrentDirectory = "C:\Users\User\Dev\samsung-tv"

WshShell.Run """C:\Users\User\AppData\Local\Programs\Python\Python313\python.exe"" update_playlist.py", 0, False