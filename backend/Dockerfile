FROM python:3.12-slim

WORKDIR /app

COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r ./backend/requirements.txt

COPY . .
ENV PYTHONPATH=/app
EXPOSE 5000

CMD ["python", "-m", "backend.app"]
