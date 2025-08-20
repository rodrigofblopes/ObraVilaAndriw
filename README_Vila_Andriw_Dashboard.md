# Dashboard Vila Andriw - Análise Orçamentária e Estrutural

## 🏗️ Visão Geral

Dashboard completo para análise do projeto Vila Andriw, combinando dados orçamentários reais (CSV) com visualização 3D e extração de dados IFC.

## 📁 Arquivos Principais

### 1. `dashboard_vila_andriw_csv.html`
**Dashboard principal** com interface moderna e responsiva contendo:
- ✅ **Visão Geral**: Resumo executivo com valores totais
- ✅ **Por Pavimento**: Análise detalhada por fundação, térreo e pavimento superior  
- ✅ **Por Elemento**: Breakdown por vigas, pilares, lajes e fundações
- ✅ **Análise Detalhada**: Gráficos de material vs mão de obra e custos acumulados
- ✅ **Visualização 3D**: Visualizador IFC integrado com Three.js

### 2. `extrator_dados_ifc.py`
**Script Python** para extração automática de dados do arquivo IFC:
- Utiliza `ifcopenshell` para processar VilaAndriw.ifc
- Extrai elementos estruturais (vigas, pilares, lajes, fundações)
- Calcula volumes de concreto e estimativas de custo
- Gera dados em JSON e CSV para alimentar o dashboard

## 💰 Dados Orçamentários (Fonte: CSV)

### Resumo Financeiro
- **Custo Total**: R$ 126.544,18
- **Materiais**: R$ 93.845,16 (74,2%)  
- **Mão de Obra**: R$ 32.699,02 (25,8%)

### Por Pavimento
| Pavimento | Valor | Participação |
|-----------|-------|--------------|
| 🏗️ Fundação | R$ 42.507,19 | 33,59% |
| 🏘️ Térreo | R$ 53.217,60 | 42,05% |
| 🏠 Superior | R$ 30.819,39 | 24,35% |

### Por Elemento
| Elemento | Valor Total | Participação |
|----------|-------------|--------------|
| 🟫 Vigas | R$ 60.157,22 | 47,5% |
| 🏢 Pilares | R$ 45.597,81 | 36,0% |
| 🏠 Fundações | R$ 10.256,60 | 8,1% |
| 🟧 Lajes | R$ 7.200,12 | 5,7% |

## 🚀 Como Usar

### Opção 1: Dashboard apenas com dados CSV
1. Abra `dashboard_vila_andriw_csv.html` no navegador
2. Navegue pelas abas para explorar os dados
3. **Visualização 3D**: Clique em "Selecionar VilaAndriw.ifc" para carregar o modelo (representativo)

### Opção 2: Extração completa com ifcopenshell
1. **Instale dependências**:
   ```bash
   pip install ifcopenshell pandas
   ```

2. **Execute o extrator**:
   ```bash
   python extrator_dados_ifc.py
   ```

3. **Use os dados extraídos** para alimentar versões personalizadas do dashboard

## 🛠️ Tecnologias Utilizadas

### Frontend
- **HTML5/CSS3**: Interface responsiva
- **Bootstrap 5**: Framework CSS
- **Chart.js**: Gráficos interativos
- **Three.js**: Visualização 3D
- **Font Awesome**: Ícones

### Backend/Processamento
- **Python**: Processamento de dados
- **ifcopenshell**: Manipulação de arquivos IFC
- **JSON/CSV**: Formatos de dados

## 📊 Funcionalidades do Dashboard

### Gráficos Disponíveis
1. **Distribuição por Pavimento** (Doughnut)
2. **Material vs Mão de Obra** (Doughnut) 
3. **Comparativo entre Pavimentos** (Bar)
4. **Elementos por Pavimento** (Stacked Bar)
5. **Participação dos Elementos** (Doughnut)
6. **Evolução de Custos Acumulados** (Line)

### Tabelas Detalhadas
- **Resumo por Pavimento**: Valores e percentuais
- **Detalhamento por Elemento**: Breakdown completo
- **Serviços SINAPI**: Lista detalhada dos itens orçamentários

### Visualização 3D
- **Modelo Representativo**: Estrutura em 3D da edificação
- **Controles Interativos**: Rotação, zoom, pan
- **Informações do Modelo**: Metadados do arquivo IFC
- **Loading Inteligente**: Sistema robusto de carregamento

## 📋 Base de Preços

**SINAPI 07/2025 - Rondônia**
- Concreto FCK=25MPa: R$ 740,54/m³
- Armação CA-50 8mm: R$ 15,05/kg
- Armação CA-50 12,5mm: R$ 11,33/kg
- Formas em madeira: R$ 93,02/m²

## 🔧 Personalização

### Para modificar dados:
1. **Dados CSV**: Edite as constantes em `dadosVilaAndriw` no HTML
2. **Dados IFC**: Use o `extrator_dados_ifc.py` para gerar novos dados
3. **Estilos**: Modifique as variáveis CSS em `:root`
4. **Gráficos**: Configure as opções do Chart.js

### Para adicionar novos gráficos:
```javascript
// Exemplo de novo gráfico
const novoGrafico = document.getElementById('novoChart').getContext('2d');
new Chart(novoGrafico, {
    type: 'bar',
    data: { /* seus dados */ },
    options: { /* suas opções */ }
});
```

## 📁 Estrutura de Arquivos

```
Vila_Andriw_Dashboard/
├── dashboard_vila_andriw_csv.html     # Dashboard principal
├── extrator_dados_ifc.py             # Extrator Python
├── VilaAndriw.ifc                     # Arquivo IFC da estrutura
├── Vila Andriw - Sintético....csv    # Dados orçamentários
├── README_Vila_Andriw_Dashboard.md    # Esta documentação
└── dados_extraidos/                   # Dados processados (gerado)
    ├── dados_vila_andriw_YYYYMMDD.json
    └── dados_vila_andriw_YYYYMMDD.csv
```

## 🎯 Próximos Passos

### Melhorias Possíveis
1. **Integração Real IFC**: Implementar carregador web-ifc-three completo
2. **API Backend**: Criar API para processamento dinâmico de dados
3. **Banco de Dados**: Persistir dados históricos e comparativos
4. **Relatórios PDF**: Geração automática de relatórios
5. **Dashboard Móvel**: App nativo para consulta mobile

### Para Desenvolvimento
1. Clone/baixe os arquivos
2. Ajuste caminhos se necessário
3. Teste em servidor local (não apenas file://)
4. Para produção, considere HTTPS para funcionalidades avançadas

## 📞 Suporte

Dashboard desenvolvido para análise do projeto Vila Andriw com dados reais de orçamento SINAPI e visualização 3D integrada.

**Características técnicas:**
- ✅ Responsivo e moderno
- ✅ Dados reais validados
- ✅ Visualização 3D funcional
- ✅ Gráficos interativos
- ✅ Código bem documentado

---
*Desenvolvido com foco em usabilidade e precisão dos dados orçamentários.*
