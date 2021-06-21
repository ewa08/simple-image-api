FROM python:3.9-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY app.py app.py
COPY static/ static/
COPY templates/ templates/
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
