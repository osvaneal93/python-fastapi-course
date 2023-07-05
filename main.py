from fastapi import Depends, FastAPI, Body, HTTPException, Path, Query, Request
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Optional
from fastapi.responses import JSONResponse
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer


app = FastAPI()
app.title = 'Learning FastApi'
app.version = '0.0.1'


#----auth
#------------------------------------
class User(BaseModel):
    email:str
    password: str

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != 'admin@gmail.com':
            raise HTTPException(status_code=403, detail="Credenciales Inválidas")

@app.post("/login", tags= ['Auth'])
def login(user: User):
    if user.email == 'admin@gmail.com' and user.password == 'admin':
        token: str = create_token(user.dict())
        print('TOKEEEEEENNN' + token)
        return JSONResponse(status_code=200, content= token)
    return JSONResponse(status_code=400, content= {'error':'Usuario o contrasena incorrectos.'})


#movies
#-----------------------------

class Movie(BaseModel):
    id : Optional[int] = None
    title:str = Field(min_length=5, max_length=30)
    overview: str = Field(min_length=5, max_length=50)
    year: int = Field(le= 2023, gt=0, )
    rating: float = Field(le= 10, gt=0, )
    category: str = Field(min_length=5, max_length=50)

    class Config:
        schema_extra = {
            "example":{
                "id":1,
                "title":"The Avengers pt.2",
                'Overview':'Avengers are in problems with the Treseracto but they use tha friendship powers.',
                "year":2023,
                "rating":9.9,
                "category":"Action"
                }
        }
movies = [Movie(
        id = 1,
        title = 'Avatar the Weather Kindom',
        overview = "En un exuberante planeta llamado Pandora ",
        year = 2009,
        rating = 7.8,
        category = 'Acción'  
        ),
        Movie(
        id = 2,
        title = 'Bad Bunny The Music  Kindom',
        overview = "La vida de Bad Bunny",
        year = 2015,
        rating = 10,
        category = 'Musica'   
        )
        ]

@app.get('/', tags = ["Home"])
def message():
    return 'hello world'

@app.get('/movies', tags = ['Movies'], response_model=list[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> list[Movie]:
    return movies

@app.get('/movies/{id}', tags = ['Movies'], status_code=200, response_model=Movie)
def get_movies_by_id(id:int = Path(ge=1)) -> Movie:
    for i in movies:
        print(" INDICE ---->  " + str(i))
        if i.id == id:
            return i
    return JSONResponse(status_code=404, content=[])
        
@app.get('/movies/', tags = ['Movies'])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)):
    for i in movies:
        if category == i.category:
            return i
    return []
        
@app.post('/movies', tags= ['Movies'])
def create_movie(movie: Movie):
    movies.append(movie)
    return movie

@app.put('/movies/{id}', tags=['Movies'])
def edit_movie(id : int, movie: Movie):
    for i in movies:
        print(" IDIDIDIDID ---->  " + str(id))
        print(" INDICE ---->  " + str(i.id))
        if id == i.id:
            i.title = movie.title
            i.overview = movie.overview
            i.year = movie.year
            i.rating = movie.rating
            i.category = movie.category
            print('SI HAY ESE INDICE')
            print(i)

            return i
        else:
            print('NO HAY ESE INDICE')

@app.delete('/movies/{id}', tags = ['Movies'])
def delete_movie(id: int):


    for i in movies:
        if id == i.id:
            movies.remove(i)
            return movies
        else:
            print('NO HAY ESE INDICE')

