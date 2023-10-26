# QRKot

Благотворительный фонд поддержки котиков.
Фонд собирает пожертвования на различные целевые проекты.

### Возможности

- В Фонде QRKot может быть открыто несколько целевых проектов.
- Каждый пользователь может сделать пожертвование и сопроводить его
  комментарием.
- Пожертвования в проекты поступают по принципу First In, First Out.

### Технологии

- FastApi
- FastApiUsers
- SQLAlchemy

## Начало Работы

Чтобы запустить локальную копию проекта, следуй инструкциям ниже.

### Зависимости

- Python 3.9+

### Установка

1. **Клонируй репозиторий**

   ```shell
   git clone https://github.com/AlexandrVasilchuk/cat_charity_fund.git
   cd QRKot
   ```

### Локальный Запуск (Development)

1. **Установи зависимости проекта**

    ```shell
    pip install -r requirements.txt
    ``` 
2. **В корне проекта создай `.env` файл**

    ```dotenv
    SECRET="<секретный ключ>"
    ```

   *Секретный ключ можно сгенерировать [тут](https://djecrety.ir/)*

3. **Запусти базу данных**

    ```shell
    alembic revision --autogenerate
    alembic upgrade head
    ```
4. **Запусти локальный сервер**

    ```shell
    uvicorn app.main:app
    ```

   После запуска, проект будет доступен по адресу http://localhost:8000/

## Использование

Swagger UI доступен по адресу http://localhost:8000/docs.

Там ты найдешь полную документацию к API, а также сможешь сделать запрос на
сервер.

---

## Контакты

___

Автор:
[Васильчук Александр](https://github.com/AlexandrVasilchuk/)

#### Контакты:

![Gmail-badge](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)\
alexandrvsko@gmail.com\
![Telegram-badge](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)\
@vsko_dev

