from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from repositories.cliente_repo import ClienteRepo
from repositories.produto_repo import ProdutoRepo
from routes import main_routes, cliente_routes
from util.auth import middleware_autenticacao
from util.exceptions import configurar_excecoes

ProdutoRepo.criar_tabela()
ProdutoRepo.inserir_produtos_json("sql/produtos.json")
ClienteRepo.criar_tabela()
ClienteRepo.inserir_clientes_json("sql/clientes.json")
app = FastAPI()
app.mount(path="/static", app=StaticFiles(directory="static"), name="static")
app.middleware(middleware_type="http")(middleware_autenticacao)
configurar_excecoes(app)
app.include_router(main_routes.router)
app.include_router(cliente_routes.router)
if __name__ == "__main__":
    uvicorn.run(app="main:app", port=8073, reload=True)
