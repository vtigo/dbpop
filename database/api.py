from __future__ import annotations

from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session


class Database:
    """Connection facade for any SQLAlchemy-supported database."""

    def __init__(self, url: str, *, echo: bool = False) -> None:
        self.url = url
        self.engine: Engine = create_engine(url, echo=echo)

    def session(self) -> Session:
        """Open a new ORM session bound to this database."""
        return Session(self.engine)

    def create_all(self, metadata) -> None:
        """Create every table described by ``metadata``."""
        metadata.create_all(self.engine)

    def drop_all(self, metadata) -> None:
        """Drop every table described by ``metadata`` (handy when reseeding)."""
        metadata.drop_all(self.engine)

    def inspector(self):
        """Return a SQLAlchemy inspector for schema introspection."""
        return inspect(self.engine)

    def dispose(self) -> None:
        """Release the underlying connection pool."""
        self.engine.dispose()
