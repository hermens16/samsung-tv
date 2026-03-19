import re
import os
from datetime import datetime

entrada = "samsung.m3u"
saida = "samsung_final.m3u"

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

if not os.path.exists(entrada):
    print("❌ samsung.m3u NÃO encontrado!")
    exit()

print("📥 Lendo playlist...")

with open(entrada, "r", encoding="utf-8", errors="ignore") as f:
    linhas = f.readlines()

grupos = {g: [] for g in ordem_grupos}
nomes_vistos = set()

total = 0
adicionados = 0

i = 0
while i < len(linhas):

    linha = linhas[i]

    if linha.startswith("#EXTINF"):

        total += 1

        try:
            nome = linha.split(",")[-1].strip().upper()
        except:
            i += 1
            continue

        grupo = "VARIEDADES"

        if 'group-title="' in linha:
            try:
                grupo_original = linha.split('group-title="')[1].split('"')[0].upper()
                grupo = mapa_grupos.get(grupo_original, grupo_original)
            except:
                pass

        nome = re.sub(r'[^\w\s\-\&\|]', '', nome)

        # normaliza nome (menos agressivo)
        nome_base = re.sub(r'\bHD\b|\bFHD\b|\bSD\b|\b4K\b', '', nome)
        nome_base = re.sub(r'\s+', ' ', nome_base).strip()

        url = linhas[i+1].strip() if i+1 < len(linhas) else ""

        # 🔥 ACEITA QUALQUER PROTOCOLO DE STREAM
        if not url or len(url) < 10:
            i += 2
            continue

        # 🔥 DUPLICADO (APENAS POR NOME)
        if nome_base in nomes_vistos:
            i += 2
            continue

        nomes_vistos.add(nome_base)

        linha = re.sub(r'group-title="[^"]*"', '', linha)

        metadados = linha.split(",")[0]
        metadados = re.sub(r"\s+", " ", metadados).strip()

        nova_extinf = f'{metadados} group-title="{grupo}",{nome}\n'

        grupos.setdefault(grupo, [])
        grupos[grupo].append(nova_extinf)
        grupos[grupo].append(url + "\n")

        adicionados += 1

        i += 2
        continue

    i += 1

print(f"📊 Total lidos: {total}")
print(f"✅ Adicionados: {adicionados}")

# 🔥 GERA PLAYLIST
with open(saida, "w", encoding="utf-8") as f:

    f.write(f'#EXTM3U updated="{datetime.now()}"\n')

    for grupo in ordem_grupos:
        for linha in grupos.get(grupo, []):
            f.write(linha)

print("🔥 Playlist final gerada!")

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
