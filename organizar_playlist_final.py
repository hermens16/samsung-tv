import requests
import time

arquivo_entrada = "samsung_traduzida.m3u"
arquivo_saida = "samsung_final.m3u"

print("📡 Limpando duplicados (priorizando canais ON)...")

def canal_online(url):
    try:
        r = requests.head(url, timeout=5, allow_redirects=True)
        return r.status_code < 400
    except:
        return False

with open(arquivo_entrada, "r", encoding="utf-8", errors="ignore") as f:
    linhas = f.readlines()

canais = {}
saida = []

i = 0

# 🔥 AGRUPAR CANAIS PELO NOME
while i < len(linhas):

    if linhas[i].startswith("#EXTINF"):

        extinf = linhas[i]
        url = linhas[i+1].strip()
        nome = extinf.split(",")[-1].strip()

        if nome not in canais:
            canais[nome] = []

        canais[nome].append((extinf, url))

        i += 2
        continue

    i += 1

# 🔥 FILTRAGEM INTELIGENTE
for nome, lista in canais.items():

    print(f"\n🔎 Canal: {nome}")

    online = []
    offline = []

    for extinf, url in lista:

        status = canal_online(url)

        if status:
            print("✅ ON")
            online.append((extinf, url))
        else:
            print("❌ OFF")
            offline.append((extinf, url))

        time.sleep(0.2)

    # 🎯 REGRA FINAL
    if online:
        escolhidos = online[:2]  # mantém até 2 ON
    else:
        escolhidos = offline[:1]  # mantém 1 OFF se não tiver ON

    for extinf, url in escolhidos:
        saida.append(extinf)
        saida.append(url + "\n")

# 🔥 SALVAR
with open(arquivo_saida, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    for linha in saida:
        f.write(linha)

print("\n✅ Lista final otimizada gerada!")
