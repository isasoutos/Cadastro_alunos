FROM python:3.12-slim

WORKDIR /app

# Instala as dependências primeiro
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código para dentro do container
COPY . .

# O comando padrão, mas executaremos de forma interativa depois
CMD ["python", "main.py"]