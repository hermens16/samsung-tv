import re
import os
import requests
from datetime import datetime

# 🔥 CONFIG
url_playlist = "http://127.0.0.1:8182/playlist.m3u8"
arquivo_bruto = "samsung.m3u"
arquivo_final = "samsung_final.m3u"

print("🌐 Baixando playlist do servidor...")

try:
    r = requests.get(url_playlist, timeout=10)
    conteudo = r.text

    if "#EXTINF" not in conteudo:
        print("❌ Playlist veio vazia ou inválida!")
        exit()

    with open(arquivo_bruto, "w", encoding="utf-8") as f:
        f.write(conteudo)

    print("✅ Playlist bruta salva!")

except Exception as e:
    print("❌ Erro ao baixar playlist:", e)
    exit()

# 🔥 ORGANIZAÇÃO

mapa_grupos = {
    "MOVIES": "FILMES",
    "FILMS": "FILMES",
    "CINE": "FILMES",

    "SERIES": "SÉRIES",
    "TV SHOWS": "SÉRIES",

    "DOCUMENTARY": "DOCUMENTÁRIOS",
    "HISTORY": "DOCUMENTÁRIOS",

    "KIDS": "INFANTIL",
    "CHILDREN": "INFANTIL",

    "ENTERTAINMENT": "VARIEDADES",
    "LIFESTYLE": "VARIEDADES",

    "NEWS": "NOTÍCIAS",
    "MUSIC": "MÚSICA",
    "SPORTS": "ESPORTES",
    "ANIME": "ANIME & TOKUSATSU",

    "INTERNATIONAL": "VARIEDADES",
}

ordem_grupos = [
    "ESPORTES",
    "FILMES",
    "SÉRIES",
    "DOCUMENTÁRIOS",
    "ANIME & TOKUSATSU",
    "INFANTIL",
    "MÚSICA",
    "NOTÍCIAS",
    "VARIEDADES"
]

with open(arquivo_bruto, "r", encoding="utf-8", errors="ignore") as f:
    linhas = f.readlines()

grupos = {g: [] for g in ordem_grupos}
urls_vistas = set()

i = 0
while i < len(linhas):

    linha = linhas[i]

    if linha.startswith("#EXTINF"):

        nome = linha.split(",")[-1].strip().upper()

        grupo = "VARIEDADES"

        if 'group-title="' in linha:
            grupo_original = linha.split('group-title="')[1].split('"')[0].upper()
            grupo = mapa_grupos.get(grupo_original, grupo_original)

        nome = re.sub(r'[^\w\s\-\&\|]', '', nome)

        linha = re.sub(r'group-title="[^"]*"', '', linha)

        metadados = linha.split(",")[0]
        metadados = re.sub(r"\s+", " ", metadados).strip()

        nova_extinf = f'{metadados} group-title="{grupo}",{nome}\n'

        url = linhas[i+1].strip()

        # remove duplicado
        if url in urls_vistas:
            i += 2
            continue

        urls_vistas.add(url)

        if not url.startswith("http"):
            i += 2
            continue

        grupos.setdefault(grupo, [])
        grupos[grupo].append(nova_extinf)
        grupos[grupo].append(url + "\n")

        i += 2
        continue

    i += 1

print("⚙️ Gerando playlist final...")

with open(arquivo_final, "w", encoding="utf-8") as f:

    f.write(f'#EXTM3U updated="{datetime.now()}"\n')

    for grupo in ordem_grupos:
        for linha in grupos.get(grupo, []):
            f.write(linha)

print("✅ Playlist final pronta!")

# 🔥 GIT
print("📤 Enviando para GitHub...")

os.system("git add .")
commit_status = os.system('git diff --cached --quiet')

if commit_status != 0:
    os.system('git commit -m "Atualização automática Samsung"')
    os.system("git push")
    print("✅ Upload concluído!")
else:
    print("ℹ️ Nada para enviar.")
