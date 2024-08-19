FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN apt update
RUN sudo apt-get install poppler-utils
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5100

CMD ["python", "app.py"]