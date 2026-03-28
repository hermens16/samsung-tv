import re
import os
import requests
import unicodedata
from datetime import datetime

url_playlist = "https://raw.githubusercontent.com/BuddyChewChew/app-m3u-generator/refs/heads/main/playlists/samsungtvplus_all.m3u"
arquivo_bruto = "samsung.m3u"
arquivo_final = "samsung_traduzida.m3u"

print("🌐 Baixando playlist...")

try:
    r = requests.get(url_playlist, timeout=15)
    conteudo = r.text
except Exception as e:
    print("❌ Erro:", e)
    exit()

if "#EXTINF" not in conteudo:
    print("❌ Playlist inválida!")
    exit()

with open(arquivo_bruto, "w", encoding="utf-8") as f:
    f.write(conteudo)

def normalizar(txt):
    txt = unicodedata.normalize("NFKD", txt)
    txt = txt.encode("ASCII", "ignore").decode("ASCII")
    return txt.upper().strip()

def traduzir_grupo(grupo_original):

    mapa_coreano = {
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
        "쇼핑": "SHOPPING"
    }

    if grupo_original in mapa_coreano:
        traduzido = mapa_coreano[grupo_original]
        if traduzido in ["AO VIVO", "SHOPPING"]:
            return "VARIEDADES"
        return traduzido

    g = normalizar(grupo_original)

    if "BALL" in g:
        return "ESPORTES"

    if "NINOS" in g or "NIÑOS" in grupo_original.upper():
        return "INFANTIL"

    if "ANIME" in g:
        return "ANIME & TOKUSATSU"

    if any(x in g for x in ["NEWS","NOTIC","ACTUAL","OPINION","REGIONAL","ENGLISH","HINDI"]):
        return "NOTÍCIAS"

    if any(x in g for x in ["SPORT","DEPORTE","CALCIO","FUTB","MOTOR"]):
        return "ESPORTES"

    if any(x in g for x in ["KID","NIÑ","JEUN","BAMB"]):
        return "INFANTIL"

    if any(x in g for x in ["SERIE","DRAMA","CRIME","CRIMEN","TELENOVELA","REALITE","REALITY","CLASSIC TV","WESTERN"]):
        return "SÉRIES"

    if any(x in g for x in ["MOVIE","FILM","CINE","SCI-FI","HORROR"]):
        return "FILMES"

    if any(x in g for x in ["DOCU","HISTORY","NATURE","WISSEN","INFOTAIN"]):
        return "DOCUMENTÁRIOS"

    if any(x in g for x in ["MUSIC","MUSIK","MUSIQUE"]):
        return "MÚSICA"

    if any(x in g for x in ["ENTERTAIN","ENTRETEN","LATINO","GAME","COMEDY","COMEDIA","INTRATTEN","DIVERT","AMBIANCE","AO VIVO"]):
        return "VARIEDADES"

    if "DEVOTIONAL" in g:
        return "RELIGIOSO"

    if any(x in g for x in ["LIFESTYLE","FOOD","TRAVEL","CUCINA","VIAGGI","VOYAGES","GASTRONOMIE","VIAJES"]):
        return "VARIEDADES"

    return grupo_original

print("⚙️ Processando...")

with open(arquivo_bruto, "r", encoding="utf-8", errors="ignore") as f:
    linhas = f.readlines()

saida = []

for linha in linhas:

    if linha.startswith("#EXTINF"):

        nome = linha.split(",")[-1].strip().upper()
        grupo = "VARIEDADES"

        if 'group-title="' in linha:
            grupo_original = linha.split('group-title="')[1].split('"')[0].strip()
            grupo = traduzir_grupo(grupo_original)

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

print("✅ Traduzida gerada!")
