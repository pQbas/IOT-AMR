# IOT-AMR
This is a repository used to develop the iot dashboard of an autonomous movile robot.

Preparing the environment in Windows:
- Install
    python -m pip install roslibpy
    python -m pip install waitress
    python -m pip install watchdog


Pasos en GIT:
    1: Actualizar
    2: Codificar, actualizar, subir
    Actualizar:
        git pull
    Subir camabios:
        git add .
        git commit -m 'Fixed funcions name'
        git push -u origin main

Pasos simular servidor WEB:
    1. En app.py modificar:
        - comentar la linea: sys.path.append('/home/pqbas/miniconda3/envs/iot/lib/python3.8/site-packages')
        - poner variables: SIMULATOR = True
        - ejecutar app.py
        - en el navegador, entrar a la direccion http://127.0.0.1:5000/
        git commit -m 'Folder documents with topic_list.txt was addded'
        git push -u origin main



Tareas:
- Crear dos diccionarios, uno para datos de laboratorio, otro para empresa. Buscar que sean similares.

- Cómo devolver una imagen en un servidor con python.
    