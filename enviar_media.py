import os
from django.conf import settings
from django.core.files import File
from django.core.files.storage import default_storage

enviados = 0
erros = 0

for raiz, _, arquivos in os.walk(settings.MEDIA_ROOT):
    for nome in arquivos:
        caminho = os.path.join(raiz, nome)
        destino = os.path.relpath(caminho, settings.MEDIA_ROOT).replace("\\", "/")
        try:
            with open(caminho, "rb") as f:
                salvo = default_storage.save(destino, File(f))
            enviados += 1
            if salvo != destino:
                print("Enviado com outro nome:", destino, "->", salvo)
            else:
                print("Enviado:", salvo)
        except Exception as erro:
            erros += 1
            print("ERRO em", destino, "->", erro)

print(f"\nConcluído: {enviados} enviado(s), {erros} erro(s).")