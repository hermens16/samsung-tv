
import os
from collections import defaultdict

arquivo_entrada = "samsung_traduzida.m3u"
arquivo_saida = "samsung_final.m3u"

print("🧹 Removendo duplicados por nome (definitivo)...")

if not os.path.exists(arquivo_entrada):
    print("❌ Arquivo não encontrado!")
    exit()

with open(arquivo_entrada, "r", encoding="utf-8", errors="ignore") as f:
    linhas = f.readlines()

canais_unicos = {}
grupos = defaultdict(list)

i = 0

while i < len(linhas):

    if linhas[i].startswith("#EXTINF"):

        if i + 1 >= len(linhas):
            break

        extinf = linhas[i]
        url = linhas[i+1]

        nome = extinf.split(",")[-1].strip().upper()

        grupo = "VARIEDADES"
        if 'group-title="' in extinf:
            grupo = extinf.split('group-title="')[1].split('"')[0]

        # 🔥 GUARDA APENAS O PRIMEIRO (MESMA LÓGICA SUA)
        if nome not in canais_unicos:
            canais_unicos[nome] = True
            grupos[grupo].append((extinf, url))

        i += 2
        continue

    i += 1

# 🎯 SUA ORDEM PADRÃO
ORDEM_GRUPOS = [
    "ESPORTES",
    "FILMES",
    "SÉRIES",
    "DOCUMENTÁRIOS",
    "ANIME & TOKUSATSU",
    "INFANTIL",
    "MÚSICA",
    "NOTÍCIAS",
    "RELIGIOSO",
    "VARIEDADES"
]

# 🔥 SALVAR ORDENADO
with open(arquivo_saida, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")

    # grupos na ordem correta
    for grupo in ORDEM_GRUPOS:
        if grupo in grupos:
            for extinf, url in grupos[grupo]:
                f.write(extinf)
                f.write(url)

    # grupos que não estavam na lista (fallback)
    for grupo in grupos:
        if grupo not in ORDEM_GRUPOS:
            for extinf, url in grupos[grupo]:
                f.write(extinf)
                f.write(url)

print(f"✅ Final gerado! Total de canais únicos: {len(canais_unicos)}")
