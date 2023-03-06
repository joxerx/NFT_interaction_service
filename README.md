# NFT interaction service
## Стек:

- Язык: Python 3.11
- Web framework: Django 3+ & DRF
- Database: SQLite
- Blockchain framework: Web3.py
- Blockchain: Ethereum (Goerli Testnet)
- Контейнирезация: Docker
- Документация: Swagger - drf-yasg

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

- API /tokens/total_supply
Метод запроса: GET
Это API должно обращаться к контракту в блокчейне и выдавать в ответе информацию о текущем Total supply токена - общем числе находящихся токенов в сети. Форма ответа - произвольная, в JSON-формате. Минимальный базовый пример ответа - {"result": 10000}

- API /tokens/create
Метод запроса: POST
Это API должно создавать новый уникальный токен в блокчейне и записывать параметры запроса в БД.
Запрос должен принимать:
  - media_url - урл с произвольным изображением
  - owner - Ethereum-адрес будущего владельца токена

## Конфигурирование и запуск
1. Скачать и распаковать репозиторий. 
2. Отредактировать `config.yml` с указанием своих параметров
3. В командной строке последовательно выполнить команды:
```
docker build -t nft_service .

docker run -d -p 8080:8000 -v src:/src_nft_app --name nft_app nft_service
```
4. Сервис будет доступен по адресу `http://localhost:8080/`

### Кстати, tokenURI к первому токену возвращает:
![ow57Hgj](https://user-images.githubusercontent.com/29130600/222440671-a523cc04-ab2a-4250-a315-d360ef87777a.jpeg)

#### Примеры запрососов
![image](https://user-images.githubusercontent.com/29130600/222981546-ba66f8ae-d362-45fd-bf7d-a79908653937.png)

![image](https://user-images.githubusercontent.com/29130600/222981579-22d72975-9842-4bf3-9ba8-223c2512ead7.png)

![image](https://user-images.githubusercontent.com/29130600/222981607-73493551-4dc5-4036-9ed0-fc2367ae6b89.png)
