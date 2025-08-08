from sqlalchemy.orm import Session
from app.core.database import engine, Base, get_db
from app.models import Clinica

# Ensure tables are created
Base.metadata.create_all(bind=engine)

def create_sample_clinicas():
    db: Session = next(get_db())
    try:
        clinicas_data = [
            {"nome": "Clínica A", "endereco": "Rua A, 123", "telefone": "1111-1111", "num_guiches": 2, "tempo_minimo_atendimento": 20},
            {"nome": "Clínica B", "endereco": "Rua B, 456", "telefone": "2222-2222", "num_guiches": 3, "tempo_minimo_atendimento": 25},
            {"nome": "Clínica C", "endereco": "Rua C, 789", "telefone": "3333-3333", "num_guiches": 1, "tempo_minimo_atendimento": 30},
        ]

        for clinica_data in clinicas_data:
            # Check if clinic already exists to prevent duplicates
            existing_clinica = db.query(Clinica).filter(Clinica.nome == clinica_data["nome"]).first()
            if not existing_clinica:
                clinica = Clinica(**clinica_data)
                db.add(clinica)
                print(f"Adding clinic: {clinica.nome}")
            else:
                print(f"Clinic already exists: {clinica_data['nome']}")
        db.commit()
        print("Sample clinics added successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error adding sample clinics: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_clinicas()
