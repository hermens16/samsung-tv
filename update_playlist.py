import re
import os
import requests
import unicodedata
from datetime import datetime

url_playlist = "http://127.0.0.1:8182/playlist.m3u8"
arquivo_bruto = "samsung.m3u"
arquivo_final = "samsung_traduzida.m3u"

print("🌐 Baixando playlist...")

try:
    r = requests.get(url_playlist, timeout=15)
    conteudo = r.text
    print("Status:", r.status_code)
except Exception as e:
    print("❌ Erro:", e)
    input("Pressione ENTER...")
    exit()

if "#EXTINF" not in conteudo:
    print("❌ Playlist inválida!")
    input("Pressione ENTER...")
    exit()

with open(arquivo_bruto, "w", encoding="utf-8") as f:
    f.write(conteudo)

print("✅ Playlist salva!")

def normalizar(txt):
    txt = unicodedata.normalize("NFKD", txt)
    txt = txt.encode("ASCII", "ignore").decode("ASCII")
    return txt.upper().strip()

def traduzir_grupo(grupo_original):

    mapa_coreano = {
        "예능": "VARIEDADES",
        "드라마": "SÉRIES",
        "뉴스": "NOTÍCIAS",
        "스포츠": "ESPORTES",
        "어린이": "INFANTIL",
        "시사/교양": "DOCUMENTÁRIOS",
        "음악": "MÚSICA",
        "영화": "FILMES",
        "라이프스타일": "VARIEDADES",
        "실시간": "AO VIVO",
        "쇼핑": "SHOPPING"
    }

    if grupo_original in mapa_coreano:
        return mapa_coreano[grupo_original]

    g = normalizar(grupo_original)

    # 🔥 AGRUPAMENTO FORÇADO
    if g in ["AO VIVO", "SHOPPING"]:
        return "VARIEDADES"

    # 🔥 CORREÇÕES FINAIS (casos que escapavam)
    # 🔥 CORREÇÃO DEFINITIVA FUTEBOL
    if "BALL" in g:
        return "ESPORTES"

    if "NINOS" in g or "NIÑOS" in grupo_original.upper():
        return "INFANTIL"

    # 🔥 ANIME
    if "ANIME" in g:
        return "ANIME & TOKUSATSU"

    # 🔥 NOTÍCIAS
    if any(x in g for x in [
        "NEWS", "NOTIC", "ACTUAL",
        "OPINION", "REGIONAL", "ENGLISH", "HINDI"
    ]):
        return "NOTÍCIAS"

    # 🔥 ESPORTES
    if any(x in g for x in [
        "SPORT", "DEPORTE", "CALCIO",
        "FUTB", "MOTOR"
    ]):
        return "ESPORTES"

    # 🔥 INFANTIL
    if any(x in g for x in ["KID", "NIÑ", "JEUN", "BAMB"]):
        return "INFANTIL"

    # 🔥 SÉRIES
    if any(x in g for x in [
        "SERIE", "DRAMA", "CRIME", "CRIMEN",
        "TELENOVELA", "REALITE", "REALITY",
        "CLASSIC TV", "WESTERN"
    ]):
        return "SÉRIES"

    # 🔥 FILMES
    if any(x in g for x in [
        "MOVIE", "FILM", "CINE",
        "SCI-FI", "HORROR"
    ]):
        return "FILMES"

    # 🔥 DOCUMENTÁRIOS
    if any(x in g for x in [
        "DOCU", "HISTORY", "NATURE",
        "WISSEN", "INFOTAIN"
    ]):
        return "DOCUMENTÁRIOS"

    # 🔥 MÚSICA
    if any(x in g for x in ["MUSIC", "MUSIK", "MUSIQUE"]):
        return "MÚSICA"

    # 🔥 VARIEDADES
    if any(x in g for x in [
        "ENTERTAIN", "ENTRETEN", "LATINO",
        "GAME", "COMEDY", "COMEDIA",
        "INTRATTEN", "DIVERT", "AMBIANCE",
        "AO VIVO"
    ]):
        return "VARIEDADES"

    # 🔥 RELIGIOSO
    if "DEVOTIONAL" in g:
        return "RELIGIOSO"

    # 🔥 COMIDA / VIAGEM
    if any(x in g for x in [
        "LIFESTYLE", "FOOD", "TRAVEL",
        "CUCINA", "VIAGGI", "VOYAGES",
        "GASTRONOMIE", "VIAJES"
    ]):
        return "VARIEDADES"

    return grupo_original

print("⚙️ Processando...")

with open(arquivo_bruto, "r", encoding="utf-8", errors="ignore") as f:
    linhas = f.readlines()

saida = []

for linha in linhas:

    if linha.startswith("#EXTINF"):

        nome = linha.split(",")[-1].strip().upper()
        grupo = "VARIEDADES"

        if 'group-title="' in linha:
            grupo_original = linha.split('group-title="')[1].split('"')[0].strip()
            grupo = traduzir_grupo(grupo_original)

        linha = re.sub(r'group-title="[^"]*"', '', linha)
        metadados = linha.split(",")[0]

        nova = f'{metadados} group-title="{grupo}",{nome}\n'
        saida.append(nova)

    else:
        saida.append(linha)

with open(arquivo_final, "w", encoding="utf-8") as f:
    f.write(f'#EXTM3U updated="{datetime.now()}"\n')
    for linha in saida:
        f.write(linha)

print("✅ Traduzida gerada!")

print("📤 Git...")
os.system("git add .")
os.system('git commit -m "Atualização automática IPTV"')
os.system("git push")

print("🚀 Fim!")
input("Pressione ENTER para sair...")
