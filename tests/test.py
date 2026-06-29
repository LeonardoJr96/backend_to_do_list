import pytest
from fastapi.testclient import TestClient

# conftest.py já fez o patch — só importa o app aqui
from src.backend_to_do_list.main import app
from src.backend_to_do_list.services.sqlite import Base, Task
import src.backend_to_do_list.services.sqlite as sqlite_module


@pytest.fixture(autouse=True)
def limpar_banco():
    """Limpa e recria as tabelas antes de cada teste."""
    session = sqlite_module.session
    session.rollback()              # limpa qualquer transação pendente
    Base.metadata.drop_all(bind=session.bind)
    Base.metadata.create_all(bind=session.bind)
    yield
    session.rollback()


@pytest.fixture
def client():
    return TestClient(app, raise_server_exceptions=True)


# ── Helper ────────────────────────────────────────────────────────────────────
def criar_tarefa(client, title="Tarefa teste", description="Descrição", status=False):
    return client.post("/", json={"title": title, "description": description, "status": status})


# =============================================================================
# 1. Health check  GET /
# =============================================================================
class TestHealthCheck:
    def test_retorna_200(self, client):
        assert client.get("/").status_code == 200

    def test_retorna_message(self, client):
        assert "message" in client.get("/").json()


# =============================================================================
# 2. Criar tarefa  POST /
# =============================================================================
class TestCriarTarefa:
    def test_status_200(self, client):
        assert criar_tarefa(client).status_code == 200

    def test_retorna_id(self, client):
        data = criar_tarefa(client).json()
        assert "id" in data and isinstance(data["id"], int)

    def test_retorna_details(self, client):
        assert criar_tarefa(client).json()["details"] == "Item criado"

    def test_status_false(self, client):
        assert criar_tarefa(client, status=False).json()["status"] is False

    def test_status_true(self, client):
        assert criar_tarefa(client, status=True).json()["status"] is True

    def test_ids_distintos(self, client):
        id1 = criar_tarefa(client, title="A").json()["id"]
        id2 = criar_tarefa(client, title="B").json()["id"]
        assert id1 != id2


# =============================================================================
# 3. Listar tarefas  GET /items/
# =============================================================================
class TestListarTarefas:
    def test_lista_vazia(self, client):
        response = client.get("/items/")
        assert response.status_code == 200
        assert response.json() == []

    def test_retorna_tarefa_criada(self, client):
        criar_tarefa(client, title="Minha tarefa")
        data = client.get("/items/").json()
        assert len(data) == 1
        assert data[0]["title"] == "Minha tarefa"

    def test_retorna_todas(self, client):
        criar_tarefa(client, title="A")
        criar_tarefa(client, title="B")
        criar_tarefa(client, title="C")
        assert len(client.get("/items/").json()) == 3

    def test_campos_presentes(self, client):
        criar_tarefa(client)
        item = client.get("/items/").json()[0]
        assert all(k in item for k in ["id", "title", "description", "status"])


# =============================================================================
# 4. Buscar por ID  GET /items/{id}
# =============================================================================
class TestBuscarTarefa:
    def test_busca_existente(self, client):
        id_ = criar_tarefa(client, title="Busca").json()["id"]
        response = client.get(f"/items/{id_}")
        assert response.status_code == 200
        assert response.json()["title"] == "Busca"

    def test_inexistente_retorna_404(self, client):
        assert client.get("/items/9999").status_code == 404

    def test_campos_corretos(self, client):
        id_ = criar_tarefa(client, title="T", description="D", status=True).json()["id"]
        data = client.get(f"/items/{id_}").json()
        assert data["title"] == "T"
        assert data["description"] == "D"
        assert data["status"] is True


# =============================================================================
# 5. Atualizar  PUT /items/{id}
# =============================================================================
class TestAtualizarTarefa:
    def test_retorna_200(self, client):
        id_ = criar_tarefa(client).json()["id"]
        response = client.put(f"/items/{id_}", json={"title": "Novo", "description": "D", "status": True})
        assert response.status_code == 200

    def test_retorna_details(self, client):
        id_ = criar_tarefa(client).json()["id"]
        data = client.put(f"/items/{id_}", json={"title": "X", "description": "Y", "status": False}).json()
        assert data["details"] == "item atualizado"

    def test_valores_atualizados(self, client):
        id_ = criar_tarefa(client, title="Antes", status=False).json()["id"]
        client.put(f"/items/{id_}", json={"title": "Depois", "description": "D", "status": True})
        data = client.get(f"/items/{id_}").json()
        assert data["title"] == "Depois"
        assert data["status"] is True

    def test_inexistente_retorna_404(self, client):
        response = client.put("/items/9999", json={"title": "X", "description": "Y", "status": False})
        assert response.status_code == 404


# =============================================================================
# 6. Deletar por ID  DELETE /items/{id}
# =============================================================================
class TestDeletarTarefa:
    def test_retorna_200(self, client):
        id_ = criar_tarefa(client).json()["id"]
        assert client.delete(f"/items/{id_}").status_code == 200

    def test_retorna_details(self, client):
        id_ = criar_tarefa(client).json()["id"]
        data = client.delete(f"/items/{id_}").json()
        assert data["details"] == "item deletado"
        assert data["id"] == id_

    def test_remove_do_banco(self, client):
        id_ = criar_tarefa(client).json()["id"]
        client.delete(f"/items/{id_}")
        assert client.get(f"/items/{id_}").status_code == 404

    def test_inexistente_retorna_404(self, client):
        assert client.delete("/items/9999").status_code == 404


# =============================================================================
# 7. Deletar todas  DELETE /items/
# =============================================================================
class TestDeletarTodas:
    def test_retorna_200(self, client):
        criar_tarefa(client)
        assert client.delete("/items/").status_code == 200

    def test_retorna_message(self, client):
        criar_tarefa(client)
        assert "message" in client.delete("/items/").json()

    def test_limpa_banco(self, client):
        criar_tarefa(client, title="A")
        criar_tarefa(client, title="B")
        client.delete("/items/")
        assert client.get("/items/").json() == []

    def test_banco_vazio_retorna_200(self, client):
        assert client.delete("/items/").status_code == 200


# =============================================================================
# 8. Fluxo completo
# =============================================================================
class TestFluxoCompleto:
    def test_crud_completo(self, client):
        id_ = criar_tarefa(client, title="Comprar leite", status=False).json()["id"]
        assert client.get(f"/items/{id_}").json()["title"] == "Comprar leite"
        client.put(f"/items/{id_}", json={"title": "Comprar leite e pão", "description": "", "status": True})
        assert client.get(f"/items/{id_}").json()["status"] is True
        client.delete(f"/items/{id_}")
        assert client.get(f"/items/{id_}").status_code == 404

    def test_isolamento_entre_tarefas(self, client):
        id1 = criar_tarefa(client, title="A").json()["id"]
        id2 = criar_tarefa(client, title="B").json()["id"]
        client.delete(f"/items/{id1}")
        assert client.get(f"/items/{id2}").status_code == 200