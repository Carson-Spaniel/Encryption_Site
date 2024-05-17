import os
import subprocess
import multiprocessing
from multiprocessing import freeze_support
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Encryption_Site.settings')
application = get_wsgi_application()

ELECTRON_APP_PATH = os.path.join(os.path.dirname(__file__), 'ElectronApp')

def start_electron():
    try:
        print('Opening Secure Browser Window')
        # print(f'Electron App Path: {ELECTRON_APP_PATH}')
        # Replace 'electron' with the path to your Electron executable
        electron_path = os.path.join(ELECTRON_APP_PATH, 'node_modules', 'electron', 'dist', 'electron.exe')

        # print(f'Electron Path: {electron_path}')
        electron_process = subprocess.Popen([electron_path, ELECTRON_APP_PATH])
        electron_process.wait()  # Wait for Electron process to finish
        print('Electron process has ended.')
    except Exception as exc:
        raise Exception(f'An error occurred: {exc}') from exc

def start_django_server():
    try:
        print('Starting Django Server')
        call_command('runserver', '127.0.0.1:8000', '--noreload')
    except Exception as exc:
        raise Exception(f'An error occurred: {exc}') from exc

def main():
    freeze_support()
        
    django_process = multiprocessing.Process(target=start_django_server)
    electron_process = multiprocessing.Process(target=start_electron)

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
