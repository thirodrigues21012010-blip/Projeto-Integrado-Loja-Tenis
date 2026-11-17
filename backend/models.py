"""Entidades do domínio; persistência fica nos DAOs."""
from dataclasses import dataclass, asdict

@dataclass
class Usuario:
    id_usuario: int
    nome_completo: str
    email: str
    perfil: str
    def publico(self):
        return asdict(self)

@dataclass
class Modelo:
    nome: str
    marca: str
    descricao: str = ''

@dataclass
class Coloracao:
    id_modelo: int
    cor: str
    preco: float

@dataclass
class Variante:
    id_coloracao: int
    tamanho: str
    quantidade_estoque: int
