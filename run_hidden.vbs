If WScript.Arguments.Count = 0 Then
    Set WshShell = CreateObject("WScript.Shell")
    
    ' 🔥 chama ele mesmo invisível
    WshShell.Run "wscript """ & WScript.ScriptFullName & """ invisivel", 0, False
    WScript.Quit
End If

' 🔥 AQUI roda normal (sem quebrar nada)
Set WshShell = CreateObject("WScript.Shell")

caminho = """C:\Users\User\AppData\Local\Programs\Python\Python313\python.exe"""

WshShell.CurrentDirectory = "C:\Users\User\Dev\samsung-tv"

WshShell.Run caminho & " update_playlist.py", 1, True
WshShell.Run caminho & " remover_duplicados.py", 1, True