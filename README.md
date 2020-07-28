ТЗ: [here](https://pastebin.com/KyEpdNUg)

# Installation

Create `.env` file
```bash
cp .env.example .env
```

Install project
```bash
python setup.py develop
```

Install dev dependencies
```bash
pip install -r dev-requirements.txt
```

##### Note:

> Make sure your Postgres and Redis is working and the correct information is stored in the `.env` file

Run bot:
```bash
python tbot/bot.py
```

Run flask dev server
```bash
flask run
```

## Migrations
Create new migrations
```bash
alembic revision --autogenerate -m "Message"
```

Run existing migrations
```bash
alembic upgrade head
```

## Tests
```bash
pytest
```

## Code style
```bash
flake8
```