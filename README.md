## Делаба - Веб-приложение для планирования задач по учёбе

<img align="right" alt="Delaba main logo" src="https://github.com/user-attachments/assets/5ba19b13-7a24-4004-b50f-59b2acfd89eb" width="180" />

* Загружайте задания в виде списка пунктов или документов (.pdf);
* Отслеживайте доступные задания и сроки их выполнения
* Поддержка прав доступа - все данные разделены по виртуальным каналам.

<img width="700" alt="Delaba home screen (only partially shown)" src="https://github.com/user-attachments/assets/cb030da5-41bb-4883-a812-60643b1449f9" />

## Как запустить?
### 1. Настройте файл окружения
Добавьте файл ``.env`` внутри ``backend``, например такой:
```yaml
MINIO_ROOT_USER=admin
MINIO_ROOT_PASSWORD=delaba-admin
MINIO_DEFAULT_BUCKET=delaba

POSTGRES_PASSWORD=admin
POSTGRES_USER=admin
POSTGRES_DB=delaba

POSTGRES_ADDRESS=relational-db
POSTGRES_PORT=5432

# Выводить ли SQLAlchemy данные для отладки
SQLALCHEMY_ECHO=true

# Сгенерируйте и вставьте вместо угловых скобок свои токены (JWT Secret)
JWT_ACCESS_SECRET=<access-token>
JWT_REFRESH_SECRET=<refresh-token>

# Домен приложения (пока что почти не используется)
ALLOWED_HOSTNAME=delaba.ru
```

### 2. Запуск
Cоберите и запустите контейнеры приложения:

### 2.1. Разработка
```docker-compose up```

### 2.2. Продакшен
```docker-compose -f docker-compose.yml up```

### 3. Завершите создание первого аккаунта администратора

### 3.1. Откройте веб-интерфейс
После запуска приложения интерфейс пользователя станет доступен по адресу ``ALLOWED_HOSTNAME`` (для продакшена; ещё в разработке) и ``localhost``.

### 3.2. Введите данные инициализации
Система при первом запуске автоматически выводит в консоль контейнера ``backend`` первоначальный логин и пароль для создания аккаунта администратора.


Введите эти данные в соответствующие поля веб-интерфейса и задайте новый логин и пароль администратора.


Готово!
