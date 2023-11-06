from fastapi import APIRouter, Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    tags = ['router']
)

@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def index(request: Request, q: str = None):   
    print(request.__dict__)
    with open("data.json", "r") as read_file:
        data = json.load(read_file)
    return templates.TemplateResponse("index.html", {"request": request, "item_list": data})

@router.get("/drogas-intubacao-ga", response_class=HTMLResponse, include_in_schema=False)
async def drogas_intubacao_ga(request: Request):   
    return templates.TemplateResponse("intubacao_sedacao_ga.html", {"request":request})

@router.get("/5h5t", response_class=HTMLResponse, include_in_schema=False)
async def causas_pcr(request: Request):   
    return templates.TemplateResponse("5h5t.html", {"request":request})

@router.get("/doses-pediatricas", response_class=HTMLResponse, include_in_schema=False)
async def doses_pediatricas(request: Request):   
    return templates.TemplateResponse("doses_pediatricas.html", {"request":request})

@router.get("/trechos-exames", response_class=HTMLResponse, include_in_schema=False)
async def trechos_exames(request: Request):   
    return templates.TemplateResponse("trechos.html", {"request":request})

@router.get("/trechos-receitas", response_class=HTMLResponse, include_in_schema=False)
async def trechos_receitas(request: Request):   
    return templates.TemplateResponse("receituario.html", {"request":request})