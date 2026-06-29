import os
from unittest.mock import MagicMock, patch

# Seta a variável antes de qualquer import
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

# Impede o SQLAlchemy de tentar conectar em banco real
patch("sqlalchemy.create_engine", MagicMock()).start()
patch("sqlalchemy.orm.declarative_base", MagicMock()).start()