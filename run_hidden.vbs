Set WshShell = CreateObject("WScript.Shell")

python = """C:\Users\User\AppData\Local\Programs\Python\Python313\python.exe"""
pasta = "C:\Users\User\Dev\samsung-tv"

' roda tudo com caminho absoluto
WshShell.Run python & " """ & pasta & "\update_playlist.py""", 0, True
WshShell.Run python & " """ & pasta & "\remover_duplicados.py""", 0, True