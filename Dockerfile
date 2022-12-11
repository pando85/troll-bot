FROM python:3.9

ADD . /troll-bot
WORKDIR /troll-bot
RUN pip install -r requirements.txt

# espeak and oggenc
RUN apt-get update \
    && apt-get install -y \
        espeak \
        vorbis-tools \
    && rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["python", "-m", "troll_bot"]
