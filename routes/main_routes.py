import math
import os
from sqlite3 import DatabaseError
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from dtos.entrar_dto import EntrarDTO
from ler_html import ler_html
from dtos.novo_cliente_dto import NovoClienteDTO
from models.cliente_model import Cliente
from models.locacao_model import Locacao
from models.produto_model import Produto
from repositories.cliente_repo import ClienteRepo
from repositories.locacao_repo import LocacaoRepo
from repositories.produto_repo import ProdutoRepo
from util.auth import (
    conferir_senha,
    gerar_token,
    obter_hash_senha,
)

from util.cookies import adicionar_cookie_auth, adicionar_mensagem_sucesso
from util.pydantic import create_validation_errors

router = APIRouter()

templates = Jinja2Templates(directory="templates")

def user_logged_in(request: Request):
    token = request.cookies.get("auth_token")
    if not token:
        return False
    cliente = ClienteRepo.obter_por_token(token)
    return cliente is not None

@router.get("/html/{arquivo}")
async def get_html(arquivo: str):
    response = HTMLResponse(ler_html(arquivo))
    return response


@router.get("/")
async def get_root(request: Request):
    produtos = ProdutoRepo.obter_todos()
    logged_in = user_logged_in(request)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "produtos": produtos, "user_logged_in": logged_in},
    )


@router.get("/contato")
async def get_contato(request: Request):
    return templates.TemplateResponse(
        "contato.html",
        {"request": request},
    )


# CADASTROS 
@router.get("/cadastro")
async def get_cadastro(request: Request):
    return templates.TemplateResponse(
        "cadastro.html",
        {"request": request},
    )

@router.get("/cadastrar_ferramenta")
async def get_cadastro_ferramenta(request: Request):
    return templates.TemplateResponse(
        "cadastrar_ferramenta.html",
        {"request": request},
    )

@router.post("/cadastrar_ferramenta", response_class=JSONResponse)
async def post_cadastrar_ferramenta(produto: Produto):
   
    produto_cadastrado = ProdutoRepo.inserir(produto)
    if not produto_cadastrado or not produto_cadastrado.id:
        raise HTTPException(status_code=400, detail="Erro ao cadastrar ferramenta.")
    return {"redirect": {"url": "/cadastro_ferramenta_realizado"}}

# FIM CADASTROS

# ALTERAÇÕES
@router.get("/alterar_ferramenta/{id}")
async def get_alterar_ferramenta(request: Request, id: int):
    produto = ProdutoRepo.obter_um(id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
   

    return templates.TemplateResponse(
        "alterar_ferramenta.html",
        {"request": request, "produto": produto},
    )

@router.post("/alterar_ferramenta", response_class=JSONResponse)
async def post_alterar_ferramenta(produto: Produto):
    produto_alterado = ProdutoRepo.alterar(produto)
    if not produto_alterado or not produto_alterado.id:
        raise HTTPException(status_code=400, detail="Erro ao alterar produto.")
    return {"redirect": {"url": "/alterar_ferramenta_confirmado"}}
# FIM ALTERAÇÕES

# EXCLUSÕES
@router.get("/excluir_ferramenta/{id}")
async def get_excluir_ferramenta(request: Request, id: int):
    produto = ProdutoRepo.obter_um(id)
    print("ID>>>>" + str(produto.id))
    print("NOME>>>>" + produto.nome)
    print("PREÇO>>>>" + str(produto.preco))
    print("DESCRICAO>>>>" + produto.descricao)
    print("QUANTIDADE>>>>" + str(produto.estoque))
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    return templates.TemplateResponse(
        "excluir_ferramenta.html",
        {"request": request, "produto": produto},
    )

@router.post("/excluir_ferramenta", response_class=JSONResponse)
async def post_excluir_ferramenta(produto: Produto):
    print("ID>>>>" + str(produto.id))
    print("NOME>>>>" + produto.nome)
    print("PREÇO>>>>" + str(produto.preco))
    print("DESCRICAO>>>>" + produto.descricao)
    print("QUANTIDADE>>>>" + str(produto.estoque))
    produto_excluido = ProdutoRepo.excluir(produto.id)
    print(produto_excluido)
    if not produto_excluido :
        raise HTTPException(status_code=400, detail="Erro ao excluir produto.")
    return {"redirect": {"url": "/excluir_ferramenta_realizado"}}
# FIM EXCLUSÕES


@router.post("/post_cadastro", response_class=JSONResponse)
async def post_cadastro(cliente_dto: NovoClienteDTO):
    cliente_data = cliente_dto.model_dump(exclude={"confirmacao_senha"})
    cliente_data["senha"] = obter_hash_senha(cliente_data["senha"])
    novo_cliente = ClienteRepo.inserir(Cliente(**cliente_data))
    if not novo_cliente or not novo_cliente.id:
        raise HTTPException(status_code=400, detail="Erro ao cadastrar cliente.")
    return {"redirect": {"url": "/cadastro_realizado"}}


@router.get("/cadastro_realizado")
async def get_cadastro_realizado(request: Request):
    return templates.TemplateResponse(
        "cadastro_confirmado.html",
        {"request": request},
    )

@router.get("/cadastro_ferramenta_realizado")
async def get_cadastro_realizado(request: Request):
    return templates.TemplateResponse(
        "cadastro_ferramenta_confirmado.html",
        {"request": request},
    )

@router.get("/alterar_ferramenta_confirmado")
async def get_alterar_realizado(request: Request):
    return templates.TemplateResponse(
        "alterar_ferramenta_confirmado.html",
        {"request": request},
    )

@router.get("/excluir_ferramenta_realizado")
async def get_excluir_realizado(request: Request):
    return templates.TemplateResponse(
        "excluir_ferramenta_confirmado.html",
        {"request": request},
    )


@router.get("/entrar")
async def get_entrar(
    request: Request,
    return_url: str = Query("/"),
):
    return templates.TemplateResponse(
        "entrar.html",
        {"request": request, "return_url": return_url},
    )


@router.post("/post_entrar", response_class=JSONResponse)
async def post_entrar(entrar_dto: EntrarDTO):
    cliente_entrou = ClienteRepo.obter_por_email(entrar_dto.email)
    if (
        (not cliente_entrou)
        or (not cliente_entrou.senha)
        or (not conferir_senha(entrar_dto.senha, cliente_entrou.senha))
    ):
        return JSONResponse(
            content=create_validation_errors(
                entrar_dto,
                ["email", "senha"],
                ["Credenciais inválidas.", "Credenciais inválidas."],
            ),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    token = gerar_token()
    if not ClienteRepo.alterar_token(cliente_entrou.id, token):
        raise DatabaseError(
            "Não foi possível alterar o token do cliente no banco de dados."
        )
    response = JSONResponse(content={"redirect": {"url": entrar_dto.return_url}})
    adicionar_mensagem_sucesso(
        response,
        f"Olá, <b>{cliente_entrou.nome}</b>. Seja bem-vindo(a) à Ferramentel!",
    )
    adicionar_cookie_auth(response, token)
    return response


@router.get("/produto/{id:int}")
async def get_produto(request: Request, id: int):
    produto = ProdutoRepo.obter_um(id)
    return templates.TemplateResponse(
        "produto.html",
        {"request": request, "produto": produto},
    )


@router.get("/buscar")
async def get_buscar(
    request: Request,
    q: str,
    p: int = 1,
    tp: int = 6,
    o: int = 1,
):
    produtos = ProdutoRepo.obter_busca(q, p, tp, o)
    qtde_produtos = ProdutoRepo.obter_quantidade_busca(q)
    qtde_paginas = math.ceil(qtde_produtos / float(tp))
    return templates.TemplateResponse(
        "buscar.html",
        {
            "request": request,
            "produtos": produtos,
            "quantidade_paginas": qtde_paginas,
            "tamanho_pagina": tp,
            "pagina_atual": p,
            "termo_busca": q,
            "ordem": o,
        },
    )

#################################################################
# Empréstimo

@router.get("/emprestar")
async def get_locar(request: Request):
    lista_clientes = ClienteRepo.obter_todos()
    lista_produtos = ProdutoRepo.obter_todos()
    return templates.TemplateResponse(
        "emprestar.html",
        {"request": request, "lista_clientes": lista_clientes, "lista_produtos": lista_produtos},
    )


@router.get("/emprestimos")
async def get_emprestimos(request: Request):
    lista_locacoes = LocacaoRepo.obter_todos()
    lista_clientes = ClienteRepo.obter_todos()
    for p in lista_locacoes:
        print(p.data_emprestimo)
    return templates.TemplateResponse(
        "emprestimos.html",
        {"request": request,
        "lista_locacoes": lista_locacoes,
        "lista_clientes": lista_clientes
        },
    )

@router.get("/emprestimos_gerente")
async def get_emprestimos(request: Request):
    lista_locacoes = LocacaoRepo.obter_todos()
    lista_clientes = ClienteRepo.obter_todos()
    for p in lista_locacoes:
        print(p.data_emprestimo)
    return templates.TemplateResponse(
        "emprestimos_gerente.html",
        {"request": request,
        "lista_locacoes": lista_locacoes,
        "lista_clientes": lista_clientes
        },
    )


@router.get("/cadastro_locacao_realizado")
async def get_cadastro_realizado(request: Request):
    return templates.TemplateResponse(
        "cadastro_locacao_confirmado.html",
        {"request": request},
    )

@router.get("/sobre")
async def get_sobre(request: Request):
    return templates.TemplateResponse(
        "sobre.html",
        {"request": request},
    )


@router.post("/cadastrar_emprestimo", response_class=JSONResponse)
async def post_cadastrar_emprestimo(locacao: Locacao):
    try:
        # Verifica se o cliente existe
        cliente = ClienteRepo.obter_um(locacao.cliente_id)
        if not cliente:
            raise HTTPException(status_code=404, detail=f"Cliente com ID {locacao.cliente_id} não encontrado.")
        
        produto = ProdutoRepo.obter_um(locacao.produto_id)
        print(locacao.produto_id)
        print(produto)
        if not produto:
            raise HTTPException(status_code=404, detail=f"Ferramenta com ID {locacao.produto_id} não encontrado.")
        
        LocacaoRepo.inserir(locacao)
        
        return {"redirect": {"url": "/cadastro_locacao_realizado"}}    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))