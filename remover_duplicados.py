
import os

arquivo_entrada = "samsung_traduzida.m3u"
arquivo_saida = "samsung_final.m3u"

print("🧹 Removendo duplicados por nome (definitivo)...")

if not os.path.exists(arquivo_entrada):
    print("❌ Arquivo não encontrado!")
    exit()

with open(arquivo_entrada, "r", encoding="utf-8", errors="ignore") as f:
    linhas = f.readlines()

canais_unicos = {}
saida = []

i = 0

while i < len(linhas):

    if linhas[i].startswith("#EXTINF"):

        if i + 1 >= len(linhas):
            break

        extinf = linhas[i]
        url = linhas[i+1]

        nome = extinf.split(",")[-1].strip().upper()

        # 🔥 GUARDA APENAS O PRIMEIRO
        if nome not in canais_unicos:
            canais_unicos[nome] = True

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

print(f"✅ Final gerado! Total de canais únicos: {len(canais_unicos)}")
