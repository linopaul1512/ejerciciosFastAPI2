import _asyncio
from pydantic import Field
import threading
from sqlalchemy.orm import Session


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


def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items



async def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    for item in dummy_users_db():
        dummy_users_db()
    return crud.create_item(db=db, item=item)



threadin_create_item = threading.Thread(target=create_item)
threadin_read_items = threading.Thread(target=read_items)



threadin_create_item.start()
threadin_read_items.start()
