import re
import os
import requests
from datetime import datetime

# CONFIG
url_playlist = "http://127.0.0.1:8182/playlist.m3u8"
arquivo_bruto = "samsung.m3u"
arquivo_final = "samsung_traduzida.m3u"

print("🌐 Baixando playlist...")

r = requests.get(url_playlist, timeout=10)
conteudo = r.text

if "#EXTINF" not in conteudo:
    print("❌ Playlist inválida!")
    exit()

with open(arquivo_bruto, "w", encoding="utf-8") as f:
    f.write(conteudo)

print("✅ Playlist salva!")

# 🔥 MAPA COMPLETO (inclui coreano)
mapa_grupos = {

    # COREANO (🔥 AGORA FUNCIONA)
    "예능": "VARIEDADES",
    "드라마": "SÉRIES",
    "뉴스": "NOTÍCIAS",
    "스포츠": "ESPORTES",
    "어린이": "INFANTIL",
    "시사/교양": "DOCUMENTÁRIOS",
    "음악": "MÚSICA",
    "영화": "FILMES",
    "라이프스타일": "VARIEDADES",
    "실시간": "AO VIVO",
    "쇼핑": "SHOPPING",

    # OUTROS (mantém os seus)
    "MOVIES": "FILMES",
    "FILM": "FILMES",
    "CINE": "FILMES",

    "SERIES": "SÉRIES",
    "TV SHOWS": "SÉRIES",

    "NEWS": "NOTÍCIAS",
    "NOTICIAS": "NOTÍCIAS",

    "SPORTS": "ESPORTES",
    "SPORT": "ESPORTES",

    "MUSIC": "MÚSICA",

    "KIDS": "INFANTIL",

    "DOCUMENTARY": "DOCUMENTÁRIOS",

    "ENTERTAINMENT": "VARIEDADES",
}

print("⚙️ Traduzindo grupos...")

with open(arquivo_bruto, "r", encoding="utf-8", errors="ignore") as f:
    linhas = f.readlines()

saida = []

for linha in linhas:

    if linha.startswith("#EXTINF"):

        nome = linha.split(",")[-1].strip()

        grupo = None

        if 'group-title="' in linha:
            grupo_original = linha.split('group-title="')[1].split('"')[0].strip()

            # 🔥 AQUI ESTÁ A CORREÇÃO
            grupo = mapa_grupos.get(grupo_original, grupo_original)

        linha = re.sub(r'group-title="[^"]*"', '', linha)

        metadados = linha.split(",")[0]

        nova = f'{metadados} group-title="{grupo}",{nome}\n'

        saida.append(nova)

    else:
        saida.append(linha)

with open(arquivo_final, "w", encoding="utf-8") as f:
    f.write(f'#EXTM3U updated="{datetime.now()}"\n')
    for linha in saida:
        f.write(linha)

print("✅ Grupos traduzidos corretamente!")

# GIT
os.system("git add .")
os.system('git commit -m "Tradução correta dos grupos (coreano incluído)"')
os.system("git push")

print("🚀 Concluído!")
