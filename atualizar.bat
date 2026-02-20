@echo off
REM ============================================================================
REM Script para subir atualizacoes para GitHub automaticamente
REM ============================================================================

echo.
echo ========================================
echo   ATUALIZADOR AUTOMATICO - GITHUB
echo ========================================
echo.

REM Verificar se esta em um repositorio Git
git status >nul 2>&1
if errorlevel 1 (
    echo ERRO: Esta pasta nao e um repositorio Git!
    echo Execute primeiro: git init
    pause
    exit /b 1
)

echo [1/4] Verificando mudancas...
git status

echo.
echo [2/4] Adicionando arquivos...
git add .

echo.
set /p mensagem="Digite a mensagem do commit: "

if "%mensagem%"=="" (
    echo ERRO: Mensagem nao pode estar vazia!
    pause
    exit /b 1
)

echo.
echo [3/4] Fazendo commit...
git commit -m "%mensagem%"

echo.
echo [4/4] Enviando para GitHub...
git push

echo.
echo ========================================
echo   CONCLUIDO COM SUCESSO!
echo ========================================
echo.
echo Aguarde 1-2 minutos para o Streamlit
echo Cloud aplicar as mudancas.
echo.
pause
