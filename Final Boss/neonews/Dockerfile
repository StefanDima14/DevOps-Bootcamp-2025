#-------BUILD STAGE--------

FROM python:3.15-rc-alpine AS base
WORKDIR /app
COPY src/ .

RUN pip install --no-cache-dir -r requirements.txt

#-------FINAL STAGE--------

FROM python:3.15-rc-alpine AS release
WORKDIR /app

# Add these lines to patch the OS vulnerabilities
RUN apk update && apk upgrade && \
    rm -rf /var/cache/apk/*

COPY --from=base /usr/local/lib/python3.15/site-packages /usr/local/lib/python3.15/site-packages
COPY --from=base /app /app

EXPOSE 5000
ENV FLASK_APP=app.py
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]