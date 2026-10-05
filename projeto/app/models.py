from datetime import date
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class StatusEnum(str, Enum):
    pendente = "pendente"
    em_andamento = "em andamento"
    concluida = "concluída"
    cancelada = "cancelada"


class PrioridadeEnum(str, Enum):
    baixa = "baixa"
    media = "média"
    alta = "alta"
    critica = "critica"


class TarefaEntrada(BaseModel):
    titulo: str
    descricao: str
    responsavel: str
    prioridade: PrioridadeEnum
    status: StatusEnum = StatusEnum.pendente
    tags: list[str] = Field(default_factory=list)

    @field_validator("tags")
    @classmethod
    def validar_tags(cls, tags):
        return list(set(tag.lower() for tag in tags))


class TarefaSaida(BaseModel):
    id: int
    titulo: str
    descricao: str
    responsavel: str
    prioridade: PrioridadeEnum
    status: StatusEnum
    criado_em: date = Field(default_factory=date.today)
    tags: list[str] = Field(default_factory=list)

    @field_validator("tags")
    @classmethod
    def validar_tags(cls, tags):
        return list(set(tag.lower() for tag in tags))


class StatusAtualizacao(BaseModel):
    status: StatusEnum