Set WshShell = CreateObject("WScript.Shell")

WshShell.CurrentDirectory = "C:\Users\User\Dev\samsung-tv"

' 🔥 1 - Atualiza e traduz playlist
WshShell.Run """C:\Users\User\AppData\Local\Programs\Python\Python313\python.exe"" update_playlist.py", 0, True

' 🔥 2 - Remove duplicados e gera lista final
WshShell.Run """C:\Users\User\AppData\Local\Programs\Python\Python313\python.exe"" remover_duplicados.py", 0, True