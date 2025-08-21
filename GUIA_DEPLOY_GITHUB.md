# 🚀 Guia Completo: Deploy Dashboard Vila Andriw no GitHub + Streamlit Cloud

## 📋 **Pré-requisitos**
- Conta no GitHub (gratuita)
- Git instalado no seu computador

---

## 🔧 **Passo 1: Preparar o Projeto**

### ✅ Arquivos já criados e prontos:
```
📁 Streamlit/
├── 📄 app.py                    # Aplicação principal
├── 📄 requirements.txt          # Dependências Python
├── 📄 .streamlit/config.toml    # Configurações Streamlit
├── 📄 Procfile                  # Para Heroku (opcional)
├── 📄 run_app.py               # Script local
├── 📄 VilaAndriw.ifc           # Arquivo IFC do projeto
├── 📄 Vila Andriw - Sintético com Valor da Mão de Obra e Material.csv
└── 📄 README_STREAMLIT_DEPLOY.md
```

---

## 🌐 **Passo 2: Criar Repositório no GitHub**

### 2.1 Acessar GitHub
1. Vá para: https://github.com
2. Faça login ou crie uma conta gratuita

### 2.2 Criar Novo Repositório
1. Clique em **"New"** (botão verde)
2. Configure:
   - **Repository name**: `dashboard-vila-andriw`
   - **Description**: `Dashboard Orçamentário Vila Andriw - Streamlit`
   - **Public** (recomendado para Streamlit Cloud gratuito)
   - ✅ **Add a README file**
   - ✅ **Add .gitignore** → escolha "Python"
3. Clique em **"Create repository"**

---

## 💻 **Passo 3: Configurar Git Local**

### 3.1 Abrir Terminal/PowerShell na pasta do projeto:
```bash
cd C:\Users\USUARIO\Desktop\Streamlit
```

### 3.2 Inicializar Git:
```bash
git init
git config user.name "Seu Nome"
git config user.email "seu.email@exemplo.com"
```

### 3.3 Conectar ao GitHub:
```bash
git remote add origin https://github.com/SEU-USUARIO/dashboard-vila-andriw.git
```
> ⚠️ **Substitua "SEU-USUARIO"** pelo seu nome de usuário do GitHub

---

## 📤 **Passo 4: Enviar Código para GitHub**

### 4.1 Adicionar arquivos:
```bash
git add .
git commit -m "Dashboard Vila Andriw - Primeira versão"
```

### 4.2 Enviar para GitHub:
```bash
git branch -M main
git push -u origin main
```

> 🔐 **Autenticação**: GitHub pode pedir login/token. Use suas credenciais.

---

## 🚀 **Passo 5: Deploy no Streamlit Cloud**

### 5.1 Acessar Streamlit Cloud
1. Vá para: https://share.streamlit.io
2. Clique em **"Sign in with GitHub"**
3. Autorize o acesso ao GitHub

### 5.2 Criar Nova App
1. Clique em **"New app"**
2. Configure:
   - **Repository**: `SEU-USUARIO/dashboard-vila-andriw`
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL**: `dashboard-vila-andriw` (ou personalizado)

### 5.3 Deploy Automático
1. Clique em **"Deploy!"**
2. Aguarde 2-5 minutos
3. Sua URL será: `https://SEU-USUARIO-dashboard-vila-andriw-app-xxxxx.streamlit.app/`

---

## 🎯 **Resultado Final**

### ✅ **Dashboard Online**
Sua aplicação estará disponível 24/7 com:
- **🏠 Visão Geral**: Resumo executivo R$ 126.544,18
- **🏢 Por Pavimento**: Análise detalhada com filtros
- **🔧 Por Elemento**: Breakdown vigas/pilares/lajes
- **💰 Análise Detalhada**: Material vs Mão de Obra + tabela completa
- **🎮 Visualização 3D**: Modelo estrutural interativo

### 🔗 **Links Importantes**
- **Repositório GitHub**: `https://github.com/SEU-USUARIO/dashboard-vila-andriw`
- **App Online**: `https://xxx.streamlit.app/`
- **Admin Panel**: `https://share.streamlit.io/`

---

## 🔄 **Atualizações Futuras**

Para atualizar o dashboard:
```bash
# Fazer alterações no código
git add .
git commit -m "Descrição da mudança"
git push origin main
```

> 🚀 **Deploy automático**: Streamlit Cloud atualiza automaticamente quando você faz push!

---

## 🆘 **Resolução de Problemas**

### Erro de dependências:
- Verifique `requirements.txt`
- Use versões específicas se necessário

### Arquivo IFC muito grande:
- GitHub tem limite de 100MB por arquivo
- Use Git LFS se necessário: `git lfs track "*.ifc"`

### App não carrega:
- Verifique logs no Streamlit Cloud
- Teste localmente: `streamlit run app.py`

---

## 📞 **Suporte**

- **GitHub Docs**: https://docs.github.com/
- **Streamlit Docs**: https://docs.streamlit.io/
- **Streamlit Community**: https://discuss.streamlit.io/

---

**🎊 Parabéns! Seu dashboard estará online e acessível globalmente!** 🚀
