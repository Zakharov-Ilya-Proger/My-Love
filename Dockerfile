FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .

RUN sed -i 's/psycopg2/psycopg2-binary/' ./requirements.txt

RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3000

CMD ["python", "run.py"]