import re
import os

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

# 🔥 VERIFICA SE ARQUIVO EXISTE
if not os.path.exists(entrada):
    print("❌ Arquivo samsung.m3u NÃO encontrado!")
    exit()

print("📥 Lendo playlist original...")

with open(entrada, "r", encoding="utf-8", errors="ignore") as f:
    linhas = f.readlines()

grupos = {g: [] for g in ordem_grupos}
nomes_vistos = set()
urls_vistas = set()

i = 0
while i < len(linhas):

    linha = linhas[i]

    if linha.startswith("#EXTINF"):

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

        # 🔥 LIMPA CARACTERES ESTRANHOS
        nome = re.sub(r'[^\w\s\-\&\|]', '', nome)

        # 🔥 NORMALIZA NOME (ANTI-DUPLICADO)
        nome_base = nome
        nome_base = re.sub(r'\bHD\b|\bFHD\b|\bSD\b|\b4K\b', '', nome_base)
        nome_base = re.sub(r'\s+', ' ', nome_base).strip()

        url = linhas[i+1].strip() if i+1 < len(linhas) else ""

        # 🔥 IGNORA LINHAS INVÁLIDAS
        if not url.startswith("http"):
            i += 2
            continue

        # 🔥 REMOVE DUPLICADOS (NOME + URL)
        if nome_base in nomes_vistos or url in urls_vistas:
            i += 2
            continue

        nomes_vistos.add(nome_base)
        urls_vistas.add(url)

        # 🔥 REMOVE group antigo
        linha = re.sub(r'group-title="[^"]*"', '', linha)

        metadados = linha.split(",")[0]
        metadados = re.sub(r"\s+", " ", metadados).strip()

        nova_extinf = f'{metadados} group-title="{grupo}",{nome}\n'

        grupos.setdefault(grupo, [])
        grupos[grupo].append(nova_extinf)
        grupos[grupo].append(url + "\n")

        i += 2
        continue

    i += 1

# 🔥 GERA ARQUIVO FINAL
print("⚙️ Gerando playlist final...")

with open(saida, "w", encoding="utf-8") as f:

    f.write("#EXTM3U\n")

    for grupo in ordem_grupos:
        for linha in grupos.get(grupo, []):
            f.write(linha)

print("🔥 Samsung organizada com sucesso!")

# 🔥 GIT (ROBUSTO)
print("📤 Enviando para GitHub...")

# adiciona tudo (resolve seu problema)
os.system("git add .")

# commit só se houver mudança
commit_status = os.system('git diff --cached --quiet')

if commit_status != 0:
    os.system('git commit -m "Atualização automática Samsung"')
    os.system("git push")
    print("✅ Upload concluído!")
else:
    print("ℹ️ Nenhuma alteração para enviar.")
