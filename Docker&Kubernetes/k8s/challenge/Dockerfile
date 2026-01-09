#-------BUILD STAGE--------

FROM python:3.9-slim AS builder

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

#-------FINAL STAGE--------

FROM python:3.9-slim AS release

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

COPY --from=builder /app /app

ENV FLASK_APP=app.py

CMD ["python", "app.py"]