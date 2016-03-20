Troll Bot
=========
Annoy your friends with this Telegram Bot


Setup
=====

You will need to add this enviroment variables:
* BOT_TOKEN: token from [@BotFather](https://telegram.me/BotFather)
* BOT_URL(Optional): url where you setup webhook
* CERTIFICATE_PATH(Optional): self signed certificated to [set webhook](https://core.telegram.org/bots/api#setwebhook).
* DB_HOST: mongoDB host
* DB_PORT: mongoDB port

If BOT_URL or CERTIFICATE_PATH are not set, Bot will run without webhook.

Need to set privacy off using `/setprivacy` command in [@BotFather](https://telegram.me/BotFather)

Example using docker-compose:
```yml
troll-bot:
  restart: always
  image: pando85/troll-bot
  links:
    - mongo
  ports:
     - "5000:5000"
  volumes:
    - ./cert.pem:/tmp/cert.pem:ro
  environment:
    - BOT_TOKEN= Telegram Bot API token
    - BOT_URL= Telegram Bot URL
    - CERTIFICATE_PATH=/tmp/cert.pem
    - DB_HOST=mongo
    - DB_PORT=27017

mongo:
  restart: always
  image: mongo
  volumes_from:
    - data
  expose:
    - "27017"

data:
  restart: always  
  image: mongo:3.2.4
  volumes:
    - /data/db
  command: "true"
  
  ```