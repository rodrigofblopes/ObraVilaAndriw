@echo off
chcp 65001 >nul
echo.
echo ████████████████████████████████████████████████████
echo ████  🚀 DEPLOY AUTOMÁTICO - VILA ANDRIW STREAMLIT ████
echo ████████████████████████████████████████████████████
echo.
echo 📋 PASSO 1: Criar repositório no GitHub
echo ─────────────────────────────────────────────────────
echo 🌐 Acesse: https://github.com/new
echo.
echo 📝 Configurações do repositório:
echo    • Nome: vila-andriw-streamlit
echo    • Descrição: Dashboard Vila Andriw - Versão Streamlit Python
echo    • ✅ Public (para Streamlit Cloud gratuito)
echo    • ❌ NÃO adicione README, .gitignore ou license
echo.
start https://github.com/new
echo.
echo ⏳ Aguardando você criar o repositório...
pause
echo.
echo 📋 PASSO 2: Inserir URL do repositório
echo ─────────────────────────────────────────────────────
echo 💡 Exemplo: https://github.com/rodrigofblopes/vila-andriw-streamlit.git
echo.
set /p REPO_URL=📥 Cole a URL do seu repositório: 
echo.
echo 🔗 URL inserida: %REPO_URL%
echo.
echo 📋 PASSO 3: Conectando e enviando código
echo ─────────────────────────────────────────────────────
echo.
echo 🔧 Adicionando remote origin...
git remote add origin %REPO_URL%
if %errorlevel% neq 0 (
    echo ⚠️  Remote já existe, removendo e adicionando novamente...
    git remote remove origin
    git remote add origin %REPO_URL%
)
echo.
echo 📤 Enviando código para GitHub...
git branch -M main
git push -u origin main
echo.
if %errorlevel% neq 0 (
    echo ❌ ERRO no push! Verifique:
    echo    • URL do repositório está correta?
    echo    • Você tem acesso ao repositório?
    echo    • Repositório foi criado como público?
    pause
    exit /b 1
)
echo.
echo ✅ CÓDIGO ENVIADO COM SUCESSO!
echo.
echo 📋 PASSO 4: Deploy no Streamlit Cloud
echo ─────────────────────────────────────────────────────
echo.
echo 🌐 Abrindo Streamlit Cloud...
start https://share.streamlit.io
echo.
echo 📝 No Streamlit Cloud:
echo    1. ✅ Sign in with GitHub
echo    2. ✅ New app
echo    3. ✅ Repository: seu-usuario/vila-andriw-streamlit
echo    4. ✅ Branch: main
echo    5. ✅ Main file: app.py
echo    6. ✅ Deploy!
echo.
echo 🎊 Sua URL será algo como:
echo    https://seu-usuario-vila-andriw-streamlit-app-xxxxx.streamlit.app/
echo.
echo ████████████████████████████████████████████████████
echo ████              🏆 DEPLOY CONCLUÍDO!              ████
echo ████████████████████████████████████████████████████
echo.
pause
