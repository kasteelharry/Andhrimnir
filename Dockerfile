FROM selenium/standalone-chrome
#Install Cron
USER root
RUN apt-get update && apt-get install python3-distutils -y
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py
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