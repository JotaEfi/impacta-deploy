FROM python:3.10

WORKDIR /app

# Copia só o requirements.txt primeiro para instalar dependências
COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia o restante do código
COPY . .

EXPOSE 8000

CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
