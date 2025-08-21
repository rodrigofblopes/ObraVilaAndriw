@echo off
chcp 65001 >nul
echo.
echo ████████████████████████████████████████████████████
echo ████     🧹 LIMPEZA STREAMLIT - VILA ANDRIW        ████
echo ████████████████████████████████████████████████████
echo.
echo 🔍 Verificando processos Streamlit...
echo.

:: Verificar se há processos python rodando streamlit
tasklist | findstr /i "python.exe" >nul
if %errorlevel% equ 0 (
    echo 📋 Processos Python encontrados:
    tasklist | findstr /i "python.exe"
    echo.
    echo ⏹️  Parando todos os processos Streamlit...
    
    :: Tentar parar graciosamente primeiro
    echo 🔧 Tentando parada graciousa...
    taskkill /f /im "python.exe" /fi "WINDOWTITLE eq *streamlit*" 2>nul
    
    :: Forçar parada se necessário
    echo 🔧 Forçando parada de processos Python...
    taskkill /f /im "python.exe" 2>nul
    
    echo ✅ Processos Streamlit finalizados!
    echo.
) else (
    echo ✅ Nenhum processo Streamlit em execução.
    echo.
)

echo 🔍 Verificando portas ocupadas...
echo.

:: Verificar porta 8501
netstat -ano | findstr ":8501" >nul
if %errorlevel% equ 0 (
    echo 📋 Porta 8501 ocupada:
    netstat -ano | findstr ":8501"
    echo.
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8501" ^| findstr "LISTENING"') do (
        echo ⏹️  Liberando porta 8501 (PID: %%a)...
        taskkill /f /pid %%a 2>nul
    )
) else (
    echo ✅ Porta 8501 livre.
)

:: Verificar porta 8502
netstat -ano | findstr ":8502" >nul
if %errorlevel% equ 0 (
    echo 📋 Porta 8502 ocupada:
    netstat -ano | findstr ":8502"
    echo.
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8502" ^| findstr "LISTENING"') do (
        echo ⏹️  Liberando porta 8502 (PID: %%a)...
        taskkill /f /pid %%a 2>nul
    )
) else (
    echo ✅ Porta 8502 livre.
)

echo.
echo 🧹 Limpeza de cache Streamlit...
if exist "%USERPROFILE%\.streamlit" (
    echo 🗂️  Limpando cache em %USERPROFILE%\.streamlit
    rd /s /q "%USERPROFILE%\.streamlit\cache" 2>nul
    echo ✅ Cache limpo!
) else (
    echo ✅ Nenhum cache encontrado.
)

echo.
echo ████████████████████████████████████████████████████
echo ████            🏆 LIMPEZA CONCLUÍDA!              ████
echo ████████████████████████████████████████████████████
echo.
echo 💡 Agora você pode executar:
echo    python run_app.py
echo.
pause
