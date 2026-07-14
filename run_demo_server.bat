@echo off
echo Iniciando servidor SIGEA en modo demo...
echo.

REM Configurar variables de entorno para demo
set DEBUG=True
set ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
set DJANGO_SECRET_KEY=demo-secret-key-change-in-production

REM Activar entorno virtual
call venv\Scripts\activate

REM Recolectar archivos estáticos
echo Recolectando archivos estáticos...
python manage.py collectstatic --noinput

REM Ejecutar migraciones
echo Ejecutando migraciones...
python manage.py migrate

REM Iniciar servidor
echo.
echo Servidor iniciado en: http://localhost:8000
echo Para acceso externo: http://0.0.0.0:8000
echo Presiona Ctrl+C para detener el servidor
echo.
python manage.py runserver 0.0.0.0:8000

pause
