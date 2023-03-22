FROM python:3.11

ENV PYTHONUNBUFFERED 1

RUN ls

ADD nftProject /src_nft_app/

ADD config.yml /src_nft_app/

WORKDIR /src_nft_app

RUN ls .

RUN pip install -r requirements.txt

VOLUME /src_nft_app

EXPOSE 8080

# CMD ["%%CMD%%]