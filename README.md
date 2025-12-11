## Делаба - Веб-приложение для планирования задач по учёбе

<img align="right" alt="Delaba main logo" src="https://github.com/user-attachments/assets/5ba19b13-7a24-4004-b50f-59b2acfd89eb" width="180" />

* Загружайте задания в виде списка пунктов или документов (.pdf);
* Отслеживайте доступные задания и сроки их выполнения
* Поддержка прав доступа - все данные разделены по виртуальным каналам.

<img width="700" alt="Delaba home screen (only partially shown)" src="https://github.com/user-attachments/assets/cb030da5-41bb-4883-a812-60643b1449f9" />

## Как запустить?
### 1. Настройте файл окружения
Добавьте файл ``.env`` в корне проекта, например такой:
```yaml
POSTGRES_PASSWORD=admin
POSTGRES_USER=admin
POSTGRES_DB=delaba

POSTGRES_ADDRESS=localhost # Адрес базы данных для локальной разработки
POSTGRES_PORT=5432
SQLALCHEMY_ECHO=true # Выводить ли SQLAlchemy данные для отладки (отключено на продакшене)

# Сгенерируйте и вставьте вместо угловых скобок свои токены (JWT Secret)
JWT_ACCESS_SECRET=<access-token>
JWT_REFRESH_SECRET=<refresh-token>

# Это значение будет использоваться для создания аккаунта администратора
ADMIN_INIT_TOKEN=<init-token>
```

### 2.1. Продакшен
Cоберите и запустите контейнеры приложения:
```docker-compose -f docker-compose.yml up --build```

### 2.2. Разработка
Запустите бекенд и фронтенд сервисы, предварительно развернув у себя базу данных PostgreSQL:


**Бекенд (из /backend):**


```pip install -r requirements.txt```


```uvicorn src.main:app --reload```

**Фронтенд (из /frontend):**


```npm install```


```npm run dev```


### 3. Завершите создание первого аккаунта администратора
Интерфейс пользователя станет доступен по адресу ``localhost:5173``, а API - ``localhost:8000/docs``.


Зайдите в интерфейс пользователя и нажмите на кружок под полем пароля (у администратора по умолчанию устанавливается пустой логин), далее вам будет предложено ввести токен и новый пароль (используйте ранее введённый токен из ``.env``).


Готово!
