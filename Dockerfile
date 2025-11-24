#Using Selenium image with preinstalled browsers and drivers
FROM selenium/standalone-chrome

#Switching to root to install python
USER root

#Installing python and pip
RUN apt-get update && apt-get install -y python3 python3-pip

#Creating app directory
WORKDIR /app

#Copying Files
COPY requirements.txt .
COPY scraper.py .

#Installing Dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

#Creating volume directory inside container
RUN mkdir -p /app/jobs

#Setting jobs folder as volume
VOLUME ["/app/jobs"]

#Run command
CMD ["python3","scraper.py"]





