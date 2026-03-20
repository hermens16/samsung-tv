import re

arquivo = "samsung_traduzida.m3u"

grupos = {}

with open(arquivo, "r", encoding="utf-8", errors="ignore") as f:
    for linha in f:

        if 'group-title="' in linha:

            grupo = linha.split('group-title="')[1].split('"')[0].strip()

            grupo = grupo.upper()

            if grupo not in grupos:
                grupos[grupo] = 0

            grupos[grupo] += 1

# 🔥 ORDENA DO MAIOR PRO MENOR
grupos_ordenados = sorted(grupos.items(), key=lambda x: x[1], reverse=True)

print("\n📊 GRUPOS ENCONTRADOS:\n")

for grupo, qtd in grupos_ordenados:
    print(f"{grupo} -> {qtd} canais")

print("\n🔢 Total de grupos:", len(grupos_ordenados))
