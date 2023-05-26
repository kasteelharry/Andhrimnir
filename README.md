# Andhrimnir (Deprecated)

## Currently Andhrimir is broken

Since the website was overhauled, this script has been broken. Although I could make a new version or ask the developers access to their GraphQL API, I have  no intention to do so. This code is broken and that is okey. It was a fun small project to work on and I'll leave it here for posterity (or my future self).

The goal of this github repo is to scrape the popular Dutch website [eetlijst](http://www.eetlijst.nl). This website is used by many student houses to keep track of who is joining for dinner and who is cooking. Unfortunately it is very difficult to keep track of who cooked the most or what someone's cooking to eating ratio is. That is why I build this webscraper. It scrapes the last 5 pages of eetlijst history and builds an Excel file with the results in the results folder.

## Installation

To install Andhrimnir, clone the repo and create a file called ``results/credentials.py`` with the following code:

```python
username="USERNAME"
password="PASSWORD"
```

Run ``Andhrimnir.py`` and wait untill it is finished. Now you should be able to find an Excel file in either the repo folder if you were running this on windows. Otherwise you should be able to find the file in the `/results` folder.

## Setup docker image

Andhrimnir is also able to be run in a docker image. For this compose the docker file with the following command:

``Docker build . --file Dockerfile --tag YOUR_TAG_NAME``

To run the docker image run the following command:

```python
docker run
  -d
  --name='Andhrimnir'
  --net='bridge'
  --privileged=true
  -l net.unraid.docker.managed=dockerman
  -v '/mnt/user/Share/results/':'/app/results':'rw'
  -v '/dev/shm':'/dev/shm':'rw' 'YOUR TAG NAME'
```

Once the docker file is running make sure that you setup the ``credentials.py`` as discussed above inside the docker image.
