# NFT interaction service
## Стек:

- Язык: Python 3.11
- Web framework: Django 3+ & DRF
- Database: Postgres 14.0, Redis 4.0
- Blockchain framework: Web3.py
- Blockchain: Ethereum (Goerli Testnet)
- Контейнеризация: Docker
- Документация: Swagger - drf-yasg

## Реализовано
- Модели БД
  - Token
    - id - primary key
    - unique_hash - уникальный хэш
    - tx_hash - хэш транзакции создания токена
    - media_url - урл с произвольным изображением
    - owner - адрес пользователя в сети Ethereum
  - Event
    - id - primary key
    - name - название ивента
    - address - адрес контракта, к которому относится ивент
    - blockHash - хэш блока
    - blockNumber - номер блока
    - transactionHash - хэш транзакции
    - removed - был ли удален

- API /api/v1/tokens/list
Метод запроса: GET.
Получить список всех обьектов модели Token

- API /api/v1//tokens/total_supply
Метод запроса: GET
Обратиться к контракту в блокчейне и получить информацию о текущем Total supply токена - общем числе находящихся токенов в сети.  При наличии проблем с подключением к сети, появится уведомление

- API /api/v1//tokens/create
Метод запроса: POST
Создать новый уникальный токен в блокчейне и сохранить параметры запроса в БД.
Запрос должен принимать:
  - media_url - урл с произвольным изображением
  - owner - Ethereum-адрес будущего владельца токена

## Конфигурирование и запуск
1. Скачать и распаковать репозиторий. 
2. Отредактировать `config.yml` с указанием своих параметров
3. В командной строке последовательно выполнить команды:
```
docker compose build

docker compose up
```
4. Сервис будет доступен по адресу `http://localhost:8228/`
- Документация `http://localhost:8228/swagger`
### Кстати, tokenURI к первому токену возвращает:
![ow57Hgj](https://user-images.githubusercontent.com/29130600/222440671-a523cc04-ab2a-4250-a315-d360ef87777a.jpeg)

#### Примеры запрососов
![image](https://user-images.githubusercontent.com/29130600/222981546-ba66f8ae-d362-45fd-bf7d-a79908653937.png)

![image](https://user-images.githubusercontent.com/29130600/222981579-22d72975-9842-4bf3-9ba8-223c2512ead7.png)

![image](https://user-images.githubusercontent.com/29130600/222981607-73493551-4dc5-4036-9ed0-fc2367ae6b89.png)
