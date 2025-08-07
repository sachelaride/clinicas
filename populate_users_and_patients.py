from sqlalchemy.orm import Session
from app.core.database import engine, get_db
from app.models import User, Clinica, Paciente, Profissional, UserProfileEnum
from app.core.security import get_password_hash
from faker import Faker

faker = Faker('pt_BR')

def populate_users_and_patients():
    db: Session = next(get_db())
    try:
        clinicas = db.query(Clinica).all()
        if not clinicas:
            print("No clinics found. Please run populate_clinics_and_services.py first.")
            return

        # Ensure admin user exists and is linked to the first clinic
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            hashed_password = get_password_hash("adminpass")
            admin_user = User(
                username="admin",
                email="admin@example.com",
                hashed_password=hashed_password,
                perfil=UserProfileEnum.ADMIN,
                clinica_id=clinicas[0].id
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            print(f"Created admin user: {admin_user.username} for {clinicas[0].nome}")
        elif admin_user.clinica_id is None:
            admin_user.clinica_id = clinicas[0].id
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            print(f"Linked existing admin user to clinic: {clinicas[0].nome}")

        for clinica in clinicas:
            print(f"\nPopulating users and patients for {clinica.nome}...")

            # Create Atendente user
            atendente_username = f"atendente_{clinica.id}"
            if not db.query(User).filter(User.username == atendente_username).first():
                hashed_password = get_password_hash("atendente123")
                atendente = User(
                    username=atendente_username,
                    email=f"atendente{clinica.id}@example.com",
                    hashed_password=hashed_password,
                    perfil=UserProfileEnum.ATENDENTE,
                    clinica_id=clinica.id
                )
                db.add(atendente)
                db.commit()
                db.refresh(atendente)
                print(f"  Created atendente: {atendente.username}")

            # Create Profissional user and profile
            profissional_username = f"prof_{clinica.id}"
            if not db.query(User).filter(User.username == profissional_username).first():
                hashed_password = get_password_hash("prof123")
                profissional_user = User(
                    username=profissional_username,
                    email=f"prof{clinica.id}@example.com",
                    hashed_password=hashed_password,
                    perfil=UserProfileEnum.PROFISSIONAL,
                    clinica_id=clinica.id
                )
                db.add(profissional_user)
                db.commit()
                db.refresh(profissional_user)

                profissional_profile = Profissional(
                    user_id=profissional_user.id,
                    especialidade=faker.job(),
                    conselho_profissional="CRM/SP",
                    numero_conselho=faker.unique.random_number(digits=6)
                )
                db.add(profissional_profile)
                db.commit()
                print(f"  Created profissional: {profissional_user.username}")

            # Create 5 Paciente profiles (NOT users)
            for i in range(1, 6):
                # Using a deterministic CPF for testing purposes
                test_cpf = f"{(i * 1000 + clinica.id):011d}"
                if not db.query(Paciente).filter(Paciente.cpf == test_cpf).first():
                    paciente_profile = Paciente(
                        nome=faker.name(),
                        cpf=test_cpf,
                        rg=faker.unique.rg(),
                        data_nascimento=faker.date_of_birth(minimum_age=18, maximum_age=90),
                        email=faker.unique.email(),
                        telefone=faker.phone_number(),
                        endereco=faker.address(),
                        clinica_id=clinica.id
                    )
                    db.add(paciente_profile)
                    db.commit()
                    print(f"  Created paciente profile: {paciente_profile.nome} for {clinica.nome}")
                else:
                    print(f"  Patient profile with CPF {test_cpf} already exists for {clinica.nome}")

        print("\nUsers (non-patients) and patient profiles populated successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error populating users and patients: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    populate_users_and_patients()
