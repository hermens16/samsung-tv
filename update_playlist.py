import re
import os
import requests
import unicodedata
from datetime import datetime

# 🔥 CONFIG
url_playlist = "http://127.0.0.1:8182/playlist.m3u8"
arquivo_bruto = "samsung.m3u"
arquivo_final = "samsung_traduzida.m3u"

print("🌐 Baixando playlist...")

try:
    r = requests.get(url_playlist, timeout=15)
    conteudo = r.text
except:
    print("❌ Erro ao baixar playlist")
    exit()

if "#EXTINF" not in conteudo:
    print("❌ Playlist inválida!")
    exit()

with open(arquivo_bruto, "w", encoding="utf-8") as f:
    f.write(conteudo)

print("✅ Playlist salva!")

# 🔥 NORMALIZA TEXTO (remove acento + padroniza)
def normalizar(txt):
    txt = unicodedata.normalize("NFKD", txt)
    txt = txt.encode("ASCII", "ignore").decode("ASCII")
    return txt.upper().strip()

# 🔥 TRADUTOR DE GRUPOS
def traduzir_grupo(grupo_original):

    # 🔥 COREANO
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
        return mapa_coreano[grupo_original]

    g = normalizar(grupo_original)

    # 🔥 ESPORTES
    if any(x in g for x in ["SPORT", "DEPORTE", "CALCIO", "FUSSBALL", "MOTOR"]):
        return "ESPORTES"

    # 🔥 NOTÍCIAS
    if any(x in g for x in ["NEWS", "NOTIC", "ACTUAL"]):
        return "NOTÍCIAS"

    # 🔥 FILMES
    if any(x in g for x in ["MOVIE", "FILM", "CINE"]):
        return "FILMES"

    # 🔥 SÉRIES
    if any(x in g for x in ["SERIE", "DRAMA", "CRIMEN", "CLASSIC TV"]):
        return "SÉRIES"

    # 🔥 DOCUMENTÁRIOS
    if any(x in g for x in ["DOCU", "HISTORY", "NATURE", "WISSEN", "INFOTAIN"]):
        return "DOCUMENTÁRIOS"

    # 🔥 INFANTIL
    if any(x in g for x in ["KID", "NIÑ", "JEUN", "BAMB"]):
        return "INFANTIL"

    # 🔥 MÚSICA
    if any(x in g for x in ["MUSIC", "MUSIK", "MUSIQUE"]):
        return "MÚSICA"

    # 🔥 RELIGIOSO
    if "DEVOTIONAL" in g:
        return "RELIGIOSO"

    # 🔥 VARIEDADES
    if any(x in g for x in [
        "ENTERTAIN", "REALITY", "COMEDY", "COMEDIA",
        "INTRATTEN", "DIVERT", "AMBIANCE"
    ]):
        return "VARIEDADES"

    # 🔥 COMIDA / VIAGEM / LIFESTYLE
    if any(x in g for x in [
        "LIFESTYLE", "FOOD", "TRAVEL",
        "CUCINA", "VIAGGI", "VOYAGES", "GASTRONOMIE", "VIAJES"
    ]):
        return "VARIEDADES"

    return grupo_original  # fallback (não perde canal)

print("⚙️ Traduzindo grupos...")

with open(arquivo_bruto, "r", encoding="utf-8", errors="ignore") as f:
    linhas = f.readlines()

saida = []

for linha in linhas:

    if linha.startswith("#EXTINF"):

        nome = linha.split(",")[-1].strip().upper()

        grupo = None

        if 'group-title="' in linha:
            grupo_original = linha.split('group-title="')[1].split('"')[0].strip()
            grupo = traduzir_grupo(grupo_original)

        # remove grupo antigo
        linha = re.sub(r'group-title="[^"]*"', '', linha)

        metadados = linha.split(",")[0]

        nova = f'{metadados} group-title="{grupo}",{nome}\n'
        saida.append(nova)

    else:
        saida.append(linha)

# 🔥 SALVA ARQUIVO FINAL
with open(arquivo_final, "w", encoding="utf-8") as f:
    f.write(f'#EXTM3U updated="{datetime.now()}"\n')
    for linha in saida:
        f.write(linha)

print("✅ Playlist traduzida com sucesso!")

# 🔥 GIT
print("📤 Enviando para GitHub...")

os.system("git add .")
os.system('git commit -m "Tradução completa dos grupos IPTV"')
os.system("git push")

print("🚀 Concluído!")
