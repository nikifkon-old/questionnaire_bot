ТЗ: [here](https://pastebin.com/KyEpdNUg)

# Installation

Create `.env` file
```
cp .env.example .env
```

##### Note:

Make sure your Postgres and Redis is working and the correct information is stored in the `.env` file

Run bot:
```
python tbot/bot.py
```

Run flask dev server
```
flask run
```

## Migrations
Create new migrations
```
alembic revision --autogenerate -m "Message"
```

Run existing migrations
```
alembic upgrade head
```