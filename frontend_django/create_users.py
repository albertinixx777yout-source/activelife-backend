import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_data_server.settings')
django.setup()

from django.contrib.auth.models import User

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
if not User.objects.filter(username='usuario01').exists():
    User.objects.create_user('usuario01', 'u1@example.com', 'usuario123')
if not User.objects.filter(username='usuario02').exists():
    User.objects.create_user('usuario02', 'u2@example.com', 'usuario123')
print("Usuarios creados con éxito.")
