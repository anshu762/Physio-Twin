from __future__ import annotations

import os

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from backend.config import DATABASE_DIR


# -----------------------------------------------------------------------------
# DATABASE_URL
# -----------------------------------------------------------------------------
# If the DATABASE_URL environment variable is set (e.g. your Neon Postgres
# connection string), it is used — with the driver explicitly forced to
# psycopg2 (since that's the driver installed via requirements.txt).
#
# If it is NOT set, the app falls back to the original local SQLite file —
# local development behavior is completely unchanged.
# -----------------------------------------------------------------------------

_env_database_url = os.getenv("DATABASE_URL")

if _env_database_url:
    DATABASE_URL = _env_database_url

    # Force the psycopg2 driver explicitly, regardless of how the
    # connection string was provided (e.g. by Neon, Render, etc.)
    if DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace(
            "postgresql://", "postgresql+psycopg2://", 1
        )
    elif DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace(
            "postgres://", "postgresql+psycopg2://", 1
        )

    _connect_args: dict = {}
else:
    DATABASE_URL = (
        f"sqlite:///{DATABASE_DIR / 'physio_twin.db'}"
    )
    _connect_args = {
        "check_same_thread": False,
    }


class Base(DeclarativeBase):
    pass


engine = create_engine(
    DATABASE_URL,
    connect_args=_connect_args,
    pool_pre_ping=True,
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def _migrate_users_table() -> None:
    """
    Add profile fields to the existing users table without
    deleting or recreating existing users.

    Existing users receive deterministic legacy usernames.
    """

    inspector = inspect(engine)

    if "users" not in inspector.get_table_names():
        return

    columns = {
        column["name"]
        for column in inspector.get_columns("users")
    }

    with engine.begin() as connection:

        # -------------------------------------------------------------
        # Add missing columns
        # -------------------------------------------------------------

        if "name" not in columns:
            connection.execute(
                text(
                    "ALTER TABLE users "
                    "ADD COLUMN name VARCHAR(100)"
                )
            )

        if "username" not in columns:
            connection.execute(
                text(
                    "ALTER TABLE users "
                    "ADD COLUMN username VARCHAR(50)"
                )
            )

        # -------------------------------------------------------------
        # Give existing users deterministic legacy profiles.
        #
        # This does NOT change their UUID or any associated data.
        # -------------------------------------------------------------

        rows = connection.execute(
            text(
                "SELECT id FROM users "
                "WHERE username IS NULL OR username = ''"
            )
        ).fetchall()

        for row in rows:
            user_id = str(row[0])

            legacy_username = (
                f"legacy_{user_id.replace('-', '')[:8]}"
            )

            legacy_name = (
                f"Legacy User {user_id.replace('-', '')[:8]}"
            )

            connection.execute(
                text(
                    "UPDATE users "
                    "SET username = :username, "
                    "name = :name "
                    "WHERE id = :user_id"
                ),
                {
                    "username": legacy_username,
                    "name": legacy_name,
                    "user_id": user_id,
                },
            )

        # -------------------------------------------------------------
        # Unique username index
        # -------------------------------------------------------------

        connection.execute(
            text(
                "CREATE UNIQUE INDEX IF NOT EXISTS "
                "ix_users_username_unique "
                "ON users(username)"
            )
        )


def init_db() -> None:
    from backend.models import (
        User,
        DailyRecordDB,
        StateEstimateDB,
    )

    Base.metadata.create_all(
        bind=engine
    )

    _migrate_users_table()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()