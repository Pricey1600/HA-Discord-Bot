FROM python:3.12.4

WORKDIR /app

COPY . .

RUN apt-get update
RUN apt-get install tesseract-ocr -y

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "bot.py"]