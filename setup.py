from setuptools import find_packages, setup

install_requires = [
    "aiogram",
    "aioredis",
    "psycopg2",
    "Flask",
    "gunicorn",
    "Flask-Admin",
    "Flask-Login",
    "SQLAlchemy",
    "alembic",
    "pydantic",
    "python-dotenv"
]


setup(
    name="tbot",
    version="0.0.2",
    description="",
    keywords=[],
    url="https://github.com/nikifkon/questionnaire_bot.git",
    classifiers=[],
    author="Konstantin Nikiforov",
    author_email="kosty.nik.3854@gmail.com",
    license="MIT",
    packages=find_packages(),
    setup_requires=[],
    install_requires=install_requires,
    include_package_data=True,
    zip_safe=False,
)
