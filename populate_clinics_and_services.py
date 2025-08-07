from sqlalchemy.orm import Session
from app.core.database import engine, get_db
from app.models import Clinica, TipoTratamento

def populate_clinics_and_services():
    db: Session = next(get_db())
    try:
        clinic_data = [
            {
                "name": "Clínica Odontológica",
                "address": "Rua dos Dentistas, 100",
                "phone": "11987654321",
                "num_guiches": 5,
                "min_time": 30,
                "services": [
                    "Ortodontia (aparelhos)",
                    "Implantodontia (implantes)",
                    "Odontopediatria",
                    "Endodontia (canal)",
                    "Periodontia (gengiva)",
                    "Cirurgia oral",
                    "Prótese dentária",
                    "Estética dental (clareamento, lentes de contato)",
                    "Odontologia digital (scanner intraoral, planejamento 3D)"
                ]
            },
            {
                "name": "Clínica Oftalmológica",
                "address": "Avenida da Visão, 200",
                "phone": "11987654322",
                "num_guiches": 3,
                "min_time": 45,
                "services": [
                    "Exame de vista completo (refração)",
                    "Mapeamento de retina",
                    "Cirurgia de catarata e miopia",
                    "Tratamento de glaucoma",
                    "Adaptação de lentes de contato",
                    "Cirurgia refrativa a laser",
                    "Teste do olhinho (pediátrico)"
                ]
            },
            {
                "name": "Clínica de Fisioterapia",
                "address": "Rua da Reabilitação, 300",
                "phone": "11987654323",
                "num_guiches": 4,
                "min_time": 60,
                "services": [
                    "Reabilitação ortopédica, neurológica e respiratória",
                    "Fisioterapia esportiva",
                    "RPG (Reeducação Postural Global)",
                    "Pilates terapêutico",
                    "Eletroterapia",
                    "Terapias manuais e de liberação miofascial",
                    "Reabilitação pós-operatória"
                ]
            },
            {
                "name": "Clínica de Psicologia e Psicoterapia",
                "address": "Travessa da Mente, 400",
                "phone": "11987654324",
                "num_guiches": 2,
                "min_time": 50,
                "services": [
                    "Psicoterapia individual, infantil, casal ou familiar",
                    "Avaliação psicológica e laudos",
                    "Terapia cognitivo-comportamental (TCC)",
                    "Terapia sistêmica",
                    "Psicopedagogia clínica",
                    "Acompanhamento emocional para luto, ansiedade, depressão",
                    "Orientação vocacional"
                ]
            },
            {
                "name": "Clínica Psiquiátrica",
                "address": "Alameda do Equilíbrio, 500",
                "phone": "11987654325",
                "num_guiches": 2,
                "min_time": 60,
                "services": [
                    "Consulta psiquiátrica",
                    "Prescrição e monitoramento de psicofármacos",
                    "Internação voluntária ou involuntária",
                    "Tratamento para dependência química",
                    "Tratamento para transtornos como bipolaridade, esquizofrenia, TOC, etc."
                ]
            },
            {
                "name": "Clínica de Estética e Dermatologia Estética",
                "address": "Rua da Beleza, 600",
                "phone": "11987654326",
                "num_guiches": 3,
                "min_time": 60,
                "services": [
                    "Limpeza de pele profunda",
                    "Peeling químico e mecânico",
                    "Microagulhamento",
                    "Preenchimentos com ácido hialurônico",
                    "Botox (toxina botulínica)",
                    "Depilação a laser",
                    "Procedimentos corporais (radiofrequência, criolipólise, drenagem linfática)",
                    "Tratamentos capilares (queda, crescimento, laser)"
                ]
            },
            {
                "name": "Clínica de Nutrição e Nutrologia",
                "address": "Avenida da Alimentação, 700",
                "phone": "11987654327",
                "num_guiches": 2,
                "min_time": 45,
                "services": [
                    "Avaliação nutricional com bioimpedância",
                    "Planejamento alimentar personalizado",
                    "Dietas para emagrecimento, hipertrofia, doenças crônicas",
                    "Suplementação nutricional",
                    "Nutrição esportiva",
                    "Nutrição funcional",
                    "Atendimento para transtornos alimentares"
                ]
            },
            {
                "name": "Clínica de Fonoaudiologia",
                "address": "Rua da Voz, 800",
                "phone": "11987654328",
                "num_guiches": 2,
                "min_time": 40,
                "services": [
                    "Avaliação e terapia da fala, linguagem e voz",
                    "Distúrbios de aprendizagem",
                    "Terapia para dislexia, gagueira, apraxia",
                    "Reabilitação auditiva",
                    "Adaptação de aparelhos auditivos",
                    "Intervenção em autismo e TEA"
                ]
            },
            {
                "name": "Clínica de Reprodução Humana",
                "address": "Alameda da Vida, 900",
                "phone": "11987654329",
                "num_guiches": 3,
                "min_time": 60,
                "services": [
                    "Fertilização in vitro (FIV)",
                    "Inseminação artificial",
                    "Congelamento de óvulos, sêmen e embriões",
                    "Doação de gametas",
                    "Diagnóstico genético pré-implantacional",
                    "Tratamento de infertilidade feminina e masculina"
                ]
            },
            {
                "name": "Clínica de Diagnóstico por Imagem",
                "address": "Rua do Raio-X, 1000",
                "phone": "11987654330",
                "num_guiches": 4,
                "min_time": 20,
                "services": [
                    "Ultrassonografia (geral, obstétrica, doppler)",
                    "Ressonância magnética",
                    "Tomografia computadorizada",
                    "Mamografia",
                    "Densitometria óssea",
                    "Raio-X digital",
                    "Biópsias guiadas por imagem"
                ]
            },
            {
                "name": "Clínica de Análises Clínicas",
                "address": "Avenida do Laboratório, 1100",
                "phone": "11987654331",
                "num_guiches": 3,
                "min_time": 15,
                "services": [
                    "Coleta de sangue e outros fluidos",
                    "Hemograma completo, exames hormonais, glicemia, colesterol etc.",
                    "Exames toxicológicos e de DNA",
                    "Testes para ISTs e doenças infecciosas",
                    "Painéis genéticos e exames de intolerância alimentar"
                ]
            },
            {
                "name": "Clínica de Alergia e Imunologia",
                "address": "Rua da Imunidade, 1200",
                "phone": "11987654332",
                "num_guiches": 2,
                "min_time": 30,
                "services": [
                    "Testes alérgicos (cutâneo, IgE)",
                    "Tratamento de rinite, asma, urticária, dermatite",
                    "Vacinas para alergia (imunoterapia)",
                    "Avaliação imunológica",
                    "Acompanhamento de imunodeficiências"
                ]
            },
            {
                "name": "Clínica de Geriatria e Cuidados Paliativos",
                "address": "Travessa da Longevidade, 1300",
                "phone": "11987654333",
                "num_guiches": 2,
                "min_time": 60,
                "services": [
                    "Avaliação multidisciplinar do idoso",
                    "Controle de doenças crônicas",
                    "Cuidados paliativos e dor crônica",
                    "Reabilitação geriátrica",
                    "Atendimento domiciliar"
                ]
            },
            {
                "name": "Clínica de Reabilitação Química (Dependência)",
                "address": "Alameda da Recuperação, 1400",
                "phone": "11987654334",
                "num_guiches": 1,
                "min_time": 90,
                "services": [
                    "Desintoxicação supervisionada",
                    "Terapia comportamental e em grupo",
                    "Internação e acompanhamento 24h",
                    "Apoio psicossocial",
                    "Reintegração familiar"
                ]
            },
            {
                "name": "Clínica de Medicina do Trabalho",
                "address": "Rua da Ocupação, 1500",
                "phone": "11987654335",
                "num_guiches": 3,
                "min_time": 20,
                "services": [
                    "Exames admissionais, periódicos, demissionais",
                    "Laudos de saúde ocupacional (ASO)",
                    "Programas de controle médico e saúde ocupacional (PCMSO)",
                    "Perícias e atestados",
                    "Consultas para retorno ao trabalho e aptidão"
                ]
            },
            {
                "name": "Clínica de Medicina Esportiva",
                "address": "Avenida do Atleta, 1600",
                "phone": "11987654336",
                "num_guiches": 2,
                "min_time": 45,
                "services": [
                    "Avaliação física e funcional",
                    "Prescrição de treinos personalizados",
                    "Prevenção e tratamento de lesões esportivas",
                    "Nutrição esportiva",
                    "Reabilitação ortopédica e performance"
                ]
            },
            {
                "name": "Clínica de Podologia",
                "address": "Rua dos Pés, 1700",
                "phone": "11987654337",
                "num_guiches": 1,
                "min_time": 30,
                "services": [
                    "Tratamento de unhas encravadas",
                    "Calosidades e rachaduras",
                    "Podologia geriátrica e diabética",
                    "Avaliação postural e da pisada"
                ]
            },
            {
                "name": "Clínica de Dor (Algologia)",
                "address": "Praça do Alívio, 1800",
                "phone": "11987654338",
                "num_guiches": 2,
                "min_time": 60,
                "services": [
                    "Diagnóstico e tratamento de dor crônica",
                    "Bloqueios anestésicos",
                    "Tratamentos com medicamentos ou intervenções minimamente invasivas",
                    "Cuidados multidisciplinares para fibromialgia, enxaqueca, dores lombares"
                ]
            }
        ]

        for clinic_data_item in clinic_data:
            # Check if clinic already exists to prevent duplicates
            existing_clinica = db.query(Clinica).filter(Clinica.nome == clinic_data_item["name"]).first()
            if not existing_clinica:
                clinica = Clinica(
                    nome=clinic_data_item["name"],
                    endereco=clinic_data_item["address"],
                    telefone=clinic_data_item["phone"],
                    num_guiches=clinic_data_item["num_guiches"],
                    tempo_minimo_atendimento=clinic_data_item["min_time"]
                )
                db.add(clinica)
                db.commit()
                db.refresh(clinica)
                print(f"Added clinic: {clinica.nome}")

                for service_name in clinic_data_item["services"]:
                    existing_service = db.query(TipoTratamento).filter(
                        TipoTratamento.nome == service_name,
                        TipoTratamento.clinica_id == clinica.id
                    ).first()
                    if not existing_service:
                        service = TipoTratamento(
                            clinica_id=clinica.id,
                            nome=service_name,
                            descricao=f"Serviço de {service_name} oferecido pela {clinica.nome}",
                            tempo_minimo_atendimento=clinic_data_item["min_time"]
                        )
                        db.add(service)
                        print(f"  Added service: {service.nome} for {clinica.nome}")
                    else:
                        print(f"  Service already exists: {service_name} for {clinica.nome}")
                db.commit()
            else:
                print(f"Clinic already exists: {clinic_data_item['name']}")
                # If clinic exists, still check and add services that might be missing
                for service_name in clinic_data_item["services"]:
                    existing_service = db.query(TipoTratamento).filter(
                        TipoTratamento.nome == service_name,
                        TipoTratamento.clinica_id == existing_clinica.id
                    ).first()
                    if not existing_service:
                        service = TipoTratamento(
                            clinica_id=existing_clinica.id,
                            nome=service_name,
                            descricao=f"Serviço de {service_name} oferecido pela {existing_clinica.nome}",
                            tempo_minimo_atendimento=clinic_data_item["min_time"]
                        )
                        db.add(service)
                        print(f"  Added missing service: {service.nome} for {existing_clinica.nome}")
                    # else:
                        # print(f"  Service already exists: {service_name} for {existing_clinica.nome}")
                db.commit()

        print("Clinics and services populated successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error populating clinics and services: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    populate_clinics_and_services()
