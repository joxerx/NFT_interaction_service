FROM python:3.11

ENV PYTHONUNBUFFERED 1

RUN ls

ADD nftProject /src_nft_app/

ADD config.yml /src_nft_app/

WORKDIR /src_nft_app

RUN ls .

RUN pip install web3 django djangorestframework pyyaml

VOLUME /src_nft_app

EXPOSE 8080

CMD ls && python import_fix.py && python manage.py runserver 0.0.0.0:8000
# CMD ["%%CMD%%]