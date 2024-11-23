FROM python:3.12-alpine

WORKDIR /app

RUN apk add --no-cache gcc musl-dev libffi-dev postgresql-dev make openssl-dev

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3000

CMD ["python", "run.py"]