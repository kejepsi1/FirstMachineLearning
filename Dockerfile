# 1. Zaczynamy od gotowego, lekkiego "komputera" z zainstalowanym Pythonem 3.9
FROM python:3.9-slim

# 2. Tworzymy folder na naszą aplikację wewnątrz kontenera
WORKDIR /app

# 3. Kopiujemy naszą listę zakupów do kontenera i instalujemy biblioteki
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Kopiujemy CAŁĄ RESZTĘ (kod i model) z naszego komputera do kontenera
COPY . .

# 5. Mówimy kontenerowi, żeby wystawił "okienko" na świat przez port 8000
EXPOSE 8000

# 6. Komenda, która automatycznie odpala serwer przy starcie kontenera
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]