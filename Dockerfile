# Use uma imagem oficial do Python
FROM python:3.10-slim

# Configurar o diretório de trabalho
WORKDIR /app

# Copiar os arquivos de dependências
COPY requirements.txt .

# Instalar as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todos os arquivos do projeto
COPY . .

# Expor a porta padrão usada pelo Django (8000)
EXPOSE 8000

# Comando para iniciar o Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
