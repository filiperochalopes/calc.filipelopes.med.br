from fastapi import APIRouter

router = APIRouter(
    prefix='/api/v1',
    tags = ['scores']
)

@router.post('/homa-ir')
async def post_score_homa_ir():
    # HOMA IR: insulina jejum (MICRO UI/mL) x glicose jejum (mmol/L*) / 22,5 (https://drpio.com.br/exames/detalhe/1001/1001#:~:text=HOMA%20IR%3A%20insulina%20jejum%20(MICRO,%2FdL%20por%200%2C0555.)
    return {"referencias": "ELSA-Brasil (https://doi.org/10.1590/0102-311X00072120)"}

@router.post('/imc')
async def post_score_imc(peso: float, altura: int):
    return {"referencias": "ELSA-Brasil (https://doi.org/10.1590/0102-311X00072120)"}