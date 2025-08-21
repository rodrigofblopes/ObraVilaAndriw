# 🚀 **DEPLOY RÁPIDO - VILA ANDRIW STREAMLIT**

## ⚡ **OPÇÃO 1: Script Automático (Recomendado)**

### **🪟 Windows Batch**
```cmd
deploy_github.bat
```

### **💙 Windows PowerShell**
```powershell
.\deploy_github.ps1
```

---

## ⚡ **OPÇÃO 2: Manual (3 Comandos)**

### **1️⃣ Criar repositório no GitHub**
🌐 https://github.com/new
- **Nome**: `vila-andriw-streamlit`
- **✅ Public**
- **❌ Não** adicione arquivos

### **2️⃣ Conectar e enviar**
```bash
git remote add origin https://github.com/SEU-USUARIO/vila-andriw-streamlit.git
git branch -M main
git push -u origin main
```

### **3️⃣ Deploy Streamlit**
🌐 https://share.streamlit.io
- **Sign in** com GitHub
- **New app** → Selecionar repositório
- **Main file**: `app.py`
- **Deploy!**

---

## 🧹 **Problema com Porta Ocupada?**

```cmd
limpar_streamlit.bat
```

---

## 📱 **Resultado Final**

Sua aplicação ficará online em:
```
https://SEU-USUARIO-vila-andriw-streamlit-app-XXXXX.streamlit.app/
```

---

## 🏆 **Funcionalidades do Dashboard**

### 📊 **5 Abas Completas**
- 🏠 **Visão Geral**: Resumo executivo R$ 126.544,18
- 🏢 **Por Pavimento**: Fundação, Térreo, Superior
- 🔧 **Por Elemento**: Vigas, Pilares, Lajes, Fundações
- 💰 **Análise Detalhada**: 19 serviços completos
- 🎮 **Visualização 3D**: Modelo IFC real + esquemático

### 🛠️ **Tecnologias**
- **Streamlit**: Interface web
- **Plotly**: Gráficos interativos
- **ifcopenshell**: Modelo 3D real
- **Pandas**: Análise de dados

---

**🚀 Tempo total de deploy: ~5 minutos**