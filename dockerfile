FROM python:3.11-slim

ENV PYTHONDONTWRITETECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR / code

COPY requirements.txt .

RUN  pip install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput


CMD ["gunicorn", "ChatterMail.wsgi:application", "--bind", "0.0.0.0:8000"]
