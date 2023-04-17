# Проект QRKot — это сервис для благотворительного фонда поддержки котиков

## Автор: Михалицын А.С. ([misterio92](https://github.com/misterio92)) 


## **Стек**

[Python](https://www.python.org/)
[FastApi](https://fastapi.tiangolo.com/).

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/misterio92/cat_charity_fund.git
```

```
cd cat_charity_fund
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```


Заполнить .env:

```

APP_TITLE=Благотворительный фонд поддержки котиков QRKot.
APP_DESCRIPTION=Фонд сбора средств, направленные на помощь котиков.
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=SECRET
SUPERUSER_EMAIL=superusser@mail.ru
SUPERUSER_PASSWORD=passwordsuperuser
```


Создание БД и выполнений миграций:

```

alembic revision --autogenerate -m "Comment"
alembic upgrade head
```

Запуск сервера:

```

uvicorn app.main:app
```