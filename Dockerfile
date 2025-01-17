FROM python:3.10

WORKDIR /app

# Copiar os arquivos de dependências
COPY requirements.txt .

# Instalar as dependências do Python
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copiar todos os arquivos do projeto
COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
