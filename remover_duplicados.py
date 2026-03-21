
import os
from urllib.parse import urlparse

arquivo_entrada = "samsung_traduzida.m3u"
arquivo_saida = "samsung_final.m3u"

print("⚡ Removendo duplicados (VERSÃO FINAL)...")

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

        nome = extinf.split(",")[-1].strip().upper()

        try:
            parsed = urlparse(url)
            dominio = parsed.netloc
            caminho = parsed.path  # 🔥 ignora ?parametros
        except:
            dominio = "sem_dominio"
            caminho = url

        # 🔥 chave FINAL
        chave = f"{nome}|{dominio}|{caminho}"

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

print("✅ Lista FINAL limpa!")

# 🔥 GIT
print("📤 Enviando para o Git...")
os.system("git add .")
os.system('git commit -m "Limpeza final IPTV (sem duplicados reais)"')
os.system("git push")

print("🚀 FINALIZADO!")
