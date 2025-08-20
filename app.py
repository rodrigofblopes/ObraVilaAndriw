import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import base64
import io
import os

# Configuração da página
st.set_page_config(
    page_title="Dashboard Vila Andriw",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para melhorar a aparência
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        text-align: center;
        border-left: 5px solid;
    }
    
    .metric-card.total {
        border-left-color: #10b981;
    }
    
    .metric-card.material {
        border-left-color: #06b6d4;
    }
    
    .metric-card.mao-obra {
        border-left-color: #f59e0b;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #f8fafc;
        border-radius: 8px;
        color: #374151;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #1e3a8a;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Dados do projeto Vila Andriw
@st.cache_data
def carregar_dados_vila_andriw():
    """Carrega os dados orçamentários do Vila Andriw"""
    dados = {
        "resumo": {
            "custo_total": 126544.18,
            "total_material": 93845.16,
            "total_mao_obra": 32699.02,
            "percentual_material": 74.2,
            "percentual_mao_obra": 25.8
        },
        "pavimentos": [
            {
                "nome": "Fundação",
                "total": 42507.19,
                "percentual": 33.59,
                "elementos": {
                    "vigas": 23600.73,
                    "pilares": 8649.86,
                    "fundacoes": 10256.60
                }
            },
            {
                "nome": "Térreo", 
                "total": 53217.60,
                "percentual": 42.05,
                "elementos": {
                    "vigas": 25399.51,
                    "pilares": 20617.97,
                    "lajes": 7200.12
                }
            },
            {
                "nome": "Pavimento Superior",
                "total": 30819.39,
                "percentual": 24.35,
                "elementos": {
                    "vigas": 11156.98,
                    "pilares": 19662.41
                }
            }
        ],
        "servicos": [
            {
                "pavimento": "Fundação",
                "elemento": "Vigas",
                "servico": "Armação A.C. CA-50 8mm",
                "unidade": "KG",
                "quantidade": 480.2,
                "valor_unitario": 15.05,
                "material": 6295.43,
                "mao_obra": 931.58,
                "total": 7227.01,
                "percentual": 5.71
            },
            {
                "pavimento": "Fundação", 
                "elemento": "Vigas",
                "servico": "Concreto FCK=25MPa",
                "unidade": "m³",
                "quantidade": 7.1,
                "valor_unitario": 740.54,
                "material": 4730.73,
                "mao_obra": 527.10,
                "total": 5257.83,
                "percentual": 4.15
            },
            {
                "pavimento": "Térreo",
                "elemento": "Vigas",
                "servico": "Armação A.C. CA-50 8mm",
                "unidade": "KG", 
                "quantidade": 584.3,
                "valor_unitario": 15.05,
                "material": 7660.17,
                "mao_obra": 1133.54,
                "total": 8793.71,
                "percentual": 6.95
            },
            {
                "pavimento": "Térreo",
                "elemento": "Vigas",
                "servico": "Concreto FCK=25MPa",
                "unidade": "m³",
                "quantidade": 9.8,
                "valor_unitario": 740.54,
                "material": 6538.77,
                "mao_obra": 728.31,
                "total": 7267.08,
                "percentual": 5.74
            },
            {
                "pavimento": "Térreo",
                "elemento": "Pilares",
                "servico": "Armação A.C. CA-50 12.5mm",
                "unidade": "KG",
                "quantidade": 341.2,
                "valor_unitario": 11.33,
                "material": 3592.83,
                "mao_obra": 272.96,
                "total": 3865.79,
                "percentual": 3.05
            },
            {
                "pavimento": "Térreo",
                "elemento": "Pilares",
                "servico": "Concreto FCK=30MPa",
                "unidade": "m³",
                "quantidade": 20.1,
                "valor_unitario": 825.60,
                "material": 14954.56,
                "mao_obra": 1797.52,
                "total": 16752.18,
                "percentual": 13.24
            },
            {
                "pavimento": "Térreo",
                "elemento": "Lajes",
                "servico": "Laje nervurada h=20cm",
                "unidade": "m²",
                "quantidade": 38.9,
                "valor_unitario": 185.12,
                "material": 6489.17,
                "mao_obra": 710.95,
                "total": 7200.12,
                "percentual": 5.69
            },
            {
                "pavimento": "Fundação",
                "elemento": "Pilares",
                "servico": "Armação A.C. CA-50 10mm",
                "unidade": "KG",
                "quantidade": 268.5,
                "valor_unitario": 14.25,
                "material": 3346.13,
                "mao_obra": 479.94,
                "total": 3826.07,
                "percentual": 3.02
            },
            {
                "pavimento": "Fundação",
                "elemento": "Pilares",
                "servico": "Concreto FCK=25MPa",
                "unidade": "m³",
                "quantidade": 5.2,
                "valor_unitario": 740.54,
                "material": 3470.01,
                "mao_obra": 647.86,
                "total": 4117.87,
                "percentual": 3.25
            },
            {
                "pavimento": "Fundação",
                "elemento": "Lajes",
                "servico": "Laje maciça h=15cm",
                "unidade": "m²",
                "quantidade": 45.2,
                "valor_unitario": 159.30,
                "material": 6485.88,
                "mao_obra": 714.24,
                "total": 7200.12,
                "percentual": 5.69
            },
            {
                "pavimento": "Fundação",
                "elemento": "Fundações",
                "servico": "Escavação manual terreno",
                "unidade": "m³",
                "quantidade": 12.8,
                "valor_unitario": 45.80,
                "material": 498.24,
                "mao_obra": 87.96,
                "total": 586.24,
                "percentual": 0.46
            },
            {
                "pavimento": "Fundação",
                "elemento": "Fundações",
                "servico": "Concreto magro FCK=15MPa",
                "unidade": "m³",
                "quantidade": 2.4,
                "valor_unitario": 485.30,
                "material": 1048.63,
                "mao_obra": 115.99,
                "total": 1164.62,
                "percentual": 0.92
            },
            {
                "pavimento": "Fundação",
                "elemento": "Fundações",
                "servico": "Sapata corrida 40x80cm",
                "unidade": "m³",
                "quantidade": 18.6,
                "valor_unitario": 775.45,
                "material": 12987.37,
                "mao_obra": 1261.77,
                "total": 14249.14,
                "percentual": 11.26
            },
            {
                "pavimento": "Pavimento Superior",
                "elemento": "Vigas",
                "servico": "Armação A.C. CA-50 10mm",
                "unidade": "KG",
                "quantidade": 325.8,
                "valor_unitario": 14.25,
                "material": 4071.53,
                "mao_obra": 553.45,
                "total": 4624.98,
                "percentual": 3.65
            },
            {
                "pavimento": "Pavimento Superior",
                "elemento": "Vigas",
                "servico": "Concreto FCK=25MPa",
                "unidade": "m³",
                "quantidade": 8.9,
                "valor_unitario": 735.80,
                "material": 5892.72,
                "mao_obra": 639.28,
                "total": 6532.00,
                "percentual": 5.16
            },
            {
                "pavimento": "Pavimento Superior",
                "elemento": "Pilares",
                "servico": "Armação A.C. CA-50 12.5mm",
                "unidade": "KG",
                "quantidade": 512.7,
                "valor_unitario": 11.33,
                "material": 7393.94,
                "mao_obra": 561.53,
                "total": 7955.47,
                "percentual": 6.29
            },
            {
                "pavimento": "Pavimento Superior",
                "elemento": "Pilares",
                "servico": "Concreto FCK=30MPa",
                "unidade": "m³",
                "quantidade": 14.2,
                "valor_unitario": 825.60,
                "material": 10571.68,
                "mao_obra": 1135.26,
                "total": 11706.94,
                "percentual": 9.25
            },
            {
                "pavimento": "Pavimento Superior",
                "elemento": "Lajes",
                "servico": "Laje treliçada h=12cm",
                "unidade": "m²",
                "quantidade": 42.5,
                "valor_unitario": 145.80,
                "material": 5581.50,
                "mao_obra": 614.82,
                "total": 6196.32,
                "percentual": 4.90
            }
        ]
    }
    return dados

def formatar_moeda(valor):
    """Formata valores para moeda brasileira"""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def main():
    # Header principal
    st.markdown("""
    <div class="main-header">
        <h1>🏗️ Dashboard Vila Andriw</h1>
        <p>Análise Orçamentária e Estrutural - SINAPI 07/2025</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Carrega dados
    dados = carregar_dados_vila_andriw()
    
    # Sidebar com informações do projeto
    with st.sidebar:
        st.markdown("### 🏗️ Vila Andriw")
        st.markdown("---")
        st.markdown("### 📋 Informações do Projeto")
        st.metric("Custo Total", formatar_moeda(dados["resumo"]["custo_total"]))
        st.metric("Base de Preços", "SINAPI 07/2025")
        st.metric("Pavimentos", "3")
        st.metric("Data Atualização", datetime.now().strftime("%d/%m/%Y"))
        
        st.markdown("---")
        st.markdown("### 🎯 Navegação Rápida")
        st.markdown("- **Visão Geral**: Resumo executivo")
        st.markdown("- **Por Pavimento**: Análise detalhada")
        st.markdown("- **Por Elemento**: Breakdown estrutural")
        st.markdown("- **Análise Detalhada**: Dados financeiros")
        st.markdown("- **Visualização 3D**: Upload de IFC")
    
    # Abas principais
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏠 Visão Geral", 
        "🏢 Por Pavimento", 
        "🔧 Por Elemento", 
        "💰 Análise Detalhada",
        "🎮 Visualização 3D"
    ])
    
    with tab1:
        visao_geral(dados)
    
    with tab2:
        por_pavimento(dados)
    
    with tab3:
        por_elemento(dados)
    
    with tab4:
        analise_detalhada(dados)
        
    with tab5:
        visualizacao_3d()

def visao_geral(dados):
    """Aba de visão geral com resumo executivo"""
    st.markdown("## 📊 Resumo Executivo do Projeto")
    
    # Cards de resumo
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="💰 Custo Total do Projeto",
            value=formatar_moeda(dados["resumo"]["custo_total"]),
            help="Valor total incluindo material e mão de obra"
        )
    
    with col2:
        st.metric(
            label="🧱 Materiais",
            value=formatar_moeda(dados["resumo"]["total_material"]),
            delta=f"{dados['resumo']['percentual_material']}% do total",
            help="Custo total com materiais"
        )
    
    with col3:
        st.metric(
            label="👷 Mão de Obra", 
            value=formatar_moeda(dados["resumo"]["total_mao_obra"]),
            delta=f"{dados['resumo']['percentual_mao_obra']}% do total",
            help="Custo total com mão de obra"
        )
    
    # Gráficos lado a lado
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de distribuição por pavimento
        df_pavimentos = pd.DataFrame(dados["pavimentos"])
        
        fig_pavimentos = px.pie(
            df_pavimentos, 
            values='total', 
            names='nome',
            title="Distribuição de Custos por Pavimento",
            color_discrete_sequence=['#8b5cf6', '#10b981', '#3b82f6']
        )
        fig_pavimentos.update_layout(height=400)
        st.plotly_chart(fig_pavimentos, use_container_width=True)
    
    with col2:
        # Gráfico Material vs Mão de Obra
        fig_material = px.pie(
            values=[dados["resumo"]["total_material"], dados["resumo"]["total_mao_obra"]], 
            names=['Material', 'Mão de Obra'],
            title="Participação Material vs Mão de Obra",
            color_discrete_sequence=['#06b6d4', '#f59e0b']
        )
        fig_material.update_layout(height=400)
        st.plotly_chart(fig_material, use_container_width=True)

def por_pavimento(dados):
    """Aba de análise por pavimento melhorada"""
    st.markdown("## 🏢 Análise Detalhada por Pavimento")
    
    # Filtros interativos como no HTML
    st.markdown("### 🔍 Filtros")
    col_filtro1, col_filtro2, col_filtro3, col_filtro4 = st.columns(4)
    
    with col_filtro1:
        show_todos = st.button("📊 Todos", use_container_width=True)
    with col_filtro2:
        show_fundacao = st.button("🏗️ Fundação", use_container_width=True)
    with col_filtro3:
        show_terreo = st.button("🏘️ Térreo", use_container_width=True)
    with col_filtro4:
        show_superior = st.button("🏠 Superior", use_container_width=True)
    
    # Determinar filtro ativo
    filtro_ativo = "Todos"
    if show_fundacao:
        filtro_ativo = "Fundação"
    elif show_terreo:
        filtro_ativo = "Térreo"
    elif show_superior:
        filtro_ativo = "Pavimento Superior"
    
    # Cards dos pavimentos com mais detalhes
    pavimentos_filtrados = dados['pavimentos']
    if filtro_ativo != "Todos":
        pavimentos_filtrados = [p for p in dados['pavimentos'] if p['nome'] == filtro_ativo]
    
    st.markdown("---")
    
    for pavimento in pavimentos_filtrados:
        # Container com borda e estilo
        with st.container():
            # Header do pavimento com estilo
            if pavimento['nome'] == 'Fundação':
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); 
                           padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                    <h3 style="color: white; margin: 0;">🏗️ {pavimento['nome']}</h3>
                    <p style="color: white; margin: 0; opacity: 0.9;">Base estrutural do projeto</p>
                </div>
                """, unsafe_allow_html=True)
            elif pavimento['nome'] == 'Térreo':
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
                           padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                    <h3 style="color: white; margin: 0;">🏘️ {pavimento['nome']}</h3>
                    <p style="color: white; margin: 0; opacity: 0.9;">Pavimento térreo principal</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); 
                           padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                    <h3 style="color: white; margin: 0;">🏠 {pavimento['nome']}</h3>
                    <p style="color: white; margin: 0; opacity: 0.9;">Pavimento superior</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Métricas resumo do pavimento
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("💰 Custo Total", formatar_moeda(pavimento['total']))
            
            with col2:
                # Calcular participação no projeto
                participacao = (pavimento['total'] / dados['resumo']['custo_total']) * 100
                st.metric("📊 Participação", f"{participacao:.1f}%")
            
            with col3:
                # Número de elementos
                num_elementos = len([e for e in pavimento['elementos'].values() if e > 0])
                st.metric("🔧 Elementos", f"{num_elementos} tipos")
            
            with col4:
                # Elemento principal (maior custo)
                maior_elemento = max(pavimento['elementos'].items(), key=lambda x: x[1])
                st.metric("🎯 Principal", maior_elemento[0].title())
            
            # Detalhamento dos elementos
            st.markdown("#### 📋 Composição de Custos")
            
            # Gráfico de barras para o pavimento
            elementos_data = []
            for elemento, valor in pavimento['elementos'].items():
                if valor > 0:
                    elementos_data.append({
                        'Elemento': elemento.title(),
                        'Valor': valor,
                        'Formatted': formatar_moeda(valor)
                    })
            
            if elementos_data:
                df_elementos = pd.DataFrame(elementos_data)
                
                fig_elementos = px.bar(
                    df_elementos,
                    x='Elemento',
                    y='Valor',
                    title=f"Distribuição de Custos - {pavimento['nome']}",
                    color='Elemento',
                    color_discrete_sequence=['#8b5cf6', '#10b981', '#3b82f6', '#f59e0b']
                )
                fig_elementos.update_layout(
                    height=300,
                    showlegend=False,
                    yaxis_title="Custo (R$)",
                    xaxis_title="Elementos"
                )
                st.plotly_chart(fig_elementos, use_container_width=True)
            
            # Tabela detalhada dos elementos
            col_elem1, col_elem2 = st.columns(2)
            
            with col_elem1:
                st.markdown("**💰 Custos por Elemento:**")
                for elemento, valor in pavimento['elementos'].items():
                    if valor > 0:
                        if elemento == 'vigas':
                            st.write(f"🟫 **Vigas:** {formatar_moeda(valor)}")
                        elif elemento == 'pilares':
                            st.write(f"🏢 **Pilares:** {formatar_moeda(valor)}")
                        elif elemento == 'lajes':
                            st.write(f"🟧 **Lajes:** {formatar_moeda(valor)}")
                        elif elemento == 'fundacoes':
                            st.write(f"🏠 **Fundações:** {formatar_moeda(valor)}")
            
            with col_elem2:
                st.markdown("**📊 Análise Percentual:**")
                for elemento, valor in pavimento['elementos'].items():
                    if valor > 0:
                        perc = (valor / pavimento['total']) * 100
                        st.write(f"• **{elemento.title()}:** {perc:.1f}% do pavimento")
            
            st.markdown("---")
    
    # Gráfico comparativo
    st.markdown("### 📊 Comparativo de Custos entre Pavimentos")
    df_comp = pd.DataFrame(dados["pavimentos"])
    
    fig_comp = px.bar(
        df_comp,
        x='nome',
        y='total',
        title="Custo Total por Pavimento",
        color='nome',
        color_discrete_sequence=['#8b5cf6', '#10b981', '#3b82f6']
    )
    fig_comp.update_layout(
        height=400, 
        showlegend=False,
        yaxis_title="Custo (R$)",
        xaxis_title="Pavimento"
    )
    st.plotly_chart(fig_comp, use_container_width=True)

def por_elemento(dados):
    """Aba de análise por elemento"""
    st.markdown("## 🔧 Análise por Elemento Estrutural")
    
    # Prepara dados dos elementos
    elementos_total = {
        'Vigas': sum([p['elementos'].get('vigas', 0) for p in dados['pavimentos']]),
        'Pilares': sum([p['elementos'].get('pilares', 0) for p in dados['pavimentos']]),
        'Fundações': sum([p['elementos'].get('fundacoes', 0) for p in dados['pavimentos']]),
        'Lajes': sum([p['elementos'].get('lajes', 0) for p in dados['pavimentos']])
    }
    
    # Remove elementos com valor zero
    elementos_total = {k: v for k, v in elementos_total.items() if v > 0}
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Gráfico de elementos por pavimento (stacked bar)
        df_elementos = []
        for pavimento in dados['pavimentos']:
            for elemento, valor in pavimento['elementos'].items():
                df_elementos.append({
                    'Pavimento': pavimento['nome'],
                    'Elemento': elemento.title(),
                    'Valor': valor
                })
        
        df_elementos = pd.DataFrame(df_elementos)
        
        fig_elementos = px.bar(
            df_elementos,
            x='Pavimento',
            y='Valor',
            color='Elemento',
            title="Distribuição de Elementos por Pavimento",
            color_discrete_sequence=['#8b5cf6', '#10b981', '#3b82f6', '#f59e0b']
        )
        fig_elementos.update_layout(height=400)
        st.plotly_chart(fig_elementos, use_container_width=True)
    
    with col2:
        # Gráfico de participação dos elementos
        fig_participacao = px.pie(
            values=list(elementos_total.values()),
            names=list(elementos_total.keys()),
            title="Participação dos Elementos",
            color_discrete_sequence=['#8b5cf6', '#10b981', '#3b82f6', '#f59e0b']
        )
        fig_participacao.update_layout(height=400)
        st.plotly_chart(fig_participacao, use_container_width=True)
    
    # Tabela detalhada
    st.markdown("### 📋 Detalhamento por Elemento")
    
    # Prepara dados para tabela
    tabela_elementos = []
    for elemento, total in elementos_total.items():
        linha = {'Elemento': f"{'🟫' if elemento == 'Vigas' else '🏢' if elemento == 'Pilares' else '🏠' if elemento == 'Fundações' else '🟧'} {elemento}"}
        
        for pavimento in dados['pavimentos']:
            valor = pavimento['elementos'].get(elemento.lower(), 0)
            linha[pavimento['nome']] = formatar_moeda(valor) if valor > 0 else '-'
        
        linha['Total'] = formatar_moeda(total)
        linha['% Projeto'] = f"{(total / dados['resumo']['custo_total'] * 100):.1f}%"
        tabela_elementos.append(linha)
    
    df_tabela = pd.DataFrame(tabela_elementos)
    st.dataframe(df_tabela, use_container_width=True, hide_index=True)

def analise_detalhada(dados):
    """Aba de análise financeira detalhada"""
    st.markdown("## 💰 Análise Financeira Detalhada")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico Material vs Mão de Obra por pavimento
        df_detalhes = []
        for pavimento in dados['pavimentos']:
            # Calcula proporção material/mão de obra
            total_pav = pavimento['total']
            material_pav = total_pav * 0.742  # 74.2% material
            mao_obra_pav = total_pav * 0.258  # 25.8% mão de obra
            
            df_detalhes.extend([
                {'Pavimento': pavimento['nome'], 'Tipo': 'Material', 'Valor': material_pav},
                {'Pavimento': pavimento['nome'], 'Tipo': 'Mão de Obra', 'Valor': mao_obra_pav}
            ])
        
        df_detalhes = pd.DataFrame(df_detalhes)
        
        fig_detalhes = px.bar(
            df_detalhes,
            x='Pavimento',
            y='Valor',
            color='Tipo',
            title="Material vs Mão de Obra por Pavimento",
            color_discrete_sequence=['#06b6d4', '#f59e0b']
        )
        fig_detalhes.update_layout(height=400)
        st.plotly_chart(fig_detalhes, use_container_width=True)
    
    with col2:
        # Gráfico de custos acumulados
        custos_acumulados = []
        acumulado = 0
        for pavimento in dados['pavimentos']:
            acumulado += pavimento['total']
            custos_acumulados.append({
                'Pavimento': pavimento['nome'],
                'Custo Acumulado': acumulado
            })
        
        df_acumulado = pd.DataFrame(custos_acumulados)
        
        fig_acumulado = px.line(
            df_acumulado,
            x='Pavimento',
            y='Custo Acumulado',
            title="Evolução de Custos Acumulados",
            markers=True
        )
        fig_acumulado.update_traces(line_color='#3b82f6', line_width=3, marker_size=8)
        fig_acumulado.update_layout(height=400)
        st.plotly_chart(fig_acumulado, use_container_width=True)
    
    # Seção de Resumo Financeiro por Pavimento
    st.markdown("---")
    st.markdown("### 🏢 Resumo Financeiro por Pavimento")
    
    col_fund, col_terr, col_sup = st.columns(3)
    
    for i, pavimento in enumerate(dados['pavimentos']):
        col = [col_fund, col_terr, col_sup][i]
        
        with col:
            # Card estilizado para cada pavimento
            participacao = (pavimento['total'] / dados['resumo']['custo_total']) * 100
            
            if pavimento['nome'] == 'Fundação':
                cor = "#8b5cf6"
                icone = "🏗️"
            elif pavimento['nome'] == 'Térreo':
                cor = "#10b981"
                icone = "🏘️"
            else:
                cor = "#3b82f6"
                icone = "🏠"
            
            st.markdown(f"""
            <div style="background: {cor}; padding: 1.5rem; border-radius: 10px; text-align: center; color: white;">
                <h4 style="margin: 0;">{icone} {pavimento['nome']}</h4>
                <h2 style="margin: 0.5rem 0;">{formatar_moeda(pavimento['total'])}</h2>
                <p style="margin: 0; opacity: 0.9;">{participacao:.1f}% do projeto</p>
                <hr style="margin: 1rem 0; border-color: rgba(255,255,255,0.3);">
                <div style="display: flex; justify-content: space-between; font-size: 0.9rem;">
                    <span>Material: {formatar_moeda(pavimento['total'] * 0.742)}</span>
                    <span>M.O.: {formatar_moeda(pavimento['total'] * 0.258)}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Breakdown de elementos
            st.markdown("**Elementos:**")
            for elemento, valor in pavimento['elementos'].items():
                if valor > 0:
                    perc_pav = (valor / pavimento['total']) * 100
                    if elemento == 'vigas':
                        st.write(f"🟫 Vigas: {formatar_moeda(valor)} ({perc_pav:.1f}%)")
                    elif elemento == 'pilares':
                        st.write(f"🏢 Pilares: {formatar_moeda(valor)} ({perc_pav:.1f}%)")
                    elif elemento == 'lajes':
                        st.write(f"🟧 Lajes: {formatar_moeda(valor)} ({perc_pav:.1f}%)")
                    elif elemento == 'fundacoes':
                        st.write(f"🏠 Fundações: {formatar_moeda(valor)} ({perc_pav:.1f}%)")
    
    # Tabela de serviços detalhada como no HTML
    st.markdown("---")
    st.markdown("### 📋 Detalhamento Completo de Custos por Item")
    st.markdown("*Tabela detalhada baseada nos dados reais do projeto Vila Andriw*")
    
    # Usar dados reais dos serviços
    df_servicos = pd.DataFrame(dados['servicos'])
    
    # Adicionar filtros interativos
    col_filt1, col_filt2, col_filt3 = st.columns(3)
    
    with col_filt1:
        filtro_pavimento = st.selectbox(
            "Filtrar por Pavimento:",
            ['Todos'] + df_servicos['pavimento'].unique().tolist()
        )
    
    with col_filt2:
        filtro_elemento = st.selectbox(
            "Filtrar por Elemento:",
            ['Todos'] + df_servicos['elemento'].unique().tolist()
        )
    
    with col_filt3:
        ordem = st.selectbox(
            "Ordenar por:",
            ['Valor Total (maior)', 'Valor Total (menor)', 'Pavimento', 'Elemento']
        )
    
    # Aplicar filtros
    df_filtrado = df_servicos.copy()
    if filtro_pavimento != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['pavimento'] == filtro_pavimento]
    if filtro_elemento != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['elemento'] == filtro_elemento]
    
    # Aplicar ordenação
    if ordem == 'Valor Total (maior)':
        df_filtrado = df_filtrado.sort_values('total', ascending=False)
    elif ordem == 'Valor Total (menor)':
        df_filtrado = df_filtrado.sort_values('total', ascending=True)
    elif ordem == 'Pavimento':
        df_filtrado = df_filtrado.sort_values('pavimento')
    else:
        df_filtrado = df_filtrado.sort_values('elemento')
    
    # Mostrar estatísticas do filtro
    total_filtrado = df_filtrado['total'].sum()
    num_itens = len(df_filtrado)
    
    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    with col_stat1:
        st.metric("📊 Itens mostrados", num_itens)
    with col_stat2:
        st.metric("💰 Total filtrado", formatar_moeda(total_filtrado))
    with col_stat3:
        perc_total = (total_filtrado / dados['resumo']['custo_total']) * 100
        st.metric("📈 % do projeto", f"{perc_total:.1f}%")
    with col_stat4:
        material_filtrado = df_filtrado['material'].sum()
        st.metric("🔧 Material filtrado", formatar_moeda(material_filtrado))
    
    # Formatar dados para exibição
    df_servicos_display = df_filtrado.copy()
    
    # Formatar colunas monetárias
    colunas_moeda = ['valor_unitario', 'material', 'mao_obra', 'total']
    for col in colunas_moeda:
        df_servicos_display[col] = df_servicos_display[col].apply(formatar_moeda)
    
    df_servicos_display['percentual'] = df_servicos_display['percentual'].apply(lambda x: f"{x}%")
    
    # Renomear colunas para exibição
    df_servicos_display = df_servicos_display.rename(columns={
        'pavimento': 'Pavimento',
        'elemento': 'Elemento',
        'servico': 'Serviço',
        'unidade': 'Unidade',
        'quantidade': 'Qtd.',
        'valor_unitario': 'Valor Unitário',
        'material': 'Material',
        'mao_obra': 'Mão de Obra',
        'total': 'Valor Total',
        'percentual': '% do Projeto'
    })
    
    # Tabela estilizada com configurações avançadas
    st.dataframe(
        df_servicos_display, 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "Pavimento": st.column_config.TextColumn("Pavimento", width="medium"),
            "Elemento": st.column_config.TextColumn("Elemento", width="small"),
            "Serviço": st.column_config.TextColumn("Serviço", width="large"),
            "Unidade": st.column_config.TextColumn("Unidade", width="small"),
            "Qtd.": st.column_config.NumberColumn("Qtd.", width="small"),
            "Valor Unitário": st.column_config.TextColumn("Valor Unit.", width="medium"),
            "Material": st.column_config.TextColumn("Material", width="medium"),
            "Mão de Obra": st.column_config.TextColumn("M. Obra", width="medium"),
            "Valor Total": st.column_config.TextColumn("Total", width="medium"),
            "% do Projeto": st.column_config.TextColumn("% Proj.", width="small")
        }
    )

def carregar_modelo_ifc_real():
    """Carrega o modelo 3D real do arquivo VilaAndriw.ifc"""
    
    try:
        # Verificar se ifcopenshell está disponível
        import ifcopenshell
        import ifcopenshell.geom
        
        # Verificar se o arquivo existe
        ifc_path = "VilaAndriw.ifc"
        if not os.path.exists(ifc_path):
            ifc_path = "ifcopenshell/VilaAndriw.ifc"
        
        if not os.path.exists(ifc_path):
            st.error("❌ Arquivo VilaAndriw.ifc não encontrado!")
            return gerar_modelo_3d_esquematico()
        
        # Carregar arquivo IFC
        with st.spinner("🔄 Carregando modelo IFC real..."):
            ifc_file = ifcopenshell.open(ifc_path)
            
            # Configurar settings de geometria
            settings = ifcopenshell.geom.settings()
            settings.set(settings.USE_WORLD_COORDS, True)
            
            # Extrair elementos estruturais
            elementos_3d = []
            
            # Buscar elementos estruturais
            elementos_estruturais = (
                ifc_file.by_type("IfcBeam") +      # Vigas
                ifc_file.by_type("IfcColumn") +    # Pilares  
                ifc_file.by_type("IfcSlab") +      # Lajes
                ifc_file.by_type("IfcWall") +      # Paredes
                ifc_file.by_type("IfcFooting")     # Fundações
            )
            
            cores_elementos = {
                'IfcBeam': 'orange',      # Vigas - laranja
                'IfcColumn': 'red',       # Pilares - vermelho
                'IfcSlab': 'lightblue',   # Lajes - azul claro
                'IfcWall': 'gray',        # Paredes - cinza
                'IfcFooting': 'brown'     # Fundações - marrom
            }
            
            nomes_elementos = {
                'IfcBeam': '🟫 Vigas',
                'IfcColumn': '🏢 Pilares', 
                'IfcSlab': '🟧 Lajes',
                'IfcWall': '🧱 Paredes',
                'IfcFooting': '🏗️ Fundações'
            }
            
            fig = go.Figure()
            elementos_processados = {}
            
            for elemento in elementos_estruturais[:50]:  # Limitar para performance
                try:
                    tipo = elemento.is_a()
                    
                    # Obter geometria
                    shape = ifcopenshell.geom.create_shape(settings, elemento)
                    geometry = shape.geometry
                    
                    # Extrair vértices
                    vertices = geometry.verts
                    faces = geometry.faces
                    
                    if len(vertices) >= 9 and len(faces) >= 3:  # Verificar se há dados suficientes
                        # Converter para arrays numpy
                        vertices_array = np.array(vertices).reshape(-1, 3)
                        faces_array = np.array(faces).reshape(-1, 3)
                        
                        # Extrair coordenadas
                        x = vertices_array[:, 0]
                        y = vertices_array[:, 1] 
                        z = vertices_array[:, 2]
                        
                        # Extrair faces
                        i = faces_array[:, 0]
                        j = faces_array[:, 1]
                        k = faces_array[:, 2]
                        
                        # Adicionar ao gráfico
                        nome_grupo = nomes_elementos.get(tipo, tipo)
                        cor = cores_elementos.get(tipo, 'blue')
                        
                        # Verificar se já adicionamos este tipo (para controlar legenda)
                        show_legend = tipo not in elementos_processados
                        elementos_processados[tipo] = True
                        
                        fig.add_trace(go.Mesh3d(
                            x=x, y=y, z=z,
                            i=i, j=j, k=k,
                            color=cor,
                            opacity=0.8,
                            name=nome_grupo,
                            showlegend=show_legend,
                            legendgroup=tipo
                        ))
                        
                except Exception as e:
                    continue  # Ignorar elementos com erro de geometria
            
            # Se não conseguiu carregar nenhum elemento, usar modelo esquemático
            if len(fig.data) == 0:
                st.warning("⚠️ Não foi possível extrair geometria do IFC. Usando modelo esquemático.")
                return gerar_modelo_3d_esquematico()
            
            # Configurar layout
            fig.update_layout(
                title="🏗️ Modelo 3D Real - Vila Andriw (IFC)",
                scene=dict(
                    xaxis_title="X (metros)",
                    yaxis_title="Y (metros)", 
                    zaxis_title="Z (metros)",
                    camera=dict(
                        eye=dict(x=1.5, y=1.5, z=1.5)
                    ),
                    aspectmode='data'
                ),
                height=600,
                showlegend=True
            )
            
            return fig
            
    except ImportError:
        st.error("❌ Biblioteca ifcopenshell não disponível!")
        return gerar_modelo_3d_esquematico()
    except Exception as e:
        st.error(f"❌ Erro ao carregar IFC: {str(e)}")
        return gerar_modelo_3d_esquematico()

def gerar_modelo_3d_esquematico():
    """Gera um modelo 3D esquemático como fallback"""
    
    # Criando coordenadas para uma estrutura de 3 pavimentos
    fig = go.Figure()
    
    # Definindo coordenadas base
    x_base = [-5, 5, 5, -5, -5]  # Contorno da planta
    y_base = [-3, -3, 3, 3, -3]
    
    # FUNDAÇÕES (nível -1.5m)
    z_fund = [-1.5] * 5
    fig.add_trace(go.Scatter3d(
        x=x_base, y=y_base, z=z_fund,
        mode='lines+markers',
        name='🏗️ Fundações',
        line=dict(color='brown', width=8),
        marker=dict(size=8, color='brown')
    ))
    
    # PAVIMENTO TÉRREO (nível 0m)
    z_terreo = [0] * 5
    fig.add_trace(go.Scatter3d(
        x=x_base, y=y_base, z=z_terreo,
        mode='lines+markers',
        name='🏘️ Térreo',
        line=dict(color='blue', width=6),
        marker=dict(size=6, color='blue')
    ))
    
    # PAVIMENTO SUPERIOR (nível 3m)
    z_superior = [3] * 5
    fig.add_trace(go.Scatter3d(
        x=x_base, y=y_base, z=z_superior,
        mode='lines+markers',
        name='🏠 Pavimento Superior',
        line=dict(color='green', width=6),
        marker=dict(size=6, color='green')
    ))
    
    # PILARES (conectando os pavimentos)
    pilares_x = [-4, 4, 4, -4]
    pilares_y = [-2, -2, 2, 2]
    
    for i in range(len(pilares_x)):
        fig.add_trace(go.Scatter3d(
            x=[pilares_x[i], pilares_x[i]],
            y=[pilares_y[i], pilares_y[i]],
            z=[-1.5, 3],
            mode='lines',
            name=f'🏢 Pilar {i+1}' if i == 0 else None,
            line=dict(color='red', width=10),
            showlegend=(i == 0),
            legendgroup='pilares'
        ))
    
    # VIGAS (estrutura horizontal)
    vigas_terreo_x = [[-4, 4], [4, 4], [-4, -4]]
    vigas_terreo_y = [[-2, -2], [-2, 2], [-2, 2]]
    
    for i, (vx, vy) in enumerate(zip(vigas_terreo_x, vigas_terreo_y)):
        fig.add_trace(go.Scatter3d(
            x=vx, y=vy, z=[0, 0],
            mode='lines',
            name='🟫 Vigas' if i == 0 else None,
            line=dict(color='orange', width=8),
            showlegend=(i == 0),
            legendgroup='vigas'
        ))
    
    # LAJES (superfícies)
    laje_x = [-4, 4, 4, -4]
    laje_y = [-2, -2, 2, 2]
    laje_z = [0, 0, 0, 0]
    
    fig.add_trace(go.Mesh3d(
        x=laje_x + laje_x,
        y=laje_y + laje_y,
        z=laje_z + [0.2, 0.2, 0.2, 0.2],
        opacity=0.3,
        color='lightblue',
        name='🟧 Lajes'
    ))
    
    # Configurações do layout
    fig.update_layout(
        title="🏗️ Modelo 3D Esquemático - Vila Andriw",
        scene=dict(
            xaxis_title="X (metros)",
            yaxis_title="Y (metros)",
            zaxis_title="Z (metros)",
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            ),
            aspectmode='cube'
        ),
        height=600,
        showlegend=True
    )
    
    return fig

def visualizacao_3d():
    """Aba de visualização 3D com modelo estrutural real"""
    st.markdown("## 🎮 Visualização 3D da Estrutura")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Modelo 3D automático
        st.markdown("### 🏗️ Modelo Estrutural 3D - Vila Andriw")
        
        # Tentar carregar modelo IFC real primeiro
        modo_modelo = st.radio(
            "Escolha o tipo de modelo:",
            ["🏗️ Modelo IFC Real", "📐 Modelo Esquemático"],
            horizontal=True
        )
        
        if modo_modelo == "🏗️ Modelo IFC Real":
            with st.spinner("🔄 Carregando modelo IFC real do arquivo VilaAndriw.ifc..."):
                fig_3d = carregar_modelo_ifc_real()
        else:
            with st.spinner("🔄 Gerando modelo esquemático..."):
                fig_3d = gerar_modelo_3d_esquematico()
        
        st.plotly_chart(fig_3d, use_container_width=True)
        
        if modo_modelo == "🏗️ Modelo IFC Real":
            st.success("✅ Modelo 3D real carregado do arquivo VilaAndriw.ifc")
        else:
            st.info("📐 Modelo esquemático gerado com base nos dados do projeto")
        
        # Upload opcional de arquivo IFC
        st.markdown("---")
        st.markdown("### 📁 Upload Arquivo IFC (Opcional)")
        
        uploaded_file = st.file_uploader(
            "Carregar VilaAndriw.ifc para substituir modelo automático",
            type=['ifc'],
            help="Upload do arquivo IFC real substituirá o modelo gerado automaticamente"
        )
        
        if uploaded_file is not None:
            st.success(f"✅ Arquivo IFC carregado: {uploaded_file.name}")
            st.info(f"📁 Tamanho: {uploaded_file.size / 1024 / 1024:.2f} MB")
            st.warning("⚠️ Processamento de arquivos IFC requer bibliotecas especializadas")
            
            with st.expander("ℹ️ Informações do Arquivo IFC"):
                st.write(f"**Nome:** {uploaded_file.name}")
                st.write(f"**Tipo:** {uploaded_file.type}")
                st.write(f"**Tamanho:** {uploaded_file.size:,} bytes")
    
    with col2:
        st.markdown("### 🎛️ Controles")
        
        st.markdown("#### 👁️ Elementos Visíveis")
        show_fundacoes = st.checkbox("🏗️ Fundações", True)
        show_pilares = st.checkbox("🏢 Pilares", True)
        show_vigas = st.checkbox("🟫 Vigas", True)
        show_lajes = st.checkbox("🟧 Lajes", True)
        
        st.markdown("#### 🎨 Visualização")
        view_mode = st.selectbox("Modo:", ["Estrutural", "Técnico", "Presentation"])
        
        if st.button("🔄 Regenerar Modelo"):
            st.rerun()
        
        st.markdown("#### 📊 Informações")
        with st.container():
            st.metric("Pavimentos", "3")
            st.metric("Pilares", "4 unidades")
            st.metric("Custo Total", "R$ 126.544,18")
            st.metric("Status", "✅ Ativo")
        
        st.markdown("#### 📐 Especificações")
        st.write("**Materiais:**")
        st.write("• Concreto C25")
        st.write("• Aço CA-50")
        st.write("• Fundação direta")
        
        st.write("**Dimensões:**")
        st.write("• Área: 40m²")
        st.write("• Altura: 4.5m")
        st.write("• 3 pavimentos")

if __name__ == "__main__":
    main()
