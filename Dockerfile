FROM python:3.5

ADD . /troll-bot
WORKDIR /troll-bot
RUN pip install -r requirements.txt

CMD ["python", "-m", "troll_bot"]
