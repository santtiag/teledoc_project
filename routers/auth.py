from fastapi import APIRouter, HTTPException, Request, Response, Form
from pydantic import BaseModel
from config.database import Session
from jwt_manager import create_token, validate_token
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPBearer

from fastapi.templating import Jinja2Templates
from models.physician_model import Physician as PhysicianModel


auth_router = APIRouter()
templates = Jinja2Templates(directory="templates")

class User(BaseModel):
    email: str
    id: str

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        # Extraer el token de las cookies en lugar del encabezado
        token = request.cookies.get("access_token")
        if not token:
            raise HTTPException(status_code=403, detail="Not authenticated")

        data = validate_token(token)  # Validar el token
        db = Session()
        physician = db.query(PhysicianModel).filter(PhysicianModel.email == data['email']).first()
        if not physician:
            raise HTTPException(status_code=403, detail="Credenciales inválidas")
        request.state.physician = physician
        return token

# Mostrar formulario de login usando Jinja2
@auth_router.get('/login', response_class=HTMLResponse, tags=['Auth'])
async def show_login_form(request: Request):
    return templates.TemplateResponse("login_form.html", {"request": request})

# Autenticar el usuario y almacenar el token en cookies
@auth_router.post('/auth', tags=['Auth'])
async def login(response: Response, email: str = Form(...), id: str = Form(...)):
    db = Session()
    physician = db.query(PhysicianModel).filter(PhysicianModel.email == email).first()
    if not physician or physician.identity_card != id:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    # Crear el token JWT
    token: str = create_token({"email": email, "id": id})

    # Almacenar el token en cookies HTTPOnly (más seguro que localStorage)
    response = RedirectResponse(url='/patient', status_code=302)
    response.set_cookie(key="access_token", value=token, httponly=True, secure=True)

    return response


# @auth_router.get('/home', response_class=HTMLResponse, tags=['Auth'])
# async def show_login_form(request: Request):
#     return templates.TemplateResponse("login_form.html", {"request": request})

# # INFO: AUTH
# @auth_router.post('/auth', tags=['Auth'])
# async def login(user: User):
#     db = Session()
#     physician = db.query(PhysicianModel).filter(PhysicianModel.email == user.email).first()
#     if not physician or physician.identity_card != user.id:
#         raise HTTPException(status_code=401, detail="Credenciales inválidas")
#     token: str = create_token(user.dict())
#     return JSONResponse(content=token)
