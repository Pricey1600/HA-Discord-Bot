FROM python:3.12.4

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN sudo apt install tesseract-ocr -y

ENTRYPOINT ["python", "bot.py"]