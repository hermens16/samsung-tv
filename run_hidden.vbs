Set WshShell = CreateObject("WScript.Shell")

WshShell.CurrentDirectory = "C:\Users\User\Dev\samsung-tv"

' 🔥 roda o primeiro script
WshShell.Run "cmd /c python update_playlist.py", 0, True

' 🔥 roda o segundo script
WshShell.Run "cmd /c python remover_duplicados.py", 0, True