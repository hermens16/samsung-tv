import re
import os
import requests
import unicodedata
from datetime import datetime

url_playlist = "http://127.0.0.1:8182/playlist.m3u8"

arquivo_bruto = "samsung.m3u"
arquivo_traduzido = "samsung_traduzida.m3u"
arquivo_final = "samsung_final.m3u"

print("🌐 Baixando playlist...")

try:
    r = requests.get(url_playlist, timeout=15)
    conteudo = r.text
    print("Status:", r.status_code)
except Exception as e:
    print("❌ Erro:", e)
    exit()

if "#EXTINF" not in conteudo:
    print("❌ Playlist inválida!")
    exit()

with open(arquivo_bruto, "w", encoding="utf-8") as f:
    f.write(conteudo)

print("✅ Playlist salva!")

# ---------------- NORMALIZA ----------------

def normalizar(txt):
    txt = unicodedata.normalize("NFKD", txt)
    txt = txt.encode("ASCII", "ignore").decode("ASCII")
    return txt.upper().strip()

# ---------------- TRADUZ GRUPOS ----------------

def traduzir_grupo(grupo_original):

    g = normalizar(grupo_original)

    if "ANIME" in g:
        return "ANIME & TOKUSATSU"

    if any(x in g for x in ["NEWS", "NOTIC", "ACTUAL"]):
        return "NOTÍCIAS"

    if any(x in g for x in ["SPORT", "FUTB", "BALL"]):
        return "ESPORTES"

    if any(x in g for x in ["KID", "NIÑ"]):
        return "INFANTIL"

    if any(x in g for x in ["SERIE", "DRAMA", "REALITY"]):
        return "SÉRIES"

    if any(x in g for x in ["MOVIE", "FILM", "SCI"]):
        return "FILMES"

    if any(x in g for x in ["DOCU", "NATURE"]):
        return "DOCUMENTÁRIOS"

    if any(x in g for x in ["MUSIC", "MUSIK"]):
        return "MÚSICA"

    return "VARIEDADES"

# ---------------- TRADUZ PLAYLIST ----------------

print("⚙️ Traduzindo...")

with open(arquivo_bruto, "r", encoding="utf-8", errors="ignore") as f:
    linhas = f.readlines()

traduzida = []

for linha in linhas:

    if linha.startswith("#EXTINF"):

        nome = linha.split(",")[-1].strip().upper()
        grupo = "VARIEDADES"

        if 'group-title="' in linha:
            grupo_original = linha.split('group-title="')[1].split('"')[0]
            grupo = traduzir_grupo(grupo_original)

        linha = re.sub(r'group-title="[^"]*"', '', linha)
        metadados = linha.split(",")[0]

        nova = f'{metadados} group-title="{grupo}",{nome}\n'
        traduzida.append(nova)

    else:
        traduzida.append(linha)

with open(arquivo_traduzido, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    for l in traduzida:
        f.write(l)

print("✅ Traduzida pronta!")

# ---------------- REMOVER DUPLICADOS ----------------

print("🧹 Removendo duplicados...")

canais_vistos = set()
final = []

i = 0

while i < len(traduzida):

    if traduzida[i].startswith("#EXTINF"):

        extinf = traduzida[i]
        url = traduzida[i+1]

        nome = extinf.split(",")[-1].strip()

        grupo = ""
        if 'group-title="' in extinf:
            grupo = extinf.split('group-title="')[1].split('"')[0]

        chave = f"{grupo}|{nome}"

        if chave not in canais_vistos:
            canais_vistos.add(chave)
            final.append(extinf)
            final.append(url)

        i += 2
        continue

    i += 1

with open(arquivo_final, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    for l in final:
        f.write(l)

print("✅ Lista final pronta!")

# ---------------- GIT ----------------

print("📤 Enviando para o Git...")

os.system("git add .")
os.system('git commit -m "Atualização automática IPTV"')
os.system("git push")

print("🚀 FINALIZADO COM SUCESSO!")
