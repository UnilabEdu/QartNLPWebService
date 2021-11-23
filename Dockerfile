FROM python:3.9.1
WORKDIR /qartnlp
RUN apt update
RUN apt install -y foma-bin
RUN apt-get install -y antiword poppler-utils
COPY requirements.txt /qartnlp
RUN pip install -r requirements.txt
ENV FLASK_APP run.py
ADD . /qartnlp
RUN flask db_reset
RUN flask db_populate
ENTRYPOINT ["flask"]
CMD ["run", "--host", "0.0.0.0"]