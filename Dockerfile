FROM python:3.11

ENV PYTHONUNBUFFERED=1

ADD . /src_nft_app/

WORKDIR /src_nft_app

RUN pip install -r requirements.txt

VOLUME /src_nft_app

EXPOSE 8080
