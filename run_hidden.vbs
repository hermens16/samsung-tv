Set WshShell = CreateObject("WScript.Shell")

python = """C:\Users\User\AppData\Local\Programs\Python\Python313\python.exe"""

script1 = """C:\Users\User\Dev\samsung-tv\update_playlist.py"""
script2 = """C:\Users\User\Dev\samsung-tv\remover_duplicados.py"""

' 🔥 EXECUÇÃO VISÍVEL PRA DEBUG (IMPORTANTE AGORA)
WshShell.Run python & " " & script1, 1, True
WshShell.Run python & " " & script2, 1, True