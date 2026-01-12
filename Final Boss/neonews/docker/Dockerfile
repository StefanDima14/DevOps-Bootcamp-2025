#-------BUILD STAGE--------

FROM python:3.12-slim as base
WORKDIR /app
COPY src/ .

RUN pip install --no-cache-dir -r requirements.txt

#-------FINAL STAGE--------

FROM python:3.12-slim as release
WORKDIR /app
COPY --from=base /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=base /app /app

EXPOSE 5000
ENV FLASK_APP=app.py
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]