# 🚀 Dashboard Vila Andriw - Deploy Streamlit

## 🌐 Aplicação Streamlit

Dashboard interativo desenvolvido com **Streamlit** para análise orçamentária e estrutural do projeto Vila Andriw.

### 📋 Funcionalidades

- ✅ **Visão Geral**: Resumo executivo com métricas principais
- ✅ **Por Pavimento**: Análise detalhada por fundação, térreo e superior
- ✅ **Por Elemento**: Breakdown por vigas, pilares, lajes e fundações
- ✅ **Análise Detalhada**: Gráficos de material vs mão de obra e custos acumulados
- ✅ **Visualização 3D**: Upload de arquivos IFC (VilaAndriw.ifc)

### 💰 Dados Orçamentários (SINAPI 07/2025)

- **Custo Total**: R$ 126.544,18
- **Materiais**: R$ 93.845,16 (74,2%)
- **Mão de Obra**: R$ 32.699,02 (25,8%)

### 🏢 Por Pavimento

| Pavimento | Valor | Participação |
|-----------|-------|--------------|
| 🏗️ Fundação | R$ 42.507,19 | 33,59% |
| 🏘️ Térreo | R$ 53.217,60 | 42,05% |
| 🏠 Superior | R$ 30.819,39 | 24,35% |

## 🚀 Como Fazer Deploy

### Opção 1: Streamlit Cloud (Recomendado)

1. **Prepare o repositório**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Dashboard Vila Andriw"
   ```

2. **Suba para GitHub**:
   ```bash
   git remote add origin https://github.com/seu-usuario/dashboard-vila-andriw
   git push -u origin main
   ```

3. **Deploy no Streamlit Cloud**:
   - Acesse [share.streamlit.io](https://share.streamlit.io)
   - Conecte sua conta GitHub
   - Selecione o repositório: `dashboard-vila-andriw`
   - Arquivo principal: `app.py`
   - Clique em **"Deploy"**

### Opção 2: Heroku

1. **Instale o Heroku CLI**
2. **Crie arquivo Procfile**:
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```
3. **Deploy**:
   ```bash
   heroku create dashboard-vila-andriw
   git push heroku main
   ```

### Opção 3: Local (Desenvolvimento)

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
streamlit run app.py
```

## 📁 Estrutura dos Arquivos

```
dashboard-vila-andriw/
├── app.py                          # Aplicação principal Streamlit
├── requirements.txt                # Dependências Python
├── .streamlit/
│   └── config.toml                 # Configurações do Streamlit
├── README_STREAMLIT_DEPLOY.md      # Este arquivo
└── VilaAndriw.ifc                  # Arquivo IFC (opcional para upload)
```

## 🛠️ Tecnologias Utilizadas

- **Streamlit**: Framework web para Python
- **Plotly**: Gráficos interativos
- **Pandas**: Manipulação de dados
- **NumPy**: Computação numérica

## 🎯 URLs de Exemplo

Após o deploy, sua aplicação estará disponível em:

- **Streamlit Cloud**: `https://seu-usuario-dashboard-vila-andriw-app-xxxxx.streamlit.app/`
- **Heroku**: `https://dashboard-vila-andriw.herokuapp.com/`
- **Local**: `http://localhost:8501/`

## 🔧 Configurações Avançadas

### Variáveis de Ambiente (secrets.toml)

Para dados sensíveis, crie `.streamlit/secrets.toml`:

```toml
# .streamlit/secrets.toml
[database]
url = "sua-url-database"

[api]
key = "sua-api-key"
```

### Customização de Tema

Edite `.streamlit/config.toml` para personalizar cores:

```toml
[theme]
primaryColor = "#1e3a8a"        # Azul principal
backgroundColor = "#ffffff"      # Fundo branco
secondaryBackgroundColor = "#f8fafc"  # Cinza claro
textColor = "#1f2937"           # Texto escuro
```

## 📊 Funcionalidades da Aplicação

### 🏠 Visão Geral
- Métricas principais do projeto
- Gráficos de pizza (pavimentos e material/mão de obra)
- Cards informativos

### 🏢 Por Pavimento
- Filtros interativos por pavimento
- Cards detalhados de cada pavimento
- Gráfico comparativo de custos

### 🔧 Por Elemento
- Análise por vigas, pilares, lajes e fundações
- Gráficos stacked bar e pie
- Tabela detalhada com percentuais

### 💰 Análise Detalhada
- Material vs mão de obra por pavimento
- Evolução de custos acumulados
- Tabela completa de serviços SINAPI

### 🎮 Visualização 3D
- Upload de arquivos IFC
- Simulação de controles 3D
- Informações do modelo carregado

## 🐛 Solução de Problemas

### 1. Erro de Dependências
```bash
pip install --upgrade streamlit plotly pandas numpy
```

### 2. Problemas de Port (Heroku)
Verifique se o `Procfile` está correto:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

### 3. Configurações de CORS
Adicione em `config.toml`:
```toml
[server]
enableCORS = false
enableXsrfProtection = false
```

## 📞 Suporte

Dashboard desenvolvido para o projeto Vila Andriw com dados reais de orçamento SINAPI e interface Streamlit moderna.

**Características técnicas:**
- ✅ Interface responsiva e interativa
- ✅ Dados reais validados do orçamento
- ✅ Gráficos interativos com Plotly
- ✅ Upload de arquivos IFC
- ✅ Deploy simples e rápido

---

### 🎊 Resultado Final

Uma aplicação web completa e interativa que pode ser acessada de qualquer lugar, permitindo análise detalhada dos dados orçamentários do Vila Andriw com interface moderna e profissional!

**Pronto para deploy em produção** 🚀
