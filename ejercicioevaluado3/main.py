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
@app.get("/", response_class=HTMLResponse)
async def read_items(request: Request, db: Session = Depends(get_db)):
    """
    Esta ruta maneja la solicitud GET a la URL raíz ("/").
    Busca todos los items en la base de datos y renderiza la plantilla 'listaItem.html',
    pasando la lista de items a la plantilla.
    """
    items = crud.get_items(db)
    return templates.TemplateResponse("listaItem.html", {"request": request, "items": items})

# Ruta para mostrar el formulario de crear item
@app.get("/item/create/", response_class=HTMLResponse)
async def create_item_form(request: Request):
    """
    Esta ruta maneja la solicitud GET a la URL "/item/create/".
    Renderiza la plantilla 'agregarItem.html', que contiene el formulario para crear un nuevo item.
    """
    return templates.TemplateResponse("agregarItem.html", {"request": request})

# Ruta para crear item
@app.post("/item/create/", response_class=HTMLResponse)
async def create_item(request: Request, name: str = Form(...), description: str = Form(...), db: Session = Depends(get_db)):
    """
    Esta ruta maneja la solicitud POST a la URL "/item/create/".
    Recibe los datos del formulario (nombre y descripción) y crea un nuevo item en la base de datos.
    Luego redirige a la URL raíz ("/") para mostrar la lista actualizada de items.
    """
    item = schemas.ItemCreate(name=name, description=description)
    crud.create_item(db=db, item=item)
    return RedirectResponse("/", status_code=HTTP_303_SEE_OTHER)

# Ruta para buscar item por id
@app.get("/items/{item_id}", response_class=HTMLResponse)
async def get_item(request: Request, item_id: int, db: Session = Depends(get_db)):
    """
    Esta ruta maneja la solicitud GET a la URL "/items/{item_id}".
    Busca un item en la base de datos por su ID. Si el item no existe, lanza un HTTP 404.
    Si el item existe, renderiza la plantilla 'detalles.item', pasando el item a la plantilla.
    """
    db_item = crud.item_id(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return templates.TemplateResponse("detalles.html", {"request": request, "item": db_item})

# Ruta para mostrar el formulario de modificar item
@app.get("/items/update/{item_id}", response_class=HTMLResponse)
async def modificar_item_form(request: Request, item_id: int, db: Session = Depends(get_db)):
    """
    Esta ruta maneja la solicitud GET a la URL "/items/update/{item_id}".
    Busca un item en la base de datos por su ID. Si el item no existe, lanza un HTTP 404.
    Si el item existe, renderiza la plantilla 'modificarItem.html', pasando el item a la plantilla para su edición.
    """
    item = crud.get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return templates.TemplateResponse("modificarItem.html", {"request": request, "item": item})

# Ruta para modificar item
@app.post("/items/update/{item_id}", response_class=HTMLResponse)
async def modificar_item(request: Request, item_id: int, name: str = Form(...), description: str = Form(...), db: Session = Depends(get_db)):
    """
    Esta ruta maneja la solicitud POST a la URL "/items/update/{item_id}".
    Recibe los datos del formulario (nombre y descripción) y actualiza el item en la base de datos.
    Luego redirige a la URL raíz ("/") para mostrar la lista actualizada de items.
    """
    item_update = schemas.ItemUpdate(name=name, description=description)
    crud.update_item(db=db, item_id=item_id, item=item_update)
    return RedirectResponse("/", status_code=HTTP_303_SEE_OTHER)

# Ruta para eliminar item
@app.post("/items/delete/{item_id}", response_class=HTMLResponse)
async def delete_item(request: Request, item_id: int, db: Session = Depends(get_db)):
    """
    Esta ruta maneja la solicitud POST a la URL "/items/delete/{item_id}".
    Busca un item en la base de datos por su ID. Si el item no existe, lanza un HTTP 404.
    Si el item existe, lo elimina de la base de datos y redirige a la URL raíz ("/")
    para mostrar la lista actualizada de items.
    """
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    crud.delete_item(db, item_id=item_id)
    return RedirectResponse("/", status_code=HTTP_303_SEE_OTHER)
