Set WshShell = CreateObject("WScript.Shell")

caminho = """C:\Users\User\AppData\Local\Programs\Python\Python313\python.exe"""

WshShell.CurrentDirectory = "C:\Users\User\Dev\samsung-tv"

' Script 1 - Atualiza playlist
WshShell.Run caminho & " update_playlist.py", 0, True

' Script 2 - Remove duplicados
WshShell.Run caminho & " remover_duplicados.py", 0, True