import os
import subprocess
import multiprocessing
from multiprocessing import freeze_support
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application
import platform
import random
import socket

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Encryption_Site.settings')
application = get_wsgi_application()

ELECTRON_APP_PATH = os.path.join(os.path.dirname(__file__), 'ElectronApp')

def find_available_port():
    while True:
        port = random.randint(1000, 9999)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', port)) != 0:
                return port

def start_electron(port):
    try:
        print('Opening Secure Browser Window')
        os_name = platform.system()
        if os_name == 'Windows':
            electron_path = os.path.join(ELECTRON_APP_PATH, 'node_modules', 'electron', 'dist', 'electron.exe')
        else:
            electron_path = os.path.join(ELECTRON_APP_PATH, 'node_modules', '.bin', 'electron')

        electron_process = subprocess.Popen([electron_path, ELECTRON_APP_PATH, str(port)])
        electron_process.wait()  # Wait for Electron process to finish
        print('Electron process has ended.')
    except Exception as exc:
        raise Exception(f'An error occurred: {exc}') from exc

def start_django_server(port):
    try:
        print('Starting Django Server')
        # Redirect stdout and stderr to ensure they are available
        import sys
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')

        call_command('makemigrations')
        call_command('migrate')
        call_command('runserver', f'127.0.0.1:{port}', '--noreload')
    except Exception as exc:
        raise Exception(f'An error occurred: {exc}') from exc

def main():
    freeze_support()

    port = find_available_port()
        
    django_process = multiprocessing.Process(target=start_django_server, args=[port])
    electron_process = multiprocessing.Process(target=start_electron, args=[port])

    django_process.start()
    electron_process.start()

    # Wait for Electron process to finish
    electron_process.join()
    
    # Cleanup Django
    if django_process.is_alive():
        django_process.terminate()
        django_process.join()

if __name__ == '__main__':
    main()
