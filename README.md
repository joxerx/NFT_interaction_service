# NFT interaction service
Стек:
- Django 
- DRF
- SQLite

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
