FROM python:slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . ./

RUN pip install --no-cache-dir -r requirements.txt
RUN python init_db.py

CMD ["sh", "-c", "python updater.py & gunicorn --workers=4 app:app"]
