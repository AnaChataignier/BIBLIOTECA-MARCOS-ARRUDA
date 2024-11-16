import os
import re
import sys
import django
import pandas as pd
import pyexcel as p
from django.db.models import F, Q

# from biblioteca.models import Livro


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Configura o ambiente do Django
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "setup.settings"
)  # Substitua "Biblioteca" pelo nome correto do seu projeto
django.setup()

from biblioteca.models import Livro

# Defina o caminho para o seu arquivo .ods
file_path = "biblioteca/data/biblioteca.ods"

# Carregue o arquivo usando pyexcel
records = p.get_records(file_name=file_path)
df = pd.DataFrame(records)

df = df[~df["Título"].isna()]  # Remove linhas com valores nulos em 'Título'


# Função para substituir valores indesejados por "Não informado"
def substituir_nao_informado(valor):
    # Se o valor for nulo ou contiver apenas espaços e/ou "?"
    if pd.isnull(valor) or valor in ["-", "?", None]:
        return "Não informado"

    # Se o valor tiver espaços em branco ou um ? no final, substitui por "Não informado"
    if isinstance(valor, str):
        valor = valor.strip()  # Remove espaços antes e depois da string
        if re.fullmatch(
            r"[? ]*$", valor
        ):  # Verifica se é composto apenas por espaços ou "?"
            return "Não informado"
        # Substitui um ? no final da string
        valor = re.sub(
            r"\?$", "", valor
        ).strip()  # Remove o ? no final e espaços extras

    return valor


df = df.apply(lambda x: x.apply(substituir_nao_informado))

df["Autor"] = df.get("Autor", pd.Series()).replace(["-", "?", None], "Não informado")
df["Título"] = df.get("Título", pd.Series()).replace(["-", "?", None], "Não informado")
df["Editora"] = df.get("Editora", pd.Series()).replace(
    ["-", "?", None], "Não informado"
)
df["ANO"] = df.get("ANO", pd.Series()).replace(["-", "?", None], "Não informado")
df = df[df["Título"] != "Não informado"]

records = df.to_dict(orient="records")

filtered_df = df[df['Autor'] == "?"]
print(filtered_df)

for record in records:
    Livro.objects.create(
        autor=record.get("Autor", "Não informado"),
        titulo=record.get("Título", "Não informado"),
        editora=record.get("Editora", "Não informado"),
        ano=record.get("ANO", "Não informado"),
        categoria=record.get("CATEGORIA", "Não informado"),
    )

Livro.objects.filter(autor='?').update(autor="Não informado")


print("Dados salvos com sucesso no banco de dados Django!")
