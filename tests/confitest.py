os.environ["DATABASE_URL"] = "sqlite:///:memory:"  # patch via env var
# só depois importa o módulo
import src.backend_to_do_list.services.sqlite as sqlite_module
sqlite_module.Base.metadata.create_all(bind=engine)
sqlite_module.session = test_session  # troca a session global