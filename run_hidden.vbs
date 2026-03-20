Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\Users\User\Dev\samsung-tv"
WshShell.Run "cmd /c python update_playlist.py", 0, False