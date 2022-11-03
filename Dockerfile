FROM joyzoursky/python-chromedriver:3.6-alpine3.7
#Install Cron
RUN apt-get update
RUN apt-get -y install cron
# Copy the crontab file
COPY crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab
# Set the work dir
WORKDIR /app
# Copy the files
ADD . .
# Install the dependencies
RUN pip install -r requirements.txt

# Give execution rights on the cron scripts
RUN chmod 0644 Andhrimnir.py

# run crond as main process of container
CMD ["cron", "-f"]