# Сайт доставки еды Star Burger

Ссылка на сайт: https://free-flow-code.ru/

Это сайт сети ресторанов Star Burger. Здесь можно заказать превосходные бургеры с доставкой на дом.

![скриншот сайта](https://dvmn.org/filer/canonical/1594651635/686/)


Сеть Star Burger объединяет несколько ресторанов, действующих под единой франшизой. У всех ресторанов одинаковое меню и одинаковые цены. Просто выберите блюдо из меню на сайте и укажите место доставки. Мы сами найдём ближайший к вам ресторан, всё приготовим и привезём.

На сайте есть три независимых интерфейса. Первый — это публичная часть, где можно выбрать блюда из меню, и быстро оформить заказ без регистрации и SMS.

Второй интерфейс предназначен для менеджера. Здесь происходит обработка заказов. Менеджер видит поступившие новые заказы и первым делом созванивается с клиентом, чтобы подтвердить заказ. После оператор выбирает ближайший ресторан и передаёт туда заказ на исполнение. Там всё приготовят и сами доставят еду клиенту.

Третий интерфейс — это админка. Преимущественно им пользуются программисты при разработке сайта. Также сюда заходит менеджер, чтобы обновить меню ресторанов Star Burger.

## Подготовка виртуального окружения

Перед запуском сайта создайте `.env` файл в репозитории проекта следующего содержания:

```
- DEBUG=False
- SECRET_KEY=ваш_секретный_ключ_джанго
- `ALLOWED_HOSTS`=[см. документацию Django](https://docs.djangoproject.com/en/3.1/ref/settings/#allowed-hosts)
- DB_URL=url для доступа к базе данных PostgreSQL. Должен иметь вид "postgres://USER:PASSWORD@db:PORT/NAME". Например postgres://postgres:qwerty@db:5432/mydb
- POSTGRES_USER=имя_пользователя_базы_данных
- POSTGRES_PASSWORD=пароль_пользователя_базы_данных
- POSTGRES_PORT=порт_базы_данных
- POSTGRES_DB=название_базы_данных
- YANDEX_API_KEY=апи ключ геокодера сервиса Яндекс.Карты. Получить можно [здесь](https://developer.tech.yandex.ru/services/).
```

Две **необязательных** переменных для сервиса логгирования Rollbar:

```
- ROLLBAR_TOKEN=токен доступа rollbar
- ROLLBAR_ENV=название окружения rollbar
```

### Настройка Rollbar

Создайте аккаунт в [Rollbar](https://rollbar.com) и создайте новый проект. Выбирайте Django как свою SDK и в результате вы получите строки кода, которые нужно вставить в settings.py своего проекта для интеграции Rollbar. У нас он уже установлен и настроен, вам осталось только скопировать 'access token' в файл .env в переменную ROLLBAR_TOKEN.

## Как запустить dev-версию сайта

Скачайте код:

```
git clone https://github.com/devmanorg/star-burger.git
```

Установите Docker и Docker-compose. [Ссылка на инструкцию](https://www.howtogeek.com/devops/how-to-install-docker-and-docker-compose-on-linux/).

Запустите docker-compose:

```
docker-compose -f docker-compose.dev.yml up
```

Сайт будет доступен по адресу [http://127.0.0.1:8080/](http://127.0.0.1:8080/).

## Как запустить prod-версию сайта

Скачайте код:

```
git clone https://github.com/devmanorg/star-burger.git
```

Установите Docker и Docker-compose. [Ссылка на инструкцию](https://www.howtogeek.com/devops/how-to-install-docker-and-docker-compose-on-linux/).

Запустите docker-compose:

```
docker-compose -f docker-compose.prod.yml up
```

## Как быстро обновить prod-версию сайта

В корне проекта есть скрипт`star-burger-deploy.sh`, который при запуске обновляет сайт. Переместите его в "Home/<ваш-пользователь>" для быстрого запуска сразу после входа на сервер. У пользователя должны быть права sudo.

Файл запускается командой: `./star-burger-deploy.sh`.


## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org). За основу был взят код проекта [FoodCart](https://github.com/Saibharath79/FoodCart).

Где используется репозиторий:

- Второй и третий урок [учебного курса Django](https://dvmn.org/modules/django/)
