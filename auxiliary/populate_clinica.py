from sqlalchemy.orm import Session
from app.core.database import Base, engine, get_db
from app import models

def populate_clinica():
    db: Session = next(get_db())
    try:
        # Check if a default clinic already exists
        default_clinica = db.query(models.Clinica).filter(models.Clinica.nome == "Clínica Padrão").first()
        if not default_clinica:
            db_clinica = models.Clinica(
                nome="Clínica Padrão",
                endereco="Rua Exemplo, 123",
                telefone="(11) 98765-4321",
                num_guiches=2,
                tempo_minimo_atendimento=30
            )
            db.add(db_clinica)
            db.commit()
            db.refresh(db_clinica)
            print("Clínica Padrão criada com sucesso!")
        else:
            print("Clínica Padrão já existe.")
    except Exception as e:
        db.rollback()
        print(f"Erro ao popular clínica: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    populate_clinica()
