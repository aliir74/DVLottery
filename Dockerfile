FROM python:3.11

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

RUN apt-get update && apt-get -y install cron

COPY cleanup_images.sh /app/cleanup_images.sh
RUN chmod +x /app/cleanup_images.sh

RUN echo "0 0 * * * /app/cleanup_images.sh" >> /etc/cron.d/cleanup-cron
RUN chmod 0644 /etc/cron.d/cleanup-cron

CMD cron && python src/bot.py