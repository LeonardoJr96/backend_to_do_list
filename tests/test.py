import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient


# ── Mock das funções de banco ANTES de importar o app ────────────────────────
mock_create   = MagicMock()
mock_read     = MagicMock()
mock_read_item= MagicMock()
mock_update   = MagicMock()
mock_delete   = MagicMock()
mock_delete_item = MagicMock()

with patch.dict("os.environ", {"DATABASE_URL": "sqlite:///:memory:"}), \
     patch("src.backend_to_do_list.services.database.create_engine", MagicMock()), \
     patch("src.backend_to_do_list.services.database.Base.metadata.create_all", MagicMock()), \
     patch("src.backend_to_do_list.main.create",      mock_create), \
     patch("src.backend_to_do_list.main.read",        mock_read), \
     patch("src.backend_to_do_list.main.read_item",   mock_read_item), \
     patch("src.backend_to_do_list.main.update",      mock_update), \
     patch("src.backend_to_do_list.main.delete",      mock_delete), \
     patch("src.backend_to_do_list.main.delete_item", mock_delete_item):
    from src.backend_to_do_list.main import app


# ── Fixture: reseta os mocks antes de cada teste ─────────────────────────────
@pytest.fixture(autouse=True)
def reset_mocks():
    mock_create.reset_mock()
    mock_read.reset_mock()
    mock_read_item.reset_mock()
    mock_update.reset_mock()
    mock_delete.reset_mock()
    mock_delete_item.reset_mock()


@pytest.fixture
def client():
    return TestClient(app, raise_server_exceptions=True)


# ── Helper: tarefa fake retornada pelo banco ──────────────────────────────────
def fake_task(id=1, title="Tarefa", description="Desc", status=False):
    task = MagicMock()
    task.id          = id
    task.title       = title
    task.description = description
    task.status      = status
    return task


def criar_tarefa(client, title="Tarefa teste", description="Descrição", status=False):
    return client.post("/", json={"title": title, "description": description, "status": status})


# =============================================================================
# 1. Health check  GET /
# =============================================================================
class TestHealthCheck:
    def test_retorna_200(self, client):
        assert client.get("/").status_code == 200

    def test_retorna_message(self, client):
        assert client.get("/").json() == {"message": "Hello World"}


# =============================================================================
# 2. Criar tarefa  POST /
# =============================================================================
class TestCriarTarefa:
    def test_status_200(self, client):
        mock_create.return_value = fake_task(id=1)
        assert criar_tarefa(client).status_code == 200

    def test_retorna_id_gerado(self, client):
        mock_create.return_value = fake_task(id=42)
        assert criar_tarefa(client).json()["id"] == 42

    def test_retorna_details(self, client):
        mock_create.return_value = fake_task()
        assert criar_tarefa(client).json()["details"] == "Item criado"

    def test_retorna_status_false(self, client):
        mock_create.return_value = fake_task(status=False)
        assert criar_tarefa(client, status=False).json()["status"] is False

    def test_retorna_status_true(self, client):
        mock_create.return_value = fake_task(status=True)
        assert criar_tarefa(client, status=True).json()["status"] is True

    def test_chama_create_uma_vez(self, client):
        mock_create.return_value = fake_task()
        criar_tarefa(client)
        mock_create.assert_called_once()


# =============================================================================
# 3. Listar tarefas  GET /items/
# =============================================================================
class TestListarTarefas:
    def test_lista_vazia(self, client):
        mock_read.return_value = []
        response = client.get("/items/")
        assert response.status_code == 200
        assert response.json() == []

    def test_retorna_lista_com_tarefas(self, client):
        mock_read.return_value = [
            fake_task(id=1, title="A"),
            fake_task(id=2, title="B"),
        ]
        data = client.get("/items/").json()
        assert len(data) == 2

    def test_chama_read_uma_vez(self, client):
        mock_read.return_value = []
        client.get("/items/")
        mock_read.assert_called_once()


# =============================================================================
# 4. Buscar por ID  GET /items/{id}
# =============================================================================
class TestBuscarTarefa:
    def test_retorna_200_quando_existe(self, client):
        mock_read_item.return_value = fake_task(id=1, title="Tarefa")
        assert client.get("/items/1").status_code == 200

    def test_retorna_404_quando_nao_existe(self, client):
        mock_read_item.return_value = None
        assert client.get("/items/9999").status_code == 404

    def test_chama_read_item_com_id_correto(self, client):
        mock_read_item.return_value = fake_task(id=7)
        client.get("/items/7")
        mock_read_item.assert_called_once_with(7)


# =============================================================================
# 5. Atualizar  PUT /items/{id}
# =============================================================================
class TestAtualizarTarefa:
    def test_retorna_200_quando_existe(self, client):
        mock_read_item.return_value = fake_task(id=1)
        response = client.put("/items/1", json={"title": "Novo", "description": "D", "status": True})
        assert response.status_code == 200

    def test_retorna_details(self, client):
        mock_read_item.return_value = fake_task(id=1)
        data = client.put("/items/1", json={"title": "X", "description": "Y", "status": False}).json()
        assert data["details"] == "item atualizado"

    def test_retorna_404_quando_nao_existe(self, client):
        mock_read_item.return_value = None
        response = client.put("/items/9999", json={"title": "X", "description": "Y", "status": False})
        assert response.status_code == 404

    def test_chama_update_com_id_correto(self, client):
        mock_read_item.return_value = fake_task(id=5)
        client.put("/items/5", json={"title": "X", "description": "Y", "status": False})
        args = mock_update.call_args[0]
        assert args[0] == 5

    def test_nao_chama_update_quando_nao_existe(self, client):
        mock_read_item.return_value = None
        client.put("/items/9999", json={"title": "X", "description": "Y", "status": False})
        mock_update.assert_not_called()


# =============================================================================
# 6. Deletar por ID  DELETE /items/{id}
# =============================================================================
class TestDeletarTarefa:
    def test_retorna_200_quando_existe(self, client):
        mock_read_item.return_value = fake_task(id=1)
        assert client.delete("/items/1").status_code == 200

    def test_retorna_details(self, client):
        mock_read_item.return_value = fake_task(id=1)
        data = client.delete("/items/1").json()
        assert data["details"] == "item deletado"
        assert data["id"] == 1

    def test_retorna_404_quando_nao_existe(self, client):
        mock_read_item.return_value = None
        assert client.delete("/items/9999").status_code == 404

    def test_chama_delete_item_com_id_correto(self, client):
        mock_read_item.return_value = fake_task(id=3)
        client.delete("/items/3")
        mock_delete_item.assert_called_once_with(3)

    def test_nao_chama_delete_item_quando_nao_existe(self, client):
        mock_read_item.return_value = None
        client.delete("/items/9999")
        mock_delete_item.assert_not_called()


# =============================================================================
# 7. Deletar todas  DELETE /items/
# =============================================================================
class TestDeletarTodas:
    def test_retorna_200(self, client):
        assert client.delete("/items/").status_code == 200

    def test_retorna_message(self, client):
        assert "message" in client.delete("/items/").json()

    def test_chama_delete_uma_vez(self, client):
        client.delete("/items/")
        mock_delete.assert_called_once()


# =============================================================================
# 8. Fluxo completo (comportamento encadeado)
# =============================================================================
class TestFluxoCompleto:
    def test_criar_e_buscar(self, client):
        mock_create.return_value = fake_task(id=10, title="Leite")
        mock_read_item.return_value = fake_task(id=10, title="Leite")

        id_ = criar_tarefa(client, title="Leite").json()["id"]
        data = client.get(f"/items/{id_}").json()
        assert data["title"] == "Leite"

    def test_criar_atualizar_buscar(self, client):
        mock_create.return_value = fake_task(id=1, title="Antes", status=False)
        mock_read_item.return_value = fake_task(id=1, title="Depois", status=True)

        id_ = criar_tarefa(client, title="Antes").json()["id"]
        client.put(f"/items/{id_}", json={"title": "Depois", "description": "", "status": True})
        data = client.get(f"/items/{id_}").json()
        assert data["title"] == "Depois"

    def test_deletar_chama_funcao_correta(self, client):
        mock_read_item.return_value = fake_task(id=1)
        client.delete("/items/1")
        mock_delete_item.assert_called_once_with(1)
        mock_delete.assert_not_called()