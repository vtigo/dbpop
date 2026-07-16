from __future__ import annotations

from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import Engine, make_url
from sqlalchemy.exc import ArgumentError, SQLAlchemyError
from sqlalchemy.orm import Session


# errors
class DatabaseInitError(RuntimeError):
    """Raised when the database engine cannot be initialized from a URL."""
# end errors


# main api
class Database:
    """Adapter for any SQLAlchemy-supported database."""

    def __init__(self, url: str, *, echo: bool = False) -> None:
        self.engine: Engine = create_engine(url, echo=echo)

    def session(self) -> Session:
        """Open a new ORM session bound to this database."""
        return Session(self.engine)

    def inspector(self):
        """Return a SQLAlchemy inspector for schema introspection."""
        return inspect(self.engine)

    def dispose(self) -> None:
        """Release the underlying connection pool."""
        self.engine.dispose()


def get_database(url: str) -> Database:
    try:
        return Database(url)
    except (SQLAlchemyError, ModuleNotFoundError) as exc:
        raise DatabaseInitError(
            f"could not initialize database engine for {_safe_url(url)}: {exc}"
        ) from exc


def _safe_url(url: str) -> str:
    try:
        return make_url(url).render_as_string(hide_password=True)
    except ArgumentError:
        return "<unparsable url>"
# end main api


# tables handle
class DatabaseTablesHandle:
    def __init__(self, database: Database):
        self._db = database

    def create_all(self, metadata) -> None:
        """Create every table described by ``metadata``."""
        metadata.create_all(self._db.engine)

    def drop_all(self, metadata) -> None:
        """Drop every table described by ``metadata``."""
        metadata.drop_all(self._db.engine)


def get_tables_handle(database: Database) -> DatabaseTablesHandle:
    return DatabaseTablesHandle(database)
# end tables handle
