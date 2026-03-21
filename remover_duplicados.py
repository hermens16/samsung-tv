import os
from urllib.parse import urlparse

arquivo_entrada = "samsung_traduzida.m3u"
arquivo_saida = "samsung_final.m3u"

print("⚡ Removendo duplicados INTELIGENTE...")

if not os.path.exists(arquivo_entrada):
    print(f"❌ Arquivo não encontrado: {arquivo_entrada}")
    exit()

with open(arquivo_entrada, "r", encoding="utf-8", errors="ignore") as f:
    linhas = f.readlines()

canais_vistos = set()
saida = []

i = 0

while i < len(linhas):

    if linhas[i].startswith("#EXTINF"):

        if i + 1 >= len(linhas):
            break

        extinf = linhas[i]
        url = linhas[i+1].strip()

        nome = extinf.split(",")[-1].strip()

        # 🔥 extrai domínio da URL
        try:
            dominio = urlparse(url).netloc
        except:
            dominio = "sem_dominio"

        # 🔥 chave inteligente
        chave = f"{nome}|{dominio}"

        if chave not in canais_vistos:
            canais_vistos.add(chave)
            saida.append(extinf)
            saida.append(url + "\n")

        i += 2
        continue

    i += 1

# salvar
with open(arquivo_saida, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    for linha in saida:
        f.write(linha)

print("✅ Lista final otimizada!")

# 🔥 GIT
print("📤 Enviando para o Git...")
os.system("git add .")
os.system('git commit -m "Atualização automática IPTV"')
os.system("git push")

print("🚀 Finalizado!")
