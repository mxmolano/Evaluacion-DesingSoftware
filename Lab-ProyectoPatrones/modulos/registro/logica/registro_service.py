import json
from fastapi import APIRouter, Request, HTTPException
from modulos.registro.acceso_datos.get_factory import obtener_dao
from modulos.registro.acceso_datos.registro_dto import RegistroDTO

dao = obtener_dao()
router = APIRouter()

@router.post("/")
async def crear_registro(req: Request):
    data = await req.json()
    registro = RegistroDTO(
        nombre=data["nombre"],
        apellido=data["apellido"],
        nacimiento=data["nacimiento"],
        email=data["email"],
        contraseña=data["contraseña"]
    )
    
    try:  
        dao.guardar(registro)
        return {"mensaje": "Registro almacenado correctamente."}
    except ValueError as ve: 
        raise HTTPException(status_code=409, detail=str(ve))  

@router.get("/")
def obtener_registros():
    # Excluye la contraseña al devolver los datos
    return [
        {k: v for k, v in r.__dict__.items() if k != "contraseña"}
        for r in dao.obtener_todos()
    ]

@router.get("/{id}")
def obtener_registro(id: int):
    registro = dao.obtener_por_id(id)
    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return {k: v for k, v in registro.__dict__.items() if k != "contraseña"}

@router.put("/{id}")
async def actualizar_registro(id: int, req: Request):
    data = await req.json()
    actualizado = RegistroDTO(
        id=id,
        nombre=data["nombre"],
        apellido=data["apellido"],
        nacimiento=data["nacimiento"],
        email=data["email"],
        contraseña=data["contraseña"]
    )
    
    try:  
        dao.actualizar(id, actualizado)
        return {"mensaje": "Registro actualizado"}
    except ValueError as ve:  
        raise HTTPException(status_code=409, detail=str(ve)) 

@router.delete("/{id}")
def eliminar_registro(id: int):
    dao.eliminar(id)
    return {"mensaje": "Registro eliminado"}