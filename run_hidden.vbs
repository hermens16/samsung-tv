Set WshShell = CreateObject("WScript.Shell")

caminho = """C:\Users\User\AppData\Local\Programs\Python\Python313\python.exe"""

WshShell.CurrentDirectory = "C:\Users\User\Dev\samsung-tv"

' 🔥 Script 1
WshShell.Run caminho & " update_playlist.py", 1, True

' 🔥 Script 2
WshShell.Run caminho & " remover_duplicados.py", 1, True