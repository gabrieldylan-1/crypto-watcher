FROM python:3.13-alpine
COPY . /app
WORKDIR /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt
CMD ["python3", "fetcher.py"]