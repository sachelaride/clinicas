"""Módulo que define managers personalizados para os modelos da aplicação de clínica."""

from django.db import models

class ClinicaFilteredManager(models.Manager):
    """Manager personalizado que permite filtrar objetos por clínica associada ao usuário logado.

    Este manager é útil para garantir que os usuários vejam apenas os dados
    pertencentes à sua clínica, ou a uma clínica específica.
    """
    
    def for_clinica(self, clinica):
        """Retorna um queryset filtrado pelos objetos associados à clínica especificada.

        Args:
            clinica (Clinica): A instância da clínica pela qual filtrar.

        Returns:
            QuerySet: Um queryset contendo os objetos filtrados.
        """
        return self.filter(clinica=clinica)
    
    def for_user_clinica(self, user):
        """Retorna um queryset filtrado pelos objetos associados à clínica do usuário.

        Se o usuário não estiver associado a uma clínica, retorna um queryset vazio.

        Args:
            user (User): A instância do usuário logado.

        Returns:
            QuerySet: Um queryset contendo os objetos filtrados pela clínica do usuário.
        """
        if user.clinica:
            return self.filter(clinica=user.clinica)
        return self.none()

class PacienteManager(ClinicaFilteredManager):
    """Manager específico para o modelo Paciente.

    Herda as funcionalidades de filtragem por clínica do ClinicaFilteredManager.
    """
    pass

class AgendamentoManager(ClinicaFilteredManager):
    """Manager específico para o modelo Agendamento.

    Herda as funcionalidades de filtragem por clínica e adiciona métodos
    para filtrar agendamentos por professor e aluno.
    """
    
    def for_professor(self, professor):
        """Retorna os agendamentos associados a um professor específico e à sua clínica.

        Args:
            professor (User): A instância do usuário professor.

        Returns:
            QuerySet: Um queryset contendo os agendamentos do professor.
        """
        return self.filter(medico=professor, clinica=professor.clinica)
    
    def for_aluno(self, aluno):
        """Retorna os agendamentos associados a um aluno específico e à sua clínica.

        Args:
            aluno (User): A instância do usuário aluno.

        Returns:
            QuerySet: Um queryset contendo os agendamentos do aluno.
        """
        return self.filter(aluno=aluno, clinica=aluno.clinica)

class ProntuarioManager(ClinicaFilteredManager):
    """Manager específico para o modelo Prontuario.

    Herda as funcionalidades de filtragem por clínica e adiciona métodos
    para filtrar prontuários por professor e coordenador.
    """
    
    def for_professor(self, professor):
        """Retorna os prontuários associados a um professor específico e à sua clínica.

        Args:
            professor (User): A instância do usuário professor.

        Returns:
            QuerySet: Um queryset contendo os prontuários do professor.
        """
        return self.filter(professor=professor, clinica=professor.clinica)
    
    def for_coordenador(self, coordenador):
        """Retorna os prontuários associados a um coordenador específico e à sua clínica.

        Args:
            coordenador (User): A instância do usuário coordenador.

        Returns:
            QuerySet: Um queryset contendo os prontuários do coordenador.
        """
        return self.filter(clinica=coordenador.clinica)

