FROM python:3.12.5-alpine3.19
WORKDIR /app
RUN mkdir temp
RUN apk add bash && apk add make && apk add sqlite
COPY . .
RUN python3.12 -m venv env && env/bin/pip install -r requirements.txt
RUN bash bin/db-start.sh
EXPOSE 5000
CMD ["bash", "bin/start-server.sh"]