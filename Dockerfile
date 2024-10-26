FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN apt-get update && apt-get -y install cron build-essential cmake libopenblas-dev liblapack-dev libopenblas-dev liblapack-dev

RUN pip install -r requirements.txt


COPY cleanup_images.sh /app/cleanup_images.sh
RUN chmod +x /app/cleanup_images.sh

RUN echo "0 0 * * * /app/cleanup_images.sh" >> /etc/cron.d/cleanup-cron
RUN chmod 0644 /etc/cron.d/cleanup-cron

CMD cron && python src/bot.py