from fastapi import APIRouter, HTTPException
from dataclasses import dataclass
from routers import RetornoCalculo, format_datetime_pt_br
import datetime, math

router = APIRouter(
    prefix='/api/v1',
    tags=['utils']
)

@dataclass
class IdadeGestacional:
    semana: int
    dia: int 

    def __str__(self) -> str:
        return f"{self.semana} semana(s) e {self.dia} dia(s)"
    
    def abrev(self) -> str:
        return f"{self.semana}s{self.dia}d"
    
    def total_dias(self) -> int:
        return self.semana * 7 + self.dia
    
    def dum(self) -> datetime.date:
        return datetime.date.today() - datetime.timedelta(weeks=self.semana, days=self.dia)

@router.post("/marcos-gravidez")
async def post_utils_marcos_gravidez(dum:datetime.date = None, data_exame:datetime.date = None, idade_gestacional:IdadeGestacional = None) -> RetornoCalculo:
    # Meses de gestação
    # Verifica campos obrigatórios, necessita que ou dum seja preenchido ou o conjunto de data do exame e idade gestacional referido no momento do exame
    if dum is None and data_exame is None and idade_gestacional is None:
        raise HTTPException(status_code=422, detail="É necessário que a DUM ou a data do exame e Idade Gestacional no exame seja preenchidos")
    if dum is None and data_exame is None or idade_gestacional is None:
        raise HTTPException(status_code=422, detail="É necessário que a DUM ou a data do exame e Idade Gestacional no exame seja preenchidos")
    # Se tiver presente a DUM calcula a idade gestacional
    if dum is not None:
        delta_idade_gestacional_dum = datetime.date.today() - dum
        idade_gestacional_dum = IdadeGestacional(semana=delta_idade_gestacional_dum.days//7, dia=delta_idade_gestacional_dum.days%7)
        idade_gestacional_calculada = idade_gestacional_dum
        dum_calculada = dum
    # Verifica se tem dados de ultrassonografia
    if data_exame is not None and idade_gestacional is not None:
        dum_exame = data_exame - datetime.timedelta(days=idade_gestacional.total_dias())
        delta_idade_gestacional_exame = datetime.date.today() - dum_exame
        idade_gestacional_exame = IdadeGestacional(semana=delta_idade_gestacional_exame.days//7, dia=delta_idade_gestacional_exame.days%7)
        idade_gestacional_calculada = idade_gestacional_exame
        dum_calculada = dum_exame
    
    if "idade_gestacional_dum" in locals() and "idade_gestacional_exame" in locals():
        # Caso as duas idades gestacionais estejam presentes, verifica qual melhor idade gestacional a ser utilizada
        delta_ig_dias = math.floor(0.08 * idade_gestacional_exame.total_dias())
        if idade_gestacional_dum.total_dias() > idade_gestacional_exame.total_dias() - delta_ig_dias and idade_gestacional_dum.total_dias() < idade_gestacional_exame.total_dias() + delta_ig_dias:
            idade_gestacional_calculada = idade_gestacional_dum
            dum_calculada = dum
        else:
            idade_gestacional_calculada = idade_gestacional_exame

    copiarecolar_idade_gestacional = ""
    if "idade_gestacional_dum" in locals():
        copiarecolar_idade_gestacional += f"IG {idade_gestacional_dum.abrev()} pela DUM"
    
    observacoes = ""
    if idade_gestacional_calculada is not None and idade_gestacional_calculada.semana < 7:
        observacoes = "A datação preferencial deve ser feita por CCN com embrião acima de 10mm e batimentos fetais presentes"
    
    def adicionar_semanas_dum(semanas:int=0, dias:int=0) -> str:
        return format_datetime_pt_br( idade_gestacional_calculada.dum() + datetime.timedelta(weeks=semanas, days=dias))
    
    # TODO Colocar a regra de medicina fetal 8% calcular pela DUM, preferencialmente
    return RetornoCalculo(resultado={
        "idade_gestacional": str(idade_gestacional_calculada),
        "dum_calculada_inicio_primeiro_trimestre": format_datetime_pt_br(dum_calculada),
        "inicio_segundo_trimestre_14_sem": adicionar_semanas_dum(14),
        "inicio_terceiro_trimestre_27_sem": adicionar_semanas_dum(27),
        "dpp_40_semanas": adicionar_semanas_dum(40),
        "termo_precoce": f"de {adicionar_semanas_dum(37)} a {adicionar_semanas_dum(38,6)}",
        "termo_completo": f"de {adicionar_semanas_dum(39)} a {adicionar_semanas_dum(40,6)}",
        "termo_tardio": f"de {adicionar_semanas_dum(41)} a {adicionar_semanas_dum(42)}",
        "pos_termo": f"após {adicionar_semanas_dum(42)}",
        "exames":{
            "usg_morfologica_primeiro_trimestre": f"de {adicionar_semanas_dum(11)} a {adicionar_semanas_dum(13,6)}",
            "usg_morfologica_primeiro_trimestre_melhor_data": adicionar_semanas_dum(13),
            "usg_morfologica_segundo_trimestre": f"de {adicionar_semanas_dum(20)} a {adicionar_semanas_dum(23,6)}",
            "usg_morfologica_segundo_trimestre_melhor_data": adicionar_semanas_dum(22),
            "teste_oral_tolerancia_glicose": adicionar_semanas_dum(24),
        }
    }, copiarecolar=[copiarecolar_idade_gestacional, "Solicitados exames gestacionais: "], observacoes=f"Acesse https://docs.filipelopes.med.br para gerar os documentos de forma automática. Veja mais informações sobre marcos em https://www.fetalmed.net/calculadora/calculadora-idade-gestacional. {observacoes}")


@router.post("/conversao-medidas")
async def post_utils_conversao_medidas():
    # Conversão, microgotas...
    return {"message": "Hello World"}


@router.post("/calculo-infusao")
async def post_utils_calculo_infusao():
    # Conversão, microgotas...
    return {"message": "Hello World"}
