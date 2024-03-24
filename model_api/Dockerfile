FROM python:3.8.12

# WORKDIR model_api
COPY . .

RUN apt-get update
RUN pip install -r requirements.txt

ENV PORT=5000

EXPOSE 5000

CMD ["/bin/sh", "/start.sh"]
