import logging
import os
from alembic import context
from sqlalchemy import engine_from_config, pool
from flask import current_app

# Retrieve URL from Flask app config
sqlalchemy_url = current_app.config.get('SQLALCHEMY_DATABASE_URI')
if not sqlalchemy_url:
    logging.error("SQLAlchemy URL not found in Flask app config.")
    raise ValueError("SQLAlchemy URL is required for migrations.")

config = context.config
config.set_main_option('sqlalchemy.url', sqlalchemy_url)

target_metadata = current_app.extensions['migrate'].db.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(url=sqlalchemy_url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
        url=sqlalchemy_url
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
