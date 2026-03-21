import os
import re
import unicodedata

arquivo_entrada = "samsung_traduzida.m3u"
arquivo_saida = "samsung_final.m3u"

print("🧹 Removendo duplicados inteligentes...")

if not os.path.exists(arquivo_entrada):
    print("❌ Arquivo não encontrado!")
    exit()

def normalizar_nome(nome):
    # remove acentos
    nome = unicodedata.normalize("NFKD", nome)
    nome = nome.encode("ASCII", "ignore").decode("ASCII")

    nome = nome.upper()

    # remove coisas comuns que causam duplicação
    nome = re.sub(r"\b(HD|FHD|UHD|4K|SD)\b", "", nome)
    nome = re.sub(r"\(.*?\)", "", nome)  # remove (US), (UK), etc
    nome = re.sub(r"[^A-Z0-9]", "", nome)  # remove símbolos

    return nome.strip()

with open(arquivo_entrada, "r", encoding="utf-8", errors="ignore") as f:
    linhas = f.readlines()

nomes_vistos = set()
saida = []

i = 0

while i < len(linhas):

    if linhas[i].startswith("#EXTINF"):

        if i + 1 >= len(linhas):
            break

        extinf = linhas[i]
        url = linhas[i+1]

        nome_original = extinf.split(",")[-1].strip()
        nome_normalizado = normalizar_nome(nome_original)

        # 🔥 REGRA CORRETA
        if nome_normalizado not in nomes_vistos:
            nomes_vistos.add(nome_normalizado)

            saida.append(extinf)
            saida.append(url)

        i += 2
        continue

    i += 1

# salvar
with open(arquivo_saida, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    for linha in saida:
        f.write(linha)

print("✅ Lista final limpa gerada!")
