
import os

arquivo_entrada = "samsung_traduzida.m3u"
arquivo_saida = "samsung_final.m3u"
arquivo_log = "log_final.txt"

def log(msg):
    with open(arquivo_log, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

try:
    log("🔵 Iniciando script remover duplicados...")

    if not os.path.exists(arquivo_entrada):
        log("❌ Arquivo de entrada NÃO encontrado!")
        exit()

    with open(arquivo_entrada, "r", encoding="utf-8", errors="ignore") as f:
        linhas = f.readlines()

    canais_unicos = set()
    saida = []

    i = 0

    while i < len(linhas):

        if linhas[i].startswith("#EXTINF"):

            if i + 1 >= len(linhas):
                break

            extinf = linhas[i]
            url = linhas[i+1]

            nome = extinf.split(",")[-1].strip().upper()

            if nome not in canais_unicos:
                canais_unicos.add(nome)

                saida.append(extinf)
                saida.append(url)

            i += 2
            continue

        i += 1

    # 🔥 SALVAR FINAL
    with open(arquivo_saida, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for linha in saida:
            f.write(linha)

    log(f"✅ SUCESSO! Canais finais: {len(canais_unicos)}")

except Exception as e:
    log(f"💥 ERRO: {str(e)}")
