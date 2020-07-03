ТЗ: [here](https://pastebin.com/KyEpdNUg)

Run bot:
```
python tbot/bot.py
```

Run fast Api server
```
uvicorn tbot.api.main:app --reload
```

Create new migrations
```
alembic revision --autogenerate -m "Message"
```

Run existing migrations
```
alembic upgrade head
```