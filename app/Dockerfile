FROM python:3.13-alpine
COPY . /app
WORKDIR /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]