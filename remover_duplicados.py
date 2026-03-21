import os
from urllib.parse import urlparse

arquivo_entrada = "samsung_traduzida.m3u"
arquivo_saida = "samsung_final.m3u"

print("⚡ Removendo duplicados (ajuste fino)...")

if not os.path.exists(arquivo_entrada):
    print(f"❌ Arquivo não encontrado: {arquivo_entrada}")
    exit()

with open(arquivo_entrada, "r", encoding="utf-8", errors="ignore") as f:
    linhas = f.readlines()

canais_vistos = set()
saida = []

i = 0

def base_path(path):
    partes = path.strip("/").split("/")
    
    # pega só os 2 primeiros níveis (ajuste fino)
    return "/".join(partes[:2])

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
            caminho_base = base_path(parsed.path)
        except:
            dominio = "erro"
            caminho_base = url

        # 🔥 chave equilibrada
        chave = f"{nome}|{dominio}|{caminho_base}"

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

print("✅ Lista final ajustada!")

# git
print("📤 Git...")
os.system("git add .")
os.system('git commit -m "Ajuste fino duplicados IPTV"')
os.system("git push")

print("🚀 Finalizado!")
