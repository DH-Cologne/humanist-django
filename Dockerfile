FROM python:3.9.0
ENV PYTHONUNBUFFERED=1
RUN mkdir /humanist
WORKDIR /humanist
COPY requirements.txt requirements-dev.txt /humanist/
RUN pip install -U pip
RUN pip install -r requirements-dev.txt
COPY . /humanist/
#CMD ["./migrate_and_run.sh"]
