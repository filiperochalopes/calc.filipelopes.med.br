from dataclasses import dataclass
from datetime import date


def format_datetime_pt_br(date: date) -> str:
    lista_meses_pt_br = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    return f"{date.day} de {lista_meses_pt_br[date.month-1]} de {date.year}"


@dataclass
class RetornoCalculo:
    resultado: dict
    referencias: str = None
    copiarecolar: list[str] | str = None
    observacoes: str = None
    interpretacao: str = None
