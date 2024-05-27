from typing import Annotated
from fastapi import Depends, FastAPI, File, Header



app = FastAPI()

def getlastname(lastname:Annotated[str, Header()]):
    return lastname


class User:
    def __init__(
        self,
        firstname: str,
        lastname:Annotated[str, Depends(getlastname)]
        ):
        self.firstname = firstname
        self.lastname = lastname

    @property
    def full_name(self) -> str:
        return f'{self.firstname}  {self.lastname}'
    

@app.post('/hello')
def hello(user: Annotated[User, Depends(User)]):
    return f'Hello  {user.full_name}'

@app.post('/goodbye')
def goodbye(lastname: str = Depends(getlastname)):
    return f'Bye  {lastname}'