from sqlalchemy.orm import Session
from app.core.database import Base, engine, get_db
from app import models
from app.core.security import get_password_hash

# 1. Create all tables (if they don't exist)
print("Dropping all existing database tables...")
Base.metadata.drop_all(bind=engine)
print("All tables dropped.")

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Tables created.")

def populate_permissions():
    db: Session = next(get_db())
    try:
        # Create Permissions
        permissions_to_create = [
            ("admin_acesso", "Acesso administrativo total ao sistema."),
            ("criar_usuarios", "Permite criar novos usuários."),
            ("ler_usuarios", "Permite visualizar usuários."),
            ("atualizar_usuarios", "Permite atualizar usuários existentes."),
            ("excluir_usuarios", "Permite excluir usuários."),
            ("criar_clinicas", "Permite criar novas clínicas."),
            ("ler_clinicas", "Permite visualizar clínicas."),
            ("atualizar_clinicas", "Permite atualizar clínicas existentes."),
            ("excluir_clinicas", "Permite excluir clínicas."),
            ("criar_pacientes", "Permite criar novos pacientes."),
            ("ler_pacientes", "Permite visualizar pacientes."),
            ("atualizar_pacientes", "Permite atualizar pacientes existentes."),
            ("excluir_pacientes", "Permite excluir pacientes."),
            ("criar_profissionais", "Permite criar novos profissionais."),
            ("ler_profissionais", "Permite visualizar profissionais."),
            ("atualizar_profissionais", "Permite atualizar profissionais existentes."),
            ("excluir_profissionais", "Permite excluir profissionais."),
            ("criar_tipos_tratamento", "Permite criar novos tipos de tratamento."),
            ("ler_tipos_tratamento", "Permite visualizar tipos de tratamento."),
            ("atualizar_tipos_tratamento", "Permite atualizar tipos de tratamento existentes."),
            ("excluir_tipos_tratamento", "Permite excluir tipos de tratamento."),
            ("criar_agendamentos", "Permite criar novos agendamentos."),
            ("ler_agendamentos", "Permite visualizar agendamentos."),
            ("atualizar_agendamentos", "Permite atualizar agendamentos existentes."),
            ("excluir_agendamentos", "Permite excluir agendamentos."),
            ("criar_atendimentos", "Permite criar novos atendimentos."),
            ("ler_atendimentos", "Permite visualizar atendimentos."),
            ("atualizar_atendimentos", "Permite atualizar atendimentos existentes."),
            ("excluir_atendimentos", "Permite excluir atendimentos."),
            ("criar_prontuarios", "Permite criar novos prontuários médicos."),
            ("ler_prontuarios", "Permite visualizar prontuários médicos."),
            ("atualizar_prontuarios", "Permite atualizar prontuários médicos existentes."),
            ("excluir_prontuarios", "Permite excluir prontuários médicos."),
            ("criar_documentos", "Permite criar novos documentos."),
            ("ler_documentos", "Permite visualizar documentos."),
            ("atualizar_documentos", "Permite atualizar documentos existentes."),
            ("excluir_documentos", "Permite excluir documentos."),
            ("criar_pastas_documento", "Permite criar novas pastas de documentos."),
            ("ler_pastas_documento", "Permite visualizar pastas de documentos."),
            ("atualizar_pastas_documento", "Permite atualizar pastas de documentos existentes."),
            ("excluir_pastas_documento", "Permite excluir pastas de documentos."),
            ("criar_lancamentos_financeiros", "Permite criar novos lançamentos financeiros."),
            ("ler_lancamentos_financeiros", "Permite visualizar lançamentos financeiros."),
            ("atualizar_lancamentos_financeiros", "Permite atualizar lançamentos financeiros existentes."),
            ("excluir_lancamentos_financeiros", "Permite excluir lançamentos financeiros."),
            ("criar_leads", "Permite criar novos leads."),
            ("ler_leads", "Permite visualizar leads."),
            ("atualizar_leads", "Permite atualizar leads existentes."),
            ("excluir_leads", "Permite excluir leads."),
            ("criar_campanhas_marketing", "Permite criar novas campanhas de marketing."),
            ("ler_campanhas_marketing", "Permite visualizar campanhas de marketing."),
            ("atualizar_campanhas_marketing", "Permite atualizar campanhas de marketing existentes."),
            ("excluir_campanhas_marketing", "Permite excluir campanhas de marketing."),
            ("criar_pesquisas_satisfacao", "Permite criar novas pesquisas de satisfação."),
            ("ler_pesquisas_satisfacao", "Permite visualizar pesquisas de satisfação."),
            ("atualizar_pesquisas_satisfacao", "Permite atualizar pesquisas de satisfação existentes."),
            ("excluir_pesquisas_satisfacao", "Permite excluir pesquisas de satisfação."),
            ("criar_cupons_desconto", "Permite criar novos cupons de desconto."),
            ("ler_cupons_desconto", "Permite visualizar cupons de desconto."),
            ("atualizar_cupons_desconto", "Permite atualizar cupons de desconto existentes."),
            ("excluir_cupons_desconto", "Permite excluir cupons de desconto."),
            ("criar_comissoes", "Permite criar novas comissões."),
            ("ler_comissoes", "Permite visualizar comissões."),
            ("atualizar_comissoes", "Permite atualizar comissões existentes."),
            ("excluir_comissoes", "Permite excluir comissões."),
            ("criar_faturas", "Permite criar novas faturas."),
            ("ler_faturas", "Permite visualizar faturas."),
            ("atualizar_faturas", "Permite atualizar faturas existentes."),
            ("excluir_faturas", "Permite excluir faturas."),
            ("profissional_acesso", "Acesso específico para usuários profissionais."),
            ("paciente_acesso", "Acesso específico para usuários pacientes."),
            ("atendente_acesso", "Acesso específico para usuários atendentes."),
            ("coordenador_acesso", "Acesso específico para usuários coordenadores."),
        ]

        existing_permissions = {p.nome for p in db.query(models.Permissao).all()}
        for name, desc in permissions_to_create:
            if name not in existing_permissions:
                db_permissao = models.Permissao(nome=name, descricao=desc)
                db.add(db_permissao)
                print(f"Permission '{name}' created.")
        db.commit()

        # Fetch all permissions to assign
        all_permissions = {p.nome: p for p in db.query(models.Permissao).all()}

        # Create Profiles and assign Permissions
        profiles_data = {
            "ADMIN": [p.nome for p in all_permissions.values()], # Admin gets all permissions
            "ATENDENTE": [
                "atendente_acesso",
                "criar_agendamentos", "ler_agendamentos", "atualizar_agendamentos",
                "criar_pacientes", "ler_pacientes", "atualizar_pacientes",
                "criar_atendimentos", "ler_atendimentos", "atualizar_atendimentos",
            ],
            "PROFISSIONAL": [
                "profissional_acesso",
                "ler_agendamentos", "atualizar_agendamentos",
                "ler_atendimentos", "atualizar_atendimentos",
                "criar_prontuarios", "ler_prontuarios", "atualizar_prontuarios",
            ],
            "COORDENADOR": [
                "coordenador_acesso",
                "criar_usuarios", "ler_usuarios", "atualizar_usuarios", "excluir_usuarios",
                "criar_clinicas", "ler_clinicas", "atualizar_clinicas", "excluir_clinicas",
                "criar_pacientes", "ler_pacientes", "atualizar_pacientes", "excluir_pacientes",
                "criar_profissionais", "ler_profissionais", "atualizar_profissionais", "excluir_profissionais",
                "criar_tipos_tratamento", "ler_tipos_tratamento", "atualizar_tipos_tratamento", "excluir_tipos_tratamento",
                "criar_agendamentos", "ler_agendamentos", "atualizar_agendamentos", "excluir_agendamentos",
                "criar_atendimentos", "ler_atendimentos", "atualizar_atendimentos", "excluir_atendimentos",
                "criar_prontuarios", "ler_prontuarios", "atualizar_prontuarios", "excluir_prontuarios",
                "criar_documentos", "ler_documentos", "atualizar_documentos", "excluir_documentos",
                "criar_pastas_documento", "ler_pastas_documento", "atualizar_pastas_documento", "excluir_pastas_documento",
                "criar_lancamentos_financeiros", "ler_lancamentos_financeiros", "atualizar_lancamentos_financeiros", "excluir_lancamentos_financeiros",
                "criar_leads", "ler_leads", "atualizar_leads", "excluir_leads",
                "criar_campanhas_marketing", "ler_campanhas_marketing", "atualizar_campanhas_marketing", "excluir_campanhas_marketing",
                "criar_pesquisas_satisfacao", "ler_pesquisas_satisfacao", "atualizar_pesquisas_satisfacao", "excluir_pesquisas_satisfacao",
                "criar_cupons_desconto", "ler_cupons_desconto", "atualizar_cupons_desconto", "excluir_cupons_desconto",
                "criar_comissoes", "ler_comissoes", "atualizar_comissoes", "excluir_comissoes",
                "criar_faturas", "ler_faturas", "atualizar_faturas", "excluir_faturas",
            ],
            "PACIENTE": ["paciente_acesso", "ler_agendamentos", "ler_prontuarios", "ler_documentos", "ler_lancamentos_financeiros", "ler_pesquisas_satisfacao"],
        }

        for profile_name, perms_list in profiles_data.items():
            db_perfil = db.query(models.Perfil).filter(models.Perfil.nome == profile_name).first()
            if not db_perfil:
                db_perfil = models.Perfil(nome=profile_name)
                db.add(db_perfil)
                db.commit()
                db.refresh(db_perfil)
                print(f"Profile '{profile_name}' created.")
            
            # Assign permissions to profile
            current_perms_names = {p.nome for p in db_perfil.permissoes}
            for perm_name in perms_list:
                if perm_name in all_permissions and perm_name not in current_perms_names:
                    db_perfil.permissoes.append(all_permissions[perm_name])
                    print(f"Permission '{perm_name}' assigned to profile '{profile_name}'.")
            db.commit()
            db.refresh(db_perfil)

        # Ensure a default admin user exists and is linked to the ADMIN profile
        admin_profile = db.query(models.Perfil).filter(models.Perfil.nome == "ADMIN").first()
        if admin_profile:
            admin_user = db.query(models.User).filter(models.User.username == "admin").first()
            if not admin_user:
                hashed_password = get_password_hash("admin") # Default password for admin
                db_admin = models.User(
                    username="admin",
                    email="admin@example.com",
                    hashed_password=hashed_password,
                    perfil_id=admin_profile.id,
                    is_active=True,
                    is_superuser=True,
                    is_staff=True
                )
                db.add(db_admin)
                db.commit()
                db.refresh(db_admin)
                print("Default admin user created and linked to ADMIN profile.")
            elif admin_user.perfil_id != admin_profile.id:
                admin_user.perfil_id = admin_profile.id
                db.commit()
                db.refresh(admin_user)
                print("Existing admin user linked to ADMIN profile.")
        else:
            print("ADMIN profile not found. Please ensure it's created.")

    except Exception as e:
        db.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    populate_permissions()
