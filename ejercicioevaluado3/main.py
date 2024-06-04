from fastapi import Depends, FastAPI, Request, HTTPException, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import crud, models, schemas
from sqlApp.database import SessionLocal, engine
from starlette.responses import RedirectResponse, HTMLResponse
from starlette.status import HTTP_303_SEE_OTHER
from fastapi import Depends
# Crear todas las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

# Inicializar la aplicación FastAPI
app = FastAPI()

# Montar el directorio estático para servir archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

#Ya 
# Configurar Jinja2 para la renderización de plantillas
templates = Jinja2Templates(directory="templates")

# Dependencia para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ruta para buscar todos los items
@app.get("/", response_class=HTMLResponse, name="read_items")
async def read_items(request: Request, db: Session = Depends(get_db)):
    items = crud.get_items(db)
    return templates.TemplateResponse("listaItem.html", {"request": request, "items": items})

# Ruta para crear item
@app.post("/item/create/", response_model=schemas.Item)
async def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db=db, item=item)

# Ruta para buscar item por id
@app.get("/item/{item_id}", response_class=HTMLResponse)
async def read_item(request: Request, item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return templates.TemplateResponse("item_detail.html", {"request": request, "item": item})

# Ruta para modificar item
@app.put("/items/update/{item_id}", response_model=schemas.Item)
async def modificar_item(item_id: int, item_update: schemas.ItemUpdate, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return crud.update_item(db=db, item_id=item_id, item_update=item_update)

# Ruta para eliminar item
@app.delete("/items/delete/{item_id}", response_model=schemas.Item)
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    deleted_item = crud.delete_item(db, item_id=item_id)
    return deleted_item