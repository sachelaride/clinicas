from sqlalchemy.orm import Session
from app.core.database import engine, get_db
from app.models import (
    User, Clinica, Paciente, Profissional, Convenio, Plano, TipoTratamento,
    Prontuario, Agendamento, Atendimento, PastaDocumento, DocumentoArquivo,
    TabelaPrecos, LancamentoFinanceiro, Fatura, Comissao, Lead, CampanhaMarketing,
    PesquisaSatisfacao, CupomDesconto, fatura_atendimentos # Import the association table as well
)

# Define a list of all models to clear, in reverse order of dependency
# This helps with foreign key constraints
MODELS_TO_CLEAR = [
    CupomDesconto,
    PesquisaSatisfacao,
    CampanhaMarketing,
    Lead,
    Comissao,
    LancamentoFinanceiro,
    TabelaPrecos,
    DocumentoArquivo,
    PastaDocumento,
    Atendimento,
    Agendamento,
    Prontuario,
    TipoTratamento,
    Plano,
    Convenio,
    Profissional,
    Paciente,
    Clinica,
]

def clear_db_except_admin():
    db: Session = next(get_db())
    try:
        # Find the admin user
        admin_user = db.query(User).filter(User.username == "admin").first()
        admin_clinica_id = None

        if admin_user:
            admin_clinica_id = admin_user.clinica_id
            # Temporarily set admin's clinica_id to NULL to allow clinic deletion
            admin_user.clinica_id = None
            db.add(admin_user)
            db.commit()
            print("Admin user temporarily unlinked from clinic.")

        # Clear association tables first if they are not handled by ORM cascade
        db.execute(fatura_atendimentos.delete())
        print(f"Cleared association table: {fatura_atendimentos.name}")

        for model in MODELS_TO_CLEAR:
            # Skip User model, as it's handled separately
            if model.__tablename__ == "users":
                continue
            
            db.query(model).delete()
            print(f"Cleared table: {model.__tablename__}")
        
        # Now, handle the User table: delete all except admin
        db.query(User).filter(User.username != "admin").delete()
        print("Removed all users except 'admin'.")

        db.commit()
        print("Database cleared successfully (except admin user).")

        # Re-associate admin user with a clinic if it was previously linked
        if admin_user and admin_clinica_id:
            # Try to find the first clinic created by populate_clinics_and_services.py
            first_clinica = db.query(Clinica).first()
            if first_clinica:
                admin_user.clinica_id = first_clinica.id
                db.add(admin_user)
                db.commit()
                print(f"Admin user re-linked to clinic: {first_clinica.nome}")
            else:
                print("No clinics found to re-link admin user.")

    except Exception as e:
        db.rollback()
        print(f"Error clearing database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    clear_db_except_admin()
