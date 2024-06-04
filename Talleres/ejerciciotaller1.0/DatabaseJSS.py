from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker
from fastapi import Depends, FastAPI, Request, HTTPException

engine = create_engine('sqlite://ejerciciotaller1.0/sql_app.sqlite')
engine.connect()

Base = declarative_base()
Session = sessionmaker(bind = engine)