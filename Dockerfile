FROM python:3.12.12-slim-trixie

ENV PYTHONUNBUFFERED=1

WORKDIR /ai

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY /ai ./ai

EXPOSE 8000

CMD ["uvicorn", "ai.main:app", "--host", "0.0.0.0", "--port", "8000"]