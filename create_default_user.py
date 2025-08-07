from sqlalchemy.orm import Session
from app.core.database import engine, Base, get_db
from app.models import User, Clinica, UserProfileEnum
from app.core.security import get_password_hash

# Ensure tables are created (though they should be by now)
Base.metadata.create_all(bind=engine)

def create_default_user():
    db: Session = next(get_db())
    try:
        # Check if a default user already exists
        existing_user = db.query(User).filter(User.username == "admin").first()
        if existing_user:
            print("Default user 'admin' already exists.")
            return

        # Get the first clinic to associate the user with
        first_clinica = db.query(Clinica).first()
        if not first_clinica:
            print("No clinics found. Please ensure clinics are populated before creating a user.")
            return

        hashed_password = get_password_hash("adminpass") # Use a strong password in production!
        
        default_user = User(
            username="admin",
            email="admin@example.com",
            hashed_password=hashed_password,
            perfil=UserProfileEnum.ADMIN,
            clinica_id=first_clinica.id
        )
        db.add(default_user)
        db.commit()
        db.refresh(default_user)
        print(f"Default admin user 'admin' created successfully and associated with clinic: {first_clinica.nome}")
    except Exception as e:
        db.rollback()
        print(f"Error creating default user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_default_user()
