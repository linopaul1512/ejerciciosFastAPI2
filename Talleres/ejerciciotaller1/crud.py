from sqlalchemy.orm import Session
import models, schemas
from pydantic import Field




#Buscar todos los items
def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

#Crear item
def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.model_dump())
    print("DB item: ", db_item)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    print("Db items: ", db_item)
    return db_item
