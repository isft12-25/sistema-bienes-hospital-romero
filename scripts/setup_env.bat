@echo off
echo Configurando entornos para Sistema de Bienes Hospital Romero...
echo.

:menu
echo Selecciona el entorno:
echo 1) Desarrollo (Back/Front)
echo 2) Testing
echo 3) Producción
echo 4) Salir
echo.
set /p choice="Opción [1-4]: "

if "%choice%"=="1" goto desarrollo
if "%choice%"=="2" goto testing  
if "%choice%"=="3" goto produccion
if "%choice%"=="4" goto salir

echo Opción inválida. Por favor elige 1-4.
echo.
goto menu

:desarrollo
copy .env.development .env >nul
echo Entorno de DESARROLLO configurado.
goto verificar

:testing
copy .env.testing .env >nul  
echo Entorno de TESTING configurado.
goto verificar

:produccion
copy .env.production .env >nul
echo Entorno de PRODUCCIÓN configurado.

:verificar
if exist .env (
    echo Archivo .env creado correctamente.
    echo.
    type .env
) else (
    echo Error: No se pudo crear el archivo .env
)
echo.

:salir
echo Configuración completada.
pause