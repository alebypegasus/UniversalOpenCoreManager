@echo off
REM Script de setup do projeto UOCM para Windows

echo === UOCM - Universal OpenCore Manager ===
echo Configurando ambiente de desenvolvimento...
echo.

REM Verificar Python 3.11+
python --version >nul 2>&1
if errorlevel 1 (
    echo Erro: Python nao encontrado. Instale Python 3.11+ primeiro.
    exit /b 1
)

python -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)" 2>nul
if errorlevel 1 (
    echo Erro: Python 3.11+ e necessario. Versao atual nao suportada.
    exit /b 1
)

echo Python encontrado.

REM Criar ambiente virtual
if not exist "venv" (
    echo Criando ambiente virtual...
    python -m venv venv
)

REM Ativar ambiente virtual
echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Atualizar pip
echo Atualizando pip...
python -m pip install --upgrade pip setuptools wheel

REM Instalar dependencias
echo Instalando dependencias...
pip install -r requirements.txt

REM Instalar dependencias de desenvolvimento
if "%1"=="--dev" (
    echo Instalando dependencias de desenvolvimento...
    pip install -e ".[dev]"
)

REM Inicializar banco de dados
echo Inicializando banco de dados...
python -c "from uocm.db.database import get_database; get_database().init_db()"

echo.
echo === Setup concluido! ===
echo Para ativar o ambiente virtual, execute:
echo   venv\Scripts\activate.bat
echo.
echo Para executar a aplicacao:
echo   python -m uocm.main

pause

