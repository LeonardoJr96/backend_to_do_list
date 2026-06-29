import os
from unittest.mock import MagicMock, patch

# Garante que DATABASE_URL existe antes de qualquer import
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

# Evita que o SQLAlchemy tente conectar em qualquer banco
patch("src.backend_to_do_list.services.database.create_engine", MagicMock()).start()
patch("src.backend_to_do_list.services.database.Base.metadata.create_all", MagicMock()).start()