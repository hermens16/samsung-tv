import os

arquivo_entrada = "samsung_traduzida.m3u"
arquivo_saida = "samsung_final.m3u"

print("⚡ Removendo duplicados corretamente...")

if not os.path.exists(arquivo_entrada):
    print(f"❌ Arquivo não encontrado: {arquivo_entrada}")
    input("Pressione ENTER para sair...")
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
        url = linhas[i+1]

        nome = extinf.split(",")[-1].strip()

        grupo = ""
        if 'group-title="' in extinf:
            grupo = extinf.split('group-title="')[1].split('"')[0]

        # 🔥 chave correta (grupo + nome)
        chave = f"{grupo}|{nome}"

        if chave not in canais_vistos:
            canais_vistos.add(chave)

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

print("✅ Lista final corrigida!")
input("Pressione ENTER para sair...")
