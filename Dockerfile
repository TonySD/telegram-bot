FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN apt-get update -y && apt-get upgrade -y && apt-get install -y build-essential libpq-dev ssh python3-pip postgres postgres-contrib

RUN pip install -r requirements.txt

CMD ["python", "bot.py"]