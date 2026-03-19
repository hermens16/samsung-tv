@echo off

cd /d C:\Users\User\Dev\samsung-tv

echo 🔄 Subindo Docker...
docker-compose up -d

echo ⏳ Aguardando servidor...
timeout /t 10 >nul

echo 📥 Baixando playlist original...
curl http://localhost:8182/playlist.m3u -o samsung.m3u

echo ⚙️ Processando playlist...
C:\Users\User\AppData\Local\Programs\Python\Python313\python.exe update_playlist.py

echo ✅ Finalizado
exit