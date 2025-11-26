# Деплой на Heroku

Этот документ описывает процесс деплоя LLM Council на Heroku.

## Предварительные требования

1. Аккаунт на [Heroku](https://www.heroku.com/)
2. Установленный [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
3. Git репозиторий проекта

## Шаги деплоя

### 1. Подготовка проекта

Все необходимые файлы уже созданы:
- `Procfile` - команды запуска
- `requirements.txt` - Python зависимости
- `runtime.txt` - версия Python
- `package.json` - для сборки фронтенда
- `app.json` - конфигурация Heroku
- `.slugignore` - исключения для деплоя

### 2. Логин в Heroku

```bash
heroku login
```

### 3. Создание приложения

```bash
heroku create your-app-name
```

Или используйте существующее приложение:
```bash
heroku git:remote -a your-app-name
```

### 4. Настройка buildpacks

Приложение использует два buildpack'а:
1. Node.js (для сборки фронтенда)
2. Python (для запуска бэкенда)

Установите их в правильном порядке:
```bash
heroku buildpacks:add heroku/nodejs
heroku buildpacks:add heroku/python
```

Проверьте порядок:
```bash
heroku buildpacks
```

Должно быть:
1. heroku/nodejs
2. heroku/python

### 5. Настройка переменных окружения

Установите обязательные переменные:

```bash
heroku config:set OPENROUTER_API_KEY=sk-or-v1-...
```

Опциональные переменные:
```bash
# Настройка моделей (JSON массив)
heroku config:set COUNCIL_MODELS='["openai/gpt-4o","google/gemini-2.0-flash-exp"]'

# Модель председателя
heroku config:set CHAIRMAN_MODEL="google/gemini-2.0-flash-exp"

# CORS origins (если нужно)
heroku config:set CORS_ORIGINS='["https://your-domain.com"]'

# Python окружение
heroku config:set PYTHON_ENV=production
heroku config:set NODE_ENV=production
```

### 6. Деплой

```bash
git add .
git commit -m "Prepare for Heroku deployment"
git push heroku master
```

Или если используете main ветку:
```bash
git push heroku main
```

### 7. Проверка деплоя

После деплоя откройте приложение:
```bash
heroku open
```

Проверьте логи:
```bash
heroku logs --tail
```

## Процесс сборки

При деплое Heroku автоматически:

1. **Устанавливает Node.js зависимости** из `package.json`
2. **Запускает `heroku-postbuild`** скрипт, который:
   - Переходит в `frontend/`
   - Устанавливает npm зависимости
   - Собирает фронтенд (`npm run build`)
3. **Устанавливает Python зависимости** из `requirements.txt`
4. **Запускает `release` команду** из `Procfile` (если есть)
5. **Запускает `web` команду** из `Procfile` для старта сервера

## Структура деплоя

- **Фронтенд**: Собирается в `frontend/dist/` и отдается через FastAPI как статика
- **Бэкенд**: Запускается через uvicorn на порту, указанном в переменной `PORT`
- **API**: Доступно по `/api/*` маршрутам
- **SPA роутинг**: Все не-API маршруты отдают `index.html`

## Переменные окружения

### Обязательные

- `OPENROUTER_API_KEY` - API ключ OpenRouter

### Опциональные

- `COUNCIL_MODELS` - JSON массив моделей для совета (по умолчанию: gpt-4o, gemini-2.0-flash-exp, claude-3.5-sonnet, grok-2-1212)
- `CHAIRMAN_MODEL` - Модель председателя (по умолчанию: gemini-2.0-flash-exp)
- `CORS_ORIGINS` - JSON массив разрешенных origins (в продакшене можно не указывать)
- `DATA_DIR` - Директория для хранения данных (по умолчанию: `data/conversations`)
- `API_TIMEOUT` - Таймаут API запросов в секундах (по умолчанию: 120)
- `API_MAX_RETRIES` - Максимальное количество повторов (по умолчанию: 3)
- `PORT` - Порт сервера (устанавливается автоматически Heroku)
- `PYTHON_ENV` - Окружение Python (рекомендуется: `production`)
- `NODE_ENV` - Окружение Node.js (рекомендуется: `production`)

## Устранение проблем

### Проблема: Фронтенд не собирается

Проверьте логи сборки:
```bash
heroku logs --tail
```

Убедитесь, что buildpack'и установлены в правильном порядке (Node.js первый).

### Проблема: Статика не отдается

Убедитесь, что фронтенд собран:
```bash
heroku run ls frontend/dist
```

### Проблема: CORS ошибки

В продакшене фронтенд и бэкенд на одном домене, поэтому CORS не должен быть проблемой. Если используете отдельный домен для фронтенда, установите `CORS_ORIGINS`.

### Проблема: Порт не найден

Heroku автоматически устанавливает переменную `PORT`. Убедитесь, что код использует `os.getenv("PORT")` (уже настроено в `config.py`).

## Обновление приложения

После изменений в коде:

```bash
git add .
git commit -m "Your changes"
git push heroku main
```

## Масштабирование

Для увеличения количества dyno:

```bash
heroku ps:scale web=2
```

## Мониторинг

Просмотр метрик:
```bash
heroku ps
heroku logs --tail
```

## Дополнительные ресурсы

- [Heroku Python Support](https://devcenter.heroku.com/articles/python-support)
- [Heroku Node.js Support](https://devcenter.heroku.com/articles/nodejs-support)
- [Heroku Buildpacks](https://devcenter.heroku.com/articles/buildpacks)

