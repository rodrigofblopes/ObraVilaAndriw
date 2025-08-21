# Deploy Automático - Vila Andriw Streamlit
# PowerShell Script

Write-Host ""
Write-Host "████████████████████████████████████████████████████" -ForegroundColor Cyan
Write-Host "████  🚀 DEPLOY AUTOMÁTICO - VILA ANDRIW STREAMLIT ████" -ForegroundColor Cyan
Write-Host "████████████████████████████████████████████████████" -ForegroundColor Cyan
Write-Host ""

Write-Host "📋 PASSO 1: Criar repositório no GitHub" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────" -ForegroundColor Gray
Write-Host "🌐 Acesse: https://github.com/new" -ForegroundColor White
Write-Host ""
Write-Host "📝 Configurações do repositório:" -ForegroundColor White
Write-Host "   • Nome: vila-andriw-streamlit" -ForegroundColor Green
Write-Host "   • Descrição: Dashboard Vila Andriw - Versão Streamlit Python" -ForegroundColor Green
Write-Host "   • ✅ Public (para Streamlit Cloud gratuito)" -ForegroundColor Green
Write-Host "   • ❌ NÃO adicione README, .gitignore ou license" -ForegroundColor Red
Write-Host ""

# Abrir GitHub
Start-Process "https://github.com/new"

Write-Host "⏳ Aguardando você criar o repositório..." -ForegroundColor Yellow
Read-Host "Pressione Enter após criar o repositório"

Write-Host ""
Write-Host "📋 PASSO 2: Inserir URL do repositório" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────" -ForegroundColor Gray
Write-Host "💡 Exemplo: https://github.com/rodrigofblopes/vila-andriw-streamlit.git" -ForegroundColor Cyan

$REPO_URL = Read-Host "📥 Cole a URL do seu repositório"

Write-Host ""
Write-Host "🔗 URL inserida: $REPO_URL" -ForegroundColor Green
Write-Host ""

Write-Host "📋 PASSO 3: Conectando e enviando código" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────" -ForegroundColor Gray
Write-Host ""

Write-Host "🔧 Adicionando remote origin..." -ForegroundColor Cyan
try {
    git remote add origin $REPO_URL 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️  Remote já existe, removendo e adicionando novamente..." -ForegroundColor Yellow
        git remote remove origin
        git remote add origin $REPO_URL
    }
} catch {
    Write-Host "❌ Erro ao adicionar remote: $_" -ForegroundColor Red
    Read-Host "Pressione Enter para continuar mesmo assim"
}

Write-Host ""
Write-Host "📤 Enviando código para GitHub..." -ForegroundColor Cyan
git branch -M main
git push -u origin main

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ ERRO no push! Verifique:" -ForegroundColor Red
    Write-Host "   • URL do repositório está correta?" -ForegroundColor Red
    Write-Host "   • Você tem acesso ao repositório?" -ForegroundColor Red
    Write-Host "   • Repositório foi criado como público?" -ForegroundColor Red
    Read-Host "Pressione Enter para continuar"
    exit 1
}

Write-Host ""
Write-Host "✅ CÓDIGO ENVIADO COM SUCESSO!" -ForegroundColor Green
Write-Host ""

Write-Host "📋 PASSO 4: Deploy no Streamlit Cloud" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────" -ForegroundColor Gray
Write-Host ""

Write-Host "🌐 Abrindo Streamlit Cloud..." -ForegroundColor Cyan
Start-Process "https://share.streamlit.io"

Write-Host ""
Write-Host "📝 No Streamlit Cloud:" -ForegroundColor White
Write-Host "   1. ✅ Sign in with GitHub" -ForegroundColor Green
Write-Host "   2. ✅ New app" -ForegroundColor Green
Write-Host "   3. ✅ Repository: seu-usuario/vila-andriw-streamlit" -ForegroundColor Green
Write-Host "   4. ✅ Branch: main" -ForegroundColor Green
Write-Host "   5. ✅ Main file: app.py" -ForegroundColor Green
Write-Host "   6. ✅ Deploy!" -ForegroundColor Green
Write-Host ""

Write-Host "🎊 Sua URL será algo como:" -ForegroundColor Magenta
Write-Host "   https://seu-usuario-vila-andriw-streamlit-app-xxxxx.streamlit.app/" -ForegroundColor Cyan
Write-Host ""

Write-Host "████████████████████████████████████████████████████" -ForegroundColor Cyan
Write-Host "████              🏆 DEPLOY CONCLUÍDO!              ████" -ForegroundColor Cyan
Write-Host "████████████████████████████████████████████████████" -ForegroundColor Cyan
Write-Host ""

Read-Host "Pressione Enter para finalizar"
