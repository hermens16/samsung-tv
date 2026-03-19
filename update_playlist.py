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

# 🔥 DETECÇÃO DE TEXTO ASIÁTICO (coreano, japonês, chinês)
def tem_oriental(texto):
    return re.search(r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uac00-\ud7af]', texto)

# 🔥 MAPA GLOBAL (sem depender de upper pra oriental)
mapa_grupos = {
    "MOVIES": "FILMES",
    "FILMS": "FILMES",
    "FILM": "FILMES",
    "CINE": "FILMES",

    "SERIES": "SÉRIES",
    "SERIE": "SÉRIES",
    "TV SHOWS": "SÉRIES",

    "NEWS": "NOTÍCIAS",
    "NOTICIAS": "NOTÍCIAS",

    "SPORT": "ESPORTES",
    "SPORTS": "ESPORTES",

    "MUSIC": "MÚSICA",
    "MUSIK": "MÚSICA",

    "KIDS": "INFANTIL",

    "DOCUMENTARY": "DOCUMENTÁRIOS",

    "ANIME": "ANIME",

    "ENTERTAINMENT": "VARIEDADES",
}

print("⚙️ Traduzindo...")

with open(arquivo_bruto, "r", encoding="utf-8", errors="ignore") as f:
    linhas = f.readlines()

saida = []

for linha in linhas:

    if linha.startswith("#EXTINF"):

        nome = linha.split(",")[-1].strip()

        # 🔥 LIMPA NOME ORIENTAL (mantém legível)
        if tem_oriental(nome):
            nome = re.sub(r'[^\x00-\x7F]+', '', nome)

        nome = nome.upper()

        grupo = None

        if 'group-title="' in linha:
            grupo_original = linha.split('group-title="')[1].split('"')[0].strip()

            # 🔥 SE FOR ORIENTAL → TRADUZ PRA "VARIEDADES" (ou outro que quiser)
            if tem_oriental(grupo_original):
                grupo = "VARIEDADES"
            else:
                grupo = mapa_grupos.get(grupo_original.upper(), grupo_original)

        # remove grupo antigo
        linha = re.sub(r'group-title="[^"]*"', '', linha)

        metadados = linha.split(",")[0]

        if grupo:
            nova = f'{metadados} group-title="{grupo}",{nome}\n'
        else:
            nova = f'{metadados},{nome}\n'

        saida.append(nova)

    else:
        saida.append(linha)

# SALVA
with open(arquivo_final, "w", encoding="utf-8") as f:
    f.write(f'#EXTM3U updated="{datetime.now()}"\n')
    for linha in saida:
        f.write(linha)

print("✅ Tradução concluída!")

# GIT
os.system("git add .")
os.system('git commit -m "Correção tradução oriental"')
os.system("git push")

print("🚀 Concluído!")
