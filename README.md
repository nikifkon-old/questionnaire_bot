ТЗ: [here](https://pastebin.com/KyEpdNUg)

Installation
```
cp .env.example .env
```

Run bot:
```
python tbot/bot.py
```

Run flask dev server
```
flask run
```

Create new migrations
```
alembic revision --autogenerate -m "Message"
```

Run existing migrations
```
alembic upgrade head
```