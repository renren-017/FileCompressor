from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.api.compression import router as compression_router

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(compression_router, prefix="/api", tags=["compression"])


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html(request: Request):
    return templates.TemplateResponse(
        "custom_swagger_ui.html",
        {"request": request},
        media_type="text/html",
    )


@app.get("/compress/", response_class=HTMLResponse)
async def compress(request: Request):
    return templates.TemplateResponse("compress.html", {"request": request, "name": "compress"})


@app.get("/index/", response_class=HTMLResponse)
async def index(request: Request):
    compress_url = request.url_for("compress")
    docs_url = request.url_for("custom_swagger_ui_html")
    return templates.TemplateResponse("index.html", {"request": request, "docs_url": docs_url, "compress_url": compress_url, "name": "index"})
