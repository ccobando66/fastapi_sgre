from fastapi import FastAPI,Depends
from .models.configuracion import Base
from .config.database import engine
from .routers import (
    user,personal,admin,login,equipo,
    configuracion
)
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(engine)

app = FastAPI(title='sgre(Sistema gestión redes empresariales)',
              description='Sistema de control de configuración equipos de red activos gestionable',
              version="1.0.0",
              license_info={
                "name": "Apache 2.0",
                 "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
               },
              )

#cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_headers=['*'],
    allow_methods=['*']
)



#routers
app.include_router(user.router)
app.include_router(personal.router)
app.include_router(admin.router)
app.include_router(login.router)
app.include_router(equipo.router)
app.include_router(configuracion.router)


@app.get('/')
async def root():
    return {'sms':'hello_word'}