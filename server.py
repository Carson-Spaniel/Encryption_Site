import os
import subprocess
import multiprocessing
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Encryption_Site.settings')
application = get_wsgi_application()

LOCK_FILE = 'server.lock'
ELECTRON_APP_PATH = os.path.join(os.path.dirname(__file__), 'ElectronApp')

def start_electron():
    try:
        print('Opening Secure Browser Window')
        print(f'Electron Path: {ELECTRON_APP_PATH}')
        npm_path = 'npm.cmd'  # Using npm.cmd for Windows
        electron_process = subprocess.Popen([npm_path, 'start'], cwd=ELECTRON_APP_PATH)
        electron_process.wait()  # Wait for Electron process to finish
        # If you reach here, it means the Electron process has finished
        print('Electron process has ended.')
    except Exception as exc:
        raise Exception(
            f'An error occurred: {exc}'
        ) from exc

def start_django_server():
    try:
        with open(LOCK_FILE, 'w') as lock:
            lock.write('This file is used to ensure the server runs only once.')

        print('Starting Django Server')
        # Disable autoreload when running the Django server from PyInstaller
        call_command('runserver', '127.0.0.1:8000', '--noreload')
    except Exception as exc:
        raise Exception(
            f'An error occurred: {exc}'
        ) from exc
    finally:
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)

def main():
    if os.path.exists(LOCK_FILE):
        print('Server is already running.')
    else:
        # Use multiprocessing to run Electron and Django in parallel
        django_process = multiprocessing.Process(target=start_django_server)
        electron_process = multiprocessing.Process(target=start_electron)

        django_process.start()
        electron_process.start()

        electron_process.join()  # Wait for Electron process to finish
        
        # Cleanup Django and remove lock file
        if django_process.is_alive():
            django_process.terminate()
            django_process.join()
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)

if __name__ == '__main__':
    main()
