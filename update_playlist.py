import re
import os
import requests
from datetime import datetime

# 🔥 CONFIG
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

# 🔥 MAPA GLOBAL (MULTI-IDIOMA)
mapa_grupos = {

    # 🎬 FILMES
    "MOVIES": "FILMES", "MOVIE": "FILMES", "FILM": "FILMES",
    "FILME": "FILMES", "CINE": "FILMES", "CINÉMA": "FILMES",
    "영화": "FILMES",

    # 📺 SÉRIES
    "SERIES": "SÉRIES", "SERIE": "SÉRIES", "TV SERIES": "SÉRIES",
    "SERIEN": "SÉRIES", "SERIE TV": "SÉRIES", "SÉRIES TV": "SÉRIES",
    "드라마": "SÉRIES",

    # 📰 NOTÍCIAS
    "NEWS": "NOTÍCIAS", "NOTICIAS": "NOTÍCIAS",
    "ACTUALITÉS": "NOTÍCIAS", "NEWS & OPINION": "NOTÍCIAS",
    "REGIONAL NEWS": "NOTÍCIAS", "ENGLISH NEWS": "NOTÍCIAS",
    "HINDI NEWS": "NOTÍCIAS",
    "뉴스": "NOTÍCIAS",

    # ⚽ ESPORTES
    "SPORT": "ESPORTES", "SPORTS": "ESPORTES",
    "SPORTS & OUTDOORS": "ESPORTES",
    "MOTOR SPORTS": "ESPORTES",
    "DEPORTE": "ESPORTES",
    "스포츠": "ESPORTES",

    # 🎵 MÚSICA
    "MUSIC": "MÚSICA", "MUSIK": "MÚSICA", "MUSICA": "MÚSICA",
    "MUSIQUE": "MÚSICA", "MÚSICA": "MÚSICA",
    "음악": "MÚSICA",

    # 👶 INFANTIL
    "KIDS": "INFANTIL", "NIÑOS": "INFANTIL",
    "BAMBINI": "INFANTIL", "JEUNESSE": "INFANTIL",
    "어린이": "INFANTIL",

    # 📚 DOCUMENTÁRIOS
    "DOCUMENTARY": "DOCUMENTÁRIOS", "DOCUMENTARIES": "DOCUMENTÁRIOS",
    "DOCUMENTAIRES": "DOCUMENTÁRIOS", "DOCUMENTALES": "DOCUMENTÁRIOS",
    "DOCUMENTARI": "DOCUMENTÁRIOS",
    "DOKUS & WISSEN": "DOCUMENTÁRIOS",

    # 🎌 ANIME
    "ANIME": "ANIME", "ANIME & GAMING": "ANIME",

    # 🎭 VARIEDADES
    "ENTERTAINMENT": "VARIEDADES",
    "DIVERTISSEMENT": "VARIEDADES",
    "ENTRETENIMIENTO": "VARIEDADES",
    "INTRATTENIMENTO": "VARIEDADES",
    "예능": "VARIEDADES",

    # 🍔 LIFESTYLE
    "LIFESTYLE": "VARIEDADES",
    "HOME & FOOD": "VARIEDADES",
    "FOOD & TRAVEL": "VARIEDADES",
    "VOYAGES ET GASTRONOMIE": "VARIEDADES",
    "CUCINA & VIAGGI": "VARIEDADES",
    "라이프스타일": "VARIEDADES",

}

print("⚙️ Traduzindo grupos...")

with open(arquivo_bruto, "r", encoding="utf-8", errors="ignore") as f:
    linhas = f.readlines()

saida = []

for linha in linhas:

    if linha.startswith("#EXTINF"):

        nome = linha.split(",")[-1].strip().upper()

        # limpa caracteres estranhos do nome
        nome = re.sub(r'[^\w\s\-\&]', '', nome)

        grupo = None

        if 'group-title="' in linha:
            grupo_original = linha.split('group-title="')[1].split('"')[0].strip()
            grupo_upper = grupo_original.upper()

            grupo = mapa_grupos.get(grupo_upper, grupo_original)

        linha = re.sub(r'group-title="[^"]*"', '', linha)

        metadados = linha.split(",")[0]

        if grupo:
            nova = f'{metadados} group-title="{grupo}",{nome}\n'
        else:
            nova = f'{metadados},{nome}\n'

        saida.append(nova)

    else:
        saida.append(linha)

with open(arquivo_final, "w", encoding="utf-8") as f:
    f.write(f'#EXTM3U updated="{datetime.now()}"\n')
    for linha in saida:
        f.write(linha)

print("✅ Playlist organizada e traduzida!")

# 🔥 GIT
os.system("git add .")
os.system('git commit -m "Organização por grupos + tradução completa"')
os.system("git push")
