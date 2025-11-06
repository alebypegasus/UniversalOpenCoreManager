@echo off
REM Script de build para Windows (.exe)

echo === UOCM - Build para Windows ===

REM Verificar se estamos no Windows
if not "%OS%"=="Windows_NT" (
    echo Erro: Este script so funciona no Windows
    exit /b 1
)

REM Ativar ambiente virtual se existir
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM Instalar PyInstaller se não estiver instalado
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo Instalando PyInstaller...
    pip install PyInstaller
)

REM Criar diretórios
if not exist "build" mkdir build
if not exist "dist" mkdir dist

REM Verificar se ícone existe
set ICON_FLAG=
if exist "assets\icon.ico" (
    set ICON_FLAG=--icon=assets/icon.ico
    echo Ícone encontrado: assets\icon.ico
) else (
    echo Aviso: assets\icon.ico não encontrado.
    echo O app será criado sem ícone personalizado.
    echo Para criar o ícone, coloque assets\icon.png e converta para .ico
)

REM Criar spec file se não existir
if not exist "uocm.spec" (
    echo Criando uocm.spec...
    python -m PyInstaller --name=UOCM ^
        --onefile ^
        --windowed ^
        --add-data "translations;translations" ^
        --add-data "templates;templates" ^
        --add-data "plugins;plugins" ^
        --hidden-import=PyQt6 ^
        --hidden-import=sqlalchemy ^
        %ICON_FLAG% ^
        uocm/main.py
) else (
    echo Construindo aplicacao...
    python -m PyInstaller uocm.spec
)

echo.
echo === Build concluido! ===
echo Aplicacao .exe esta em: dist\UOCM.exe
echo.
echo Para testar:
echo   dist\UOCM.exe

pause

