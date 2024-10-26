FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1
ENV TZ=Asia/Tehran
WORKDIR /app
COPY . .

RUN pip install --upgrade pip setuptools
RUN pip install cmake==3.27.0
RUN apt-get update && apt-get -y install cron build-essential cmake libopenblas-dev liblapack-dev libopenblas-dev liblapack-dev ffmpeg libsm6 libxext6

RUN pip install -r requirements.txt


COPY cleanup_images.sh /app/cleanup_images.sh
RUN chmod +x /app/cleanup_images.sh

RUN echo "0 0 * * * /app/cleanup_images.sh" >> /etc/cron.d/cleanup-cron
RUN chmod 0644 /etc/cron.d/cleanup-cron

CMD cron && python src/bot.py