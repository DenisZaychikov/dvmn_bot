# Телеграм-бот Devman на Heroku

1. Телеграм-бот информирует о проверке работ в [dvmn.org](https://dvmn.org/)
2. Код предназначен для запуска на сервере [Heroku](https://id.heroku.com/login)

## Чтобы запустить, потребуются следующие данные

* `DVMN_TOKEN` - токен ученика Devman
* `DVMN_BOT_TOKEN` - токен телеграм-бота, который отправит уведомление
* `TG_USER_CHAT_ID` - id телеграм-чата, который получит уведомление

### Как запустить на Heroku

1. Зарегистрируйте приложение на [Heroku](https://id.heroku.com/login)
2. В созданном приложении во вкладке `Deploy`
привяжите данный github-репозиторий в `Deployment method`
и нажмите `Deploy Branch` внизу страницы
3. Во вкладке `Settings` заполните переменные `Config Vars`: `DVMN_TOKEN`, `DVMN_BOT_TOKEN`, `TG_USER_CHAT_ID`
4. Во вкладке `Resources` запустите сервер

### Как запустить на своей машине

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

1. Создайте в корневой папке файл ```.env``` и пропишите в нем переменные следующим образом:  
    ```
    DVMN_TOKEN=12345
    DVMN_BOT_TOKEN=12345
    TG_USER_CHAT_ID=12345
    ```

2. Запустите ```python dvmn_bot.py```


### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
