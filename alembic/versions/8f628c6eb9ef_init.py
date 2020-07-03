"""init

Revision ID: 8f628c6eb9ef
Revises:
Create Date: 2020-06-27 17:43:16.010433

"""
from alembic import op
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey


# revision identifiers, used by Alembic.
revision = '8f628c6eb9ef'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "houses",
        Column("id", Integer, primary_key=True),
        Column("number", Integer),
        Column("street", String),
        Column("area", String),
    )

    op.create_table(
        "users",
        Column("id", Integer, primary_key=True),
        Column("name", String),
        Column("phone", String),
        Column("house_id", Integer, ForeignKey("houses.id")),
        Column("flat", Integer),
    )

    op.create_table(
        "events",
        Column("id", Integer, primary_key=True),
        Column("title", String),
        Column("type", String),
        Column("description", String),
        Column("start", DateTime),
        Column("end", DateTime),
        Column("house_id", Integer, ForeignKey("houses.id")),
        Column("area", String),
        Column("target", String)
    )


def downgrade():
    op.drop_table("users")
    op.drop_table("houses")
    op.drop_table("events")
