#
# Dockerfile for EasyMedStat DataSet microservice
#

FROM python:3.8
WORKDIR /app
RUN apt-get update \
    && apt-get install -y libspatialindex-dev
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT 5000

EXPOSE $PORT

ENTRYPOINT [ "python" ]
CMD [ "main.py" ]