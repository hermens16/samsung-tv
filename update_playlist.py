import re
import os
import requests
import unicodedata
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

# 🔥 NORMALIZA TEXTO (REMOVE ACENTO)
def normalizar(texto):
    texto = unicodedata.normalize("NFKD", texto)
    texto = texto.encode("ASCII", "ignore").decode("ASCII")
    return texto.upper().strip()

# 🔥 CLASSIFICADOR INTELIGENTE
def traduzir_grupo(grupo):

    g = normalizar(grupo)

    # COREANO (direto)
    if grupo in ["예능", "드라마", "뉴스", "스포츠", "어린이", "시사/교양", "음악", "영화"]:
        return {
            "예능": "VARIEDADES",
            "드라마": "SÉRIES",
            "뉴스": "NOTÍCIAS",
            "스포츠": "ESPORTES",
            "어린이": "INFANTIL",
            "시사/교양": "DOCUMENTÁRIOS",
            "음악": "MÚSICA",
            "영화": "FILMES"
        }.get(grupo, "VARIEDADES")

    # 🔥 PALAVRA-CHAVE
    if "SPORT" in g:
        return "ESPORTES"

    if "NEWS" in g or "NOTIC" in g or "ACTUAL" in g:
        return "NOTÍCIAS"

    if "MOVIE" in g or "FILM" in g or "CINE" in g:
        return "FILMES"

    if "SERIE" in g:
        return "SÉRIES"

    if "DOCU" in g or "HISTORY" in g or "NATURE" in g:
        return "DOCUMENTÁRIOS"

    if "KID" in g or "NIÑ" in g or "JEUN" in g or "BAMB" in g:
        return "INFANTIL"

    if "MUSIC" in g or "MUSIK" in g or "MUSIQUE" in g:
        return "MÚSICA"

    if "ANIME" in g:
        return "ANIME"

    if "REALITY" in g:
        return "VARIEDADES"

    if "LIFESTYLE" in g or "FOOD" in g or "TRAVEL" in g:
        return "VARIEDADES"

    if "ENTERTAIN" in g or "DIVERT" in g:
        return "VARIEDADES"

    return grupo  # fallback

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

print("✅ Tradução FINAL concluída!")

# GIT
os.system("git add .")
os.system('git commit -m "Tradução inteligente completa dos grupos"')
os.system("git push")

print("🚀 Concluído!")
