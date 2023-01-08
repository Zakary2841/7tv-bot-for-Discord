# Run the bot using Docker
This was made by the following user > https://hub.docker.com/r/bradyns/7tv-bot-for-discord
## Prerequisites

1. Download and install Docker
   - The easiest method for most is [Docker Desktop](https://www.docker.com/products/docker-desktop/) which is available on almost any platform.
2. Make sure you have followed the above instructions for configuring up the bot.
   - Have the `config.json` file configured to your liking with the correct token added.
     - Place `config.json` in a folder/directory where it's not likely to be deleted by accident

## Quick Start

#### For Windows users who are new to Docker:

- Docker uses "volumes" (The -v flag) to map files and folders on your computer to files/folders in the container
  - Windows uses a directory syntax like this C:\path\to\your\config.json
  - Docker may need it to be in a UNIX format. e.g. //c/path/to/your/config.json
    - If you run into issues using Windows syntax, try UNIX syntax (Case sensistivity is important, UNIX should be lower-case)

- Docker uses "ports" (The -p flag) to map a port on the outside of the container to a port inside the container.
  - This doesn't matter too much, just replace Port 6969 with a port that's available on your machine.
    - I used the example 6969:80 you can make it 22222:80
    - **DO NOT** change the 80. Only change 6969.

#### Below are two examples of a docker command which will launch the containers:

```
$ docker run -d \
--name 7tvbot \
-p 6969:80 \
-v /path/to/your/config.json:/config.json \
--restart=unless-stopped \
bradyns/7tv-bot-for-discord:latest
```

Single line:
```
$ docker run -d --name 7tvbot -p 6969:80 -v /path/to/your/config.json:/config.json --restart=unless-stopped bradyns/7tv-bot-for-discord:latest
```


## Run via Docker Compose

```
version: "3.8"

services:
  7tvbot:
    image: bradyns/7tv-bot-for-discord:latest
    container_name: 7tvbot
    restart: unless-stopped
    ports:
      - 6969:80
    volumes:
      - /path/to/your/config.json:/config.json
    networks:
      - example-network
      
networks:
  example-network:
    external: true
```

## Build from Dockerfile

The Dockerfile is [located here](Dockerfile)
