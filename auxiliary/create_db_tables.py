from app.core.database import Base, engine
from app.models import Clinica, User, Paciente, Profissional, Convenio, Plano, TipoTratamento, Prontuario, Agendamento, Atendimento, PastaDocumento, DocumentoArquivo, TabelaPrecos, LancamentoFinanceiro, Fatura, Comissao, Lead, CampanhaMarketing, PesquisaSatisfacao, CupomDesconto # Importe explicitamente todos os seus modelos

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")
