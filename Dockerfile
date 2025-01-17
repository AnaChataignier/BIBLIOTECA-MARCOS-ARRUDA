# Usar uma imagem oficial do Python como base
FROM python:3.10-slim

# Configurar o diretório de trabalho dentro do container
WORKDIR /app

# Copiar os arquivos de dependências para o container
COPY requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todos os arquivos do projeto para o container
COPY . .

# Expor a porta padrão usada pelo Django (8000)
EXPOSE 8000

# Configurar o comando de inicialização do Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
