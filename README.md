# NFT interaction service
Стек:
- Django 
- DRF
- SQLite
- web3py

## Реализовано
- Модель БД
  - id - primary key
  - unique_hash - уникальный хэш
  - tx_hash - хэш транзакции создания токена
  - media_url - урл с произвольным изображением
  - owner - адрес пользователя в сети Ethereum

- API /tokens/list
Метод запроса: GET.
Это API должно выдавать список всех обьектов модели Token

##Кстати, tokenURI к первому и единственному токену возвращает:
![ow57Hgj](https://user-images.githubusercontent.com/29130600/222440671-a523cc04-ab2a-4250-a315-d360ef87777a.jpeg)
