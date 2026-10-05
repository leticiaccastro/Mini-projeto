from fastapi import APIRouter, HTTPException, Path, Query

from app.models import (
    TarefaEntrada,
    TarefaSaida,
    StatusEnum,
    PrioridadeEnum,
    StatusAtualizacao
)


router = APIRouter(
    prefix="/tarefas",
    tags=["Tarefas"]
)


# Banco de dados temporário
tarefas_db = [
    {
        "id": 1,
        "titulo": "Configurar ambiente Python",
        "descricao": "Configurar o ambiente de desenvolvimento",
        "responsavel": "Carlos",
        "prioridade": PrioridadeEnum.alta,
        "status": StatusEnum.concluida,
        "tags": ["python", "ambiente", "configuração"]
    },
    {
        "id": 2,
        "titulo": "Criar modelos Pydantic",
        "descricao": "Criar os modelos da aplicação",
        "responsavel": "Ana",
        "prioridade": PrioridadeEnum.alta,
        "status": StatusEnum.concluida,
        "tags": ["python", "pydantic", "modelos"]
    },
    {
        "id": 3,
        "titulo": "Implementar CRUD completo",
        "descricao": "Implementar as operações de CRUD",
        "responsavel": "Carlos",
        "prioridade": PrioridadeEnum.critica,
        "status": StatusEnum.em_andamento,
        "tags": ["crud", "api", "fastapi"]
    },
    {
        "id": 4,
        "titulo": "Conectar ao banco MySQL",
        "descricao": "Fazer conexão com banco de dados",
        "responsavel": "Bruno",
        "prioridade": PrioridadeEnum.alta,
        "status": StatusEnum.pendente,
        "tags": ["mysql", "banco"]
    },
    {
        "id": 5,
        "titulo": "Escrever documentação",
        "descricao": "Criar documentação da API",
        "responsavel": "Ana",
        "prioridade": PrioridadeEnum.baixa,
        "status": StatusEnum.pendente,
        "tags": ["documentação", "api"]
    }
]


# ==========================================================
# ESTATÍSTICAS
# ==========================================================

@router.get(
    "/estatisticas",
    summary="Estatísticas gerais das tarefas"
)
def estatisticas():
    total = len(tarefas_db)

    pendentes = len([
        tarefa
        for tarefa in tarefas_db
        if tarefa["status"] == StatusEnum.pendente
    ])

    em_andamento = len([
        tarefa
        for tarefa in tarefas_db
        if tarefa["status"] == StatusEnum.em_andamento
    ])

    concluidas = len([
        tarefa
        for tarefa in tarefas_db
        if tarefa["status"] == StatusEnum.concluida
    ])

    canceladas = len([
        tarefa
        for tarefa in tarefas_db
        if tarefa["status"] == StatusEnum.cancelada
    ])

    return {
        "total": total,
        "pendentes": pendentes,
        "em_andamento": em_andamento,
        "concluidas": concluidas,
        "canceladas": canceladas
    }


# ==========================================================
# LISTAR TAREFAS
# ==========================================================

@router.get(
    "/",
    response_model=list[TarefaSaida],
    summary="Lista tarefas com filtros"
)
def listar_tarefas(
    status: StatusEnum | None = Query(default=None),
    prioridade: PrioridadeEnum | None = Query(default=None),
    responsavel: str | None = Query(default=None)
):
    resultado = tarefas_db

    if status:
        resultado = [
            tarefa
            for tarefa in resultado
            if tarefa["status"] == status
        ]

    if prioridade:
        resultado = [
            tarefa
            for tarefa in resultado
            if tarefa["prioridade"] == prioridade
        ]

    if responsavel:
        resultado = [
            tarefa
            for tarefa in resultado
            if tarefa["responsavel"].lower() == responsavel.lower()
        ]

    return resultado


# ==========================================================
# CRIAR TAREFA
# ==========================================================

@router.post(
    "/",
    response_model=TarefaSaida,
    summary="Cria uma nova tarefa"
)
def criar_tarefa(tarefa: TarefaEntrada):

    novo_id = max(
        [item["id"] for item in tarefas_db],
        default=0
    ) + 1

    nova_tarefa = {
        "id": novo_id,
        "titulo": tarefa.titulo,
        "descricao": tarefa.descricao,
        "responsavel": tarefa.responsavel,
        "prioridade": tarefa.prioridade,
        "status": tarefa.status,
        "tags": tarefa.tags
    }

    tarefas_db.append(nova_tarefa)

    return nova_tarefa


# ==========================================================
# NOVA ROTA:
# TAREFAS COM PRIORIDADE CRÍTICA
#
# IMPORTANTE:
# ESTA ROTA FICA ANTES DE /{tarefa_id}
# ==========================================================

@router.get(
    "/prioridade/critica",
    response_model=list[TarefaSaida],
    summary="Lista tarefas críticas"
)
def listar_tarefas_criticas():

    return [
        tarefa
        for tarefa in tarefas_db
        if tarefa["prioridade"] == PrioridadeEnum.critica
        and tarefa["status"] not in [
            StatusEnum.concluida,
            StatusEnum.cancelada
        ]
    ]


# ==========================================================
# NOVA ROTA:
# TAREFAS POR RESPONSÁVEL
#
# IMPORTANTE:
# ESTA ROTA FICA ANTES DE /{tarefa_id}
# ==========================================================

@router.get(
    "/responsavel/{nome}",
    response_model=list[TarefaSaida],
    summary="Busca tarefas por responsável"
)
def listar_tarefas_por_responsavel(
    nome: str = Path(
        ...,
        min_length=2,
        description="Nome do responsável"
    )
):

    resultado = [
        tarefa
        for tarefa in tarefas_db
        if tarefa["responsavel"].lower() == nome.lower()
    ]

    if not resultado:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma tarefa encontrada para este responsável"
        )

    return resultado


# ==========================================================
# NOVA ROTA:
# ALTERAR SOMENTE O STATUS
# ==========================================================

@router.patch(
    "/{tarefa_id}/status",
    response_model=TarefaSaida,
    summary="Atualiza somente o status"
)
def atualizar_status(
    tarefa_id: int,
    dados: StatusAtualizacao
):

    for tarefa in tarefas_db:

        if tarefa["id"] == tarefa_id:

            if tarefa["status"] == StatusEnum.cancelada:

                raise HTTPException(
                    status_code=400,
                    detail="Não é possível alterar o status de uma tarefa cancelada"
                )

            tarefa["status"] = dados.status

            return tarefa

    raise HTTPException(
        status_code=404,
        detail="Tarefa não encontrada"
    )


# ==========================================================
# BUSCAR TAREFA POR ID
# ==========================================================

@router.get(
    "/{tarefa_id}",
    response_model=TarefaSaida,
    summary="Busca uma tarefa pelo ID"
)
def buscar_tarefa(tarefa_id: int):

    for tarefa in tarefas_db:

        if tarefa["id"] == tarefa_id:
            return tarefa

    raise HTTPException(
        status_code=404,
        detail="Tarefa não encontrada"
    )


# ==========================================================
# PUT
# ==========================================================

@router.put(
    "/{tarefa_id}",
    response_model=TarefaSaida,
    summary="Substitui uma tarefa inteira"
)
def atualizar_tarefa(
    tarefa_id: int,
    dados: TarefaEntrada
):

    for tarefa in tarefas_db:

        if tarefa["id"] == tarefa_id:

            tarefa["titulo"] = dados.titulo
            tarefa["descricao"] = dados.descricao
            tarefa["responsavel"] = dados.responsavel
            tarefa["prioridade"] = dados.prioridade
            tarefa["status"] = dados.status
            tarefa["tags"] = dados.tags

            return tarefa

    raise HTTPException(
        status_code=404,
        detail="Tarefa não encontrada"
    )


# ==========================================================
# PATCH
# ==========================================================

@router.patch(
    "/{tarefa_id}",
    response_model=TarefaSaida,
    summary="Atualiza campos específicos"
)
def atualizar_campos(
    tarefa_id: int,
    dados: dict
):

    for tarefa in tarefas_db:

        if tarefa["id"] == tarefa_id:

            for campo, valor in dados.items():

                if campo in [
                    "titulo",
                    "descricao",
                    "responsavel",
                    "prioridade",
                    "status",
                    "tags"
                ]:
                    tarefa[campo] = valor

            return tarefa

    raise HTTPException(
        status_code=404,
        detail="Tarefa não encontrada"
    )


# ==========================================================
# DELETE
# ==========================================================

@router.delete(
    "/{tarefa_id}",
    summary="Remove uma tarefa"
)
def remover_tarefa(tarefa_id: int):

    for tarefa in tarefas_db:

        if tarefa["id"] == tarefa_id:

            tarefas_db.remove(tarefa)

            return {
                "mensagem": "Tarefa removida com sucesso"
            }

    raise HTTPException(
        status_code=404,
        detail="Tarefa não encontrada"
    )