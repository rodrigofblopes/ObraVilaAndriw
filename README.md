# 🏗️ Dashboard Vila Andriw - Streamlit Version

Dashboard completo de análise orçamentária e visualização 3D do projeto estrutural Vila Andriw, desenvolvido em Python com Streamlit.

## 🌐 **Links de Acesso**

### ✅ **Aplicação Online (Streamlit Cloud)**
🚀 **[https://vila-andriw-streamlit.streamlit.app](https://vila-andriw-streamlit.streamlit.app)** *(será disponibilizado após deploy)*

### 🔗 **Versão HTML Original**
📱 **[https://rodrigofblopes.github.io/Obra-Vila/](https://rodrigofblopes.github.io/Obra-Vila/)**

---

## 📊 **Funcionalidades**

### 🏠 **Visão Geral**
- **Resumo Executivo**: R$ 126.544,18 total
- **Distribuição Custos**: Material (74.2%) vs Mão de Obra (25.8%)
- **Métricas Principais**: Por pavimento e elemento
- **Gráficos Interativos**: Plotly para visualizações dinâmicas

### 🏢 **Por Pavimento**
- **Filtros Interativos**: Todos, Fundação, Térreo, Superior
- **Cards Estilizados**: Cada pavimento com gradiente único
- **Análise Detalhada**: Custo total, participação %, elementos principais
- **Gráficos Individuais**: Distribuição por pavimento

### 🔧 **Por Elemento**
- **Breakdown Estrutural**: Vigas, Pilares, Lajes, Fundações
- **Análise Comparativa**: Custos entre elementos
- **Filtros Dinâmicos**: Por tipo de elemento
- **Visualizações**: Gráficos de pizza e barras

### 💰 **Análise Detalhada**
- **Material vs Mão de Obra**: Por pavimento
- **Evolução Custos**: Gráfico acumulativo
- **Resumo Financeiro**: Cards por pavimento
- **Tabela Completa**: 19 serviços detalhados com filtros

### 🎮 **Visualização 3D**
- **🏗️ Modelo IFC Real**: Carregamento do arquivo VilaAndriw.ifc
- **📐 Modelo Esquemático**: Fallback quando IFC não disponível
- **Controles Interativos**: Elementos visíveis, modos de visualização
- **Informações**: Especificações técnicas e dimensões

---

## 🛠️ **Tecnologias Utilizadas**

### **Backend Python**
- **[Streamlit](https://streamlit.io/)**: Framework para aplicações web
- **[Pandas](https://pandas.pydata.org/)**: Manipulação de dados
- **[Plotly](https://plotly.com/python/)**: Gráficos interativos
- **[NumPy](https://numpy.org/)**: Computação numérica

### **Visualização 3D**
- **[ifcopenshell](https://ifcopenshell.org/)**: Processamento de arquivos IFC
- **[Plotly 3D](https://plotly.com/python/3d-charts/)**: Renderização 3D

### **Deploy & Hosting**
- **[Streamlit Cloud](https://streamlit.io/cloud)**: Hospedagem gratuita
- **[GitHub](https://github.com/)**: Controle de versão
- **[GitHub Actions](https://github.com/features/actions)**: CI/CD (futuro)

---

## 🚀 **Como Executar Localmente**

### **Pré-requisitos**
- Python 3.8+
- pip

### **Instalação Rápida**
```bash
# 1. Clonar repositório
git clone https://github.com/rodrigofblopes/vila-andriw-streamlit.git
cd vila-andriw-streamlit

# 2. Executar script automático
python run_app.py
```

### **Instalação Manual**
```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Executar aplicação
streamlit run app.py
```

### **Acesso Local**
📱 **http://localhost:8501**

---

## 📁 **Estrutura do Projeto**

```
vila-andriw-streamlit/
├── 📄 app.py                           # Aplicação principal Streamlit
├── 📄 requirements.txt                 # Dependências Python
├── 📄 run_app.py                      # Script de execução local
├── 📁 .streamlit/
│   └── config.toml                    # Configurações Streamlit
├── 📄 VilaAndriw.ifc                  # Modelo 3D IFC
├── 📄 Vila Andriw - Sintético.csv     # Dados orçamentários
├── 📄 .gitignore                      # Arquivos ignorados
├── 📄 Procfile                        # Deploy Heroku (backup)
└── 📚 docs/
    ├── GUIA_DEPLOY_GITHUB.md          # Guia de deploy
    ├── README_STREAMLIT_DEPLOY.md     # Documentação deploy
    └── DEPLOY_RAPIDO.md               # Deploy express
```

---

## 📊 **Dados do Projeto**

### **💰 Resumo Financeiro**
- **Custo Total**: R$ 126.544,18
- **Material**: R$ 93.845,16 (74.2%)
- **Mão de Obra**: R$ 32.699,02 (25.8%)

### **🏗️ Distribuição por Pavimento**
- **Fundação**: R$ 28.468,18 (22.5%)
- **Térreo**: R$ 67.256,61 (53.1%)
- **Pavimento Superior**: R$ 30.819,39 (24.4%)

### **🔧 Elementos Estruturais**
- **Vigas**: 15 serviços detalhados
- **Pilares**: Concreto armado C25/C30
- **Lajes**: Nervuradas e maciças
- **Fundações**: Sapatas corridas

---

## 🔄 **Deploy & CI/CD**

### **Deploy Automático**
- **Push para `main`** → Deploy automático no Streamlit Cloud
- **GitHub Actions**: Testes automatizados (futuro)
- **Vercel**: Deploy alternativo (backup)

### **Monitoramento**
- **Streamlit Cloud Dashboard**: Analytics de uso
- **GitHub Insights**: Estatísticas do repositório
- **Error Tracking**: Logs de erro automáticos

---

## 📱 **Compatibilidade**

### **Dispositivos**
- ✅ **Desktop**: Windows, macOS, Linux
- ✅ **Tablet**: iPad, Android tablets
- ✅ **Mobile**: iPhone, Android (otimizado)

### **Navegadores**
- ✅ **Chrome** (recomendado)
- ✅ **Firefox**
- ✅ **Safari**
- ✅ **Edge**

---

## 🤝 **Contribuição**

### **Como Contribuir**
1. **Fork** do repositório
2. **Criar branch**: `git checkout -b feature/nova-funcionalidade`
3. **Commit**: `git commit -m 'Adicionar nova funcionalidade'`
4. **Push**: `git push origin feature/nova-funcionalidade`
5. **Pull Request**: Abrir PR para revisão

### **Issues**
- 🐛 **Bug Reports**: Use template de bug
- ✨ **Feature Requests**: Use template de feature
- 📖 **Documentation**: Melhorias na documentação

---

## 📞 **Suporte & Contato**

### **Desenvolvedor**
- **👨‍💻 Nome**: Rodrigo Lopes
- **📧 Email**: engrodrigofblopes@gmail.com
- **🌐 GitHub**: [@rodrigofblopes](https://github.com/rodrigofblopes)
- **💼 LinkedIn**: [Rodrigo Lopes](https://linkedin.com/in/rodrigofblopes)

### **Projeto**
- **🐛 Issues**: [GitHub Issues](https://github.com/rodrigofblopes/vila-andriw-streamlit/issues)
- **📖 Wiki**: [Documentação](https://github.com/rodrigofblopes/vila-andriw-streamlit/wiki)
- **💬 Discussions**: [GitHub Discussions](https://github.com/rodrigofblopes/vila-andriw-streamlit/discussions)

---

## 📄 **Licença**

Este projeto está licenciado sob a **MIT License** - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 🎯 **Roadmap**

### **Versão 1.0** ✅
- [x] Dashboard completo Streamlit
- [x] Visualização 3D IFC
- [x] Deploy Streamlit Cloud
- [x] Documentação completa

### **Versão 1.1** 🚧
- [ ] Testes automatizados
- [ ] Cache otimizado
- [ ] Exportação PDF
- [ ] Múltiplos projetos

### **Versão 2.0** 📅
- [ ] API REST
- [ ] Banco de dados
- [ ] Autenticação usuários
- [ ] Dashboard admin

---

**🚀 Desenvolvido com ❤️ em Python + Streamlit**

---

## 🏆 **Projeto Relacionado**

### **Versão HTML/JavaScript**
🌐 **[Dashboard Original](https://github.com/rodrigofblopes/Obra-Vila)** - Versão web pura com Three.js

### **Comparação de Versões**

| Recurso | HTML Version | Streamlit Version |
|---------|--------------|-------------------|
| **3D Viewer** | ✅ Three.js avançado | ✅ Plotly + ifcopenshell |
| **Backend** | ❌ Frontend only | ✅ Python completo |
| **Análise Dados** | ⚠️ Limitada | ✅ Pandas + NumPy |
| **Deploy** | ✅ GitHub Pages | ✅ Streamlit Cloud |
| **Mobile** | ✅ Responsivo | ✅ Nativo |
| **Manutenção** | ⚠️ JavaScript puro | ✅ Python estruturado |

---

*Última atualização: Janeiro 2025*
