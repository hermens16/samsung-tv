import os

arquivo_entrada = "samsung_traduzida.m3u"
arquivo_saida = "samsung_final.m3u"

print("🧹 Removendo duplicados reais (1 por canal)...")

if not os.path.exists(arquivo_entrada):
    print("❌ Arquivo não encontrado!")
    exit()

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

        nome = extinf.split(",")[-1].strip().upper()

        # 🔥 REGRA PRINCIPAL
        if nome not in nomes_vistos:
            nomes_vistos.add(nome)

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

print("✅ Lista final sem duplicados gerada!")
