FROM python:slim

EXPOSE 80

WORKDIR /usr/local/app

SHELL ["/bin/bash", "-c"]

RUN apt-get update && apt-get install --yes -my wget gnupg 
RUN apt-key adv --yes --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys E1DD270288B4E6030699E45FA1715D88E1DF1F24
RUN su -c "echo 'deb http://ppa.launchpad.net/git-core/ppa/ubuntu trusty main' > /etc/apt/sources.list.d/git.list"
RUN apt-get update && apt-get install -y git
RUN git clone https://github.com/zakary2841/7tv-bot-for-Discord.git

WORKDIR /usr/local/app/7tv-bot-for-Discord

RUN pip install --upgrade pip --user
RUN pip3 install discord.py wheel idna multidict attrs requests setuptools yarl aiohttp frozenlist certifi urllib3 websockets --user

CMD ["python3", "runbot.py"]