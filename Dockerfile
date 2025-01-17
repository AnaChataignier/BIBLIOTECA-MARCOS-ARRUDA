# Use uma imagem oficial do Python
FROM python:3.10-slim

# Configurar o diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema necessárias
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    && apt-get clean

# Copiar os arquivos de dependências
COPY requirements.txt .

# Instalar as dependências do Python
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copiar todos os arquivos do projeto
COPY . .

# Expor a porta padrão usada pelo Django (8000)
EXPOSE 8000

# Comando para iniciar o Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
