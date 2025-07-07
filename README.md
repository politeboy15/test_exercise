# test_exercise

A web platform for posting, buying, and selling products and services. Built for fast, local, and secure online deals.

---

## Содержание

- [Описание](#описание)
- [Технические требования](#технические-требования)
- [Установка](#установка)
- [Настройка](#настройка)
- [Запуск проекта](#запуск-проекта)
- [Автоматическая документация API](#автоматическая-документация-api)
- [Лицензия](#лицензия)

---

## Описание

Этот проект — веб-платформа для размещения объявлений, покупки и продажи товаров и услуг с упором на локальные и безопасные сделки.

---

## Технические требования

- Python 3.8+
- pip
- [Рекомендуется] venv/virtualenv для изоляции окружения
- PostgreSQL

---

## Установка

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/politeboy15/test_exercise.git
   cd test_exercise
   ```

2. Создайте и активируйте виртуальное окружение:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   # Для Windows: venv\Scripts\activate
   ```

3. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

---

## Настройка

1. **Настройте переменные окружения**

   Создайте файл `.env` в корне проекта или используйте настройки по умолчанию из `settings.py`. Пример:

   ```
   DEBUG=True
   SECRET_KEY=your_secret_key
   ALLOWED_HOSTS=127.0.0.1,localhost
   DATABASE_URL=sqlite:///db.sqlite3  # Или настройте PostgreSQL
   ```

2. **Примените миграции базы данных**

   ```bash
   python manage.py migrate
   ```

3. **Создайте суперпользователя (для доступа к админке)**

   ```bash
   python manage.py createsuperuser
   ```

---

## Запуск проекта

Запустите сервер разработки:

```bash
python manage.py runserver
```

Проект будет доступен по адресу: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Автоматическая документация API

Если используется Django REST Framework, автоматическая документация API доступна по следующим адресам:

- **Swagger**:  
  [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)  
  или  
  [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)

- **Redoc**:  
  [http://127.0.0.1:8000/api/redoc/](http://127.0.0.1:8000/api/redoc/)

Убедитесь, что в настройках проекта подключены соответствующие пакеты (`drf-yasg` или `drf-spectacular`) и прописаны url'ы для документации.

---

## Лицензия

MIT License

---

> Для подробной информации и примеров использования API — смотрите документацию по адресу, указанному выше.
