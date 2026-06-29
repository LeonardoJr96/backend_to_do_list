import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient


# ── Mock das funções de banco ─────────────────────────────────────────────────
@pytest.fixture
def mocks():
    with patch("src.backend_to_do_list.main.create")      as mock_create, \
         patch("src.backend_to_do_list.main.read")        as mock_read, \
         patch("src.backend_to_do_list.main.read_item")   as mock_read_item, \
         patch("src.backend_to_do_list.main.update")      as mock_update, \
         patch("src.backend_to_do_list.main.delete")      as mock_delete, \
         patch("src.backend_to_do_list.main.delete_item") as mock_delete_item:
        yield {
            "create":      mock_create,
            "read":        mock_read,
            "read_item":   mock_read_item,
            "update":      mock_update,
            "delete":      mock_delete,
            "delete_item": mock_delete_item,
        }


@pytest.fixture
def client():
    from src.backend_to_do_list.main import app
    return TestClient(app, raise_server_exceptions=True)


# ── Tarefa fake ───────────────────────────────────────────────────────────────
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
# 1. Health check
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
    def test_status_200(self, client, mocks):
        mocks["create"].return_value = fake_task(id=1)
        assert criar_tarefa(client).status_code == 200

    def test_retorna_id_gerado(self, client, mocks):
        mocks["create"].return_value = fake_task(id=42)
        assert criar_tarefa(client).json()["id"] == 42

    def test_retorna_details(self, client, mocks):
        mocks["create"].return_value = fake_task()
        assert criar_tarefa(client).json()["details"] == "Item criado"

    def test_status_false(self, client, mocks):
        mocks["create"].return_value = fake_task(status=False)
        assert criar_tarefa(client, status=False).json()["status"] is False

    def test_status_true(self, client, mocks):
        mocks["create"].return_value = fake_task(status=True)
        assert criar_tarefa(client, status=True).json()["status"] is True

    def test_chama_create_uma_vez(self, client, mocks):
        mocks["create"].return_value = fake_task()
        criar_tarefa(client)
        mocks["create"].assert_called_once()


# =============================================================================
# 3. Listar tarefas  GET /items/
# =============================================================================
class TestListarTarefas:
    def test_lista_vazia(self, client, mocks):
        mocks["read"].return_value = []
        assert client.get("/items/").json() == []

    def test_retorna_tarefas(self, client, mocks):
        mocks["read"].return_value = [fake_task(id=1), fake_task(id=2)]
        assert len(client.get("/items/").json()) == 2

    def test_chama_read(self, client, mocks):
        mocks["read"].return_value = []
        client.get("/items/")
        mocks["read"].assert_called_once()


# =============================================================================
# 4. Buscar por ID  GET /items/{id}
# =============================================================================
class TestBuscarTarefa:
    def test_retorna_200_quando_existe(self, client, mocks):
        mocks["read_item"].return_value = fake_task(id=1)
        assert client.get("/items/1").status_code == 200

    def test_retorna_404_quando_nao_existe(self, client, mocks):
        mocks["read_item"].return_value = None
        assert client.get("/items/9999").status_code == 404

    def test_chama_read_item_com_id_correto(self, client, mocks):
        mocks["read_item"].return_value = fake_task(id=7)
        client.get("/items/7")
        mocks["read_item"].assert_called_once_with(7)


# =============================================================================
# 5. Atualizar  PUT /items/{id}
# =============================================================================
class TestAtualizarTarefa:
    def test_retorna_200_quando_existe(self, client, mocks):
        mocks["read_item"].return_value = fake_task(id=1)
        assert client.put("/items/1", json={"title": "X", "description": "D", "status": True}).status_code == 200

    def test_retorna_details(self, client, mocks):
        mocks["read_item"].return_value = fake_task(id=1)
        data = client.put("/items/1", json={"title": "X", "description": "Y", "status": False}).json()
        assert data["details"] == "item atualizado"

    def test_retorna_404_quando_nao_existe(self, client, mocks):
        mocks["read_item"].return_value = None
        assert client.put("/items/9999", json={"title": "X", "description": "Y", "status": False}).status_code == 404

    def test_nao_chama_update_quando_nao_existe(self, client, mocks):
        mocks["read_item"].return_value = None
        client.put("/items/9999", json={"title": "X", "description": "Y", "status": False})
        mocks["update"].assert_not_called()

    def test_chama_update_com_id_correto(self, client, mocks):
        mocks["read_item"].return_value = fake_task(id=5)
        client.put("/items/5", json={"title": "X", "description": "Y", "status": False})
        assert mocks["update"].call_args[0][0] == 5


# =============================================================================
# 6. Deletar por ID  DELETE /items/{id}
# =============================================================================
class TestDeletarTarefa:
    def test_retorna_200_quando_existe(self, client, mocks):
        mocks["read_item"].return_value = fake_task(id=1)
        assert client.delete("/items/1").status_code == 200

    def test_retorna_details_e_id(self, client, mocks):
        mocks["read_item"].return_value = fake_task(id=1)
        data = client.delete("/items/1").json()
        assert data["details"] == "item deletado"
        assert data["id"] == 1

    def test_retorna_404_quando_nao_existe(self, client, mocks):
        mocks["read_item"].return_value = None
        assert client.delete("/items/9999").status_code == 404

    def test_nao_chama_delete_item_quando_nao_existe(self, client, mocks):
        mocks["read_item"].return_value = None
        client.delete("/items/9999")
        mocks["delete_item"].assert_not_called()

    def test_chama_delete_item_com_id_correto(self, client, mocks):
        mocks["read_item"].return_value = fake_task(id=3)
        client.delete("/items/3")
        mocks["delete_item"].assert_called_once_with(3)


# =============================================================================
# 7. Deletar todas  DELETE /items/
# =============================================================================
class TestDeletarTodas:
    def test_retorna_200(self, client, mocks):
        assert client.delete("/items/").status_code == 200

    def test_retorna_message(self, client, mocks):
        assert "message" in client.delete("/items/").json()

    def test_chama_delete(self, client, mocks):
        client.delete("/items/")
        mocks["delete"].assert_called_once()


# =============================================================================
# 8. Fluxo completo
# =============================================================================
class TestFluxoCompleto:
    def test_criar_e_buscar(self, client, mocks):
        mocks["create"].return_value   = fake_task(id=10, title="Leite")
        mocks["read_item"].return_value = fake_task(id=10, title="Leite")
        id_ = criar_tarefa(client, title="Leite").json()["id"]
        assert client.get(f"/items/{id_}").json()["title"] == "Leite"

    def test_delete_nao_chama_delete_all(self, client, mocks):
        mocks["read_item"].return_value = fake_task(id=1)
        client.delete("/items/1")
        mocks["delete"].assert_not_called()
        mocks["delete_item"].assert_called_once()