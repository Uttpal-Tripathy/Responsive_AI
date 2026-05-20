FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install -r backend/requirements.txt

CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
