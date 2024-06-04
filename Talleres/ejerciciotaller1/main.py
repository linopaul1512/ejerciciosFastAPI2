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
import threading


# Crear todas las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

# Inicializar la aplicación FastAPI
app = FastAPI()


# Dependencia para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# Base de datos simulada de usuarios
dummy_users_db = {
    "Johndoe": {
        "name": "johndoe",
        "description": "johndoe@example.com",
        "disabled": True
    },
    "Alice": {
        "name": "alice",
        "description": "alice@example.com",
        "disabled": True
    },
    "Siberia": {
        "name": "sibeia",
        "description": "siberia@example.com",
        "disabled": True
    },
    "Lino": {
        "name": "lino",
        "description": "lino@example.com",
        "disabled": True
    },
    "Ari": {
        "name": "arianna",
        "description": "arianna@example.com",
        "disabled": True
    },
    "Paula": {
        "name": "paula",
        "description": "paula@example.com",
        "disabled": True
    },
    "Jesus": {
        "name": "jesus",
        "description": "jesus@example.com",
        "disabled": True
    },
    "Abner": {
        "name": "abner",
        "description": "abner@example.com",
        "disabled": True
    },
    "Gabriel": {
        "name": "gabriel",
        "description": "gabriel@example.com",
        "disabled": True
    },
    "Anderson": {
        "name": "anderson",
        "description": "anderson@example.com",
        "disabled": True
    }
}

# Ruta para buscar todos los items
@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


# Ruta para crear item
@app.post("/item/create/", response_model=schemas.Item)
async def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    for item in dummy_users_db():
        dummy_users_db()
    return crud.create_item(db=db, item=item)


threadin_item = threading.Thread(target=get_db)
threadin_create_item = threading.Thread(target=create_item)
threadin_read_items = threading.Thread(target=read_items)


threadin_item.start()
threadin_create_item.start()
threadin_read_items.start()
