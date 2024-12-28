FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ajouter PYTHONPATH
ENV PYTHONPATH=/app

#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]

# Condition pour exécuter pytest ou uvicorn selon la variable d'environnement RUN_TESTS
CMD ["sh", "-c", "if [ \"$RUN_TESTS\" = \"1\" ]; then pytest; else uvicorn main:app --host 0.0.0.0 --port 9000; fi"]