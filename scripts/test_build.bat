@echo off
REM Script de teste e build para Windows

echo === UOCM - Teste e Build ===
echo.

REM Verificar Python
python --version
if errorlevel 1 (
    echo Erro: Python nao encontrado
    exit /b 1
)

REM Ativar ambiente virtual se existir
if exist "venv\Scripts\activate.bat" (
    echo Ativando ambiente virtual...
    call venv\Scripts\activate.bat
)

REM Instalar dependencias
echo Instalando dependencias...
pip install -q -r requirements.txt

REM Executar testes
echo.
echo === Executando Testes ===
python -m pytest tests/ -v
if errorlevel 1 (
    echo Alguns testes falharam (continuando...)
)

REM Verificar lint
echo.
echo === Verificando Lint ===
python -c "import ruff" 2>nul
if not errorlevel 1 (
    ruff check uocm/
) else (
    echo ruff nao instalado, pulando lint
)

REM Build se solicitado
if "%1"=="--build" (
    echo.
    echo === Build ===
    call scripts\build_windows.bat
)

echo.
echo === Concluido! ===

pause

