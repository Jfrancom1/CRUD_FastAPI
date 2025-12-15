from typing import List
from fastapi import APIRouter, Depends, Query, status, HTTPException;
from sqlalchemy.orm import Session
from faker import Faker;
import random;
from ..models.persona import Persona
from datetime import date;

from ..database import get_db
from ..views.persona import PersonaCreate, PersonaUpdate, PersonaRead
from ..services import persona_service

router = APIRouter(prefix="/personas", tags=["personas"])
faker = Faker("es_CO")

@router.post("", response_model=PersonaRead, status_code=status.HTTP_201_CREATED)
def create_persona(persona_in: PersonaCreate, db: Session = Depends(get_db)):
    """Create a new Persona delegating to service layer."""
    # Let domain errors bubble up to global handlers
    return persona_service.create_persona(db, persona_in)


@router.get("", response_model=List[PersonaRead])
def list_personas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """List Personas with pagination via service layer."""
    return persona_service.list_personas(db, skip=skip, limit=limit)


@router.get("/{persona_id}", response_model=PersonaRead)
def get_persona(persona_id: int, db: Session = Depends(get_db)):
    """Retrieve a Persona by ID via service layer."""
    return persona_service.get_persona(db, persona_id)


@router.put("/{persona_id}", response_model=PersonaRead)
def update_persona(persona_id: int, persona_in: PersonaUpdate, db: Session = Depends(get_db)):
    """Update an existing Persona (partial) via service layer."""
    return persona_service.update_persona(db, persona_id, persona_in)


@router.delete("/{persona_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_persona(persona_id: int, db: Session = Depends(get_db)):
    """Delete a Persona by ID via service layer."""
    persona_service.delete_persona(db, persona_id)
    return None

@router.post("/poblar", status_code=201)
def poblar_personas(cantidad: int, db: Session = Depends(get_db)):

    if cantidad <= 0 or cantidad > 1000:
        raise HTTPException(status_code=400, detail="Cantidad inválida")

    dominios = ["gmail.com", "outlook.com", "hotmail.com"]

    for _ in range(cantidad):
        persona = Persona(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            email=f"{faker.first_name().lower()}.{faker.last_name().lower()}@{random.choice(dominios)}",
            phone=faker.phone_number(),
            birth_date=faker.date_of_birth(minimum_age=18, maximum_age=85),
            is_active=random.choice([True, False]),
            notes=None
        )
        db.add(persona)

    db.commit()

    return {"message": f"{cantidad} usuarios creados"}
