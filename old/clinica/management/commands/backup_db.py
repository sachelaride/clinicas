import os
import subprocess
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from datetime import datetime

class Command(BaseCommand):
    help = 'Performs a database backup.'

    def handle(self, *args, **options):
        db_settings = settings.DATABASES['default']
        db_engine = db_settings['ENGINE']

        if 'postgresql' in db_engine:
            self.backup_postgresql(db_settings)
        else:
            raise CommandError(f'Database engine {db_engine} not supported for backup.')

    def backup_postgresql(self, db_settings):
        db_name = db_settings['NAME']
        db_user = db_settings['USER']
        db_host = db_settings.get('HOST', 'localhost')
        db_port = db_settings.get('PORT', '5432')
        db_password = db_settings.get('PASSWORD', '')

        backup_dir = settings.BASE_DIR / 'backups'
        os.makedirs(backup_dir, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = backup_dir / f'{db_name}_backup_{timestamp}.sql'

        env = os.environ.copy()
        if db_password:
            env['PGPASSWORD'] = db_password

        cmd = [
            'pg_dump',
            '-h', db_host,
            '-p', db_port,
            '-U', db_user,
            '-F', 'p', # plain text
            '-b', # include blobs
            '-v', # verbose
            db_name
        ]

        try:
            with open(backup_file, 'w') as f:
                subprocess.run(cmd, env=env, stdout=f, check=True)
            self.stdout.write(self.style.SUCCESS(f'Successfully backed up database to {backup_file}'))
        except FileNotFoundError:
            raise CommandError('pg_dump command not found. Make sure PostgreSQL client tools are installed and in your PATH.')
        except subprocess.CalledProcessError as e:
            raise CommandError(f'Error during pg_dump: {e}')
