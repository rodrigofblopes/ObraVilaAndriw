import streamlit as st
import os
from openai import OpenAI

# Configuração da página
st.set_page_config(
    page_title="Perguntas - Vila Andriw",
    page_icon="❓",
    layout="wide"
)

# Estilo CSS personalizado
st.markdown("""
<style>
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
        gap: 0.5rem;
    }
    .chat-message.user {
        background-color: #f0f9ff;
        border-left: 4px solid #3b82f6;
    }
    .chat-message.assistant {
        background-color: #f0fdf4;
        border-left: 4px solid #10b981;
    }
    .chat-message .avatar {
        width: 2.5rem;
        height: 2.5rem;
        border-radius: 0.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
    }
    .chat-message .content {
        flex: 1;
    }
    .chat-message .content p {
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)

# Título e descrição
st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <h1>❓ Perguntas sobre o Projeto</h1>
    <p style="font-size: 1.2rem; opacity: 0.8;">
        Tire suas dúvidas sobre o projeto Vila Andriw usando IA
    </p>
</div>
""", unsafe_allow_html=True)

# Inicializar o cliente OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Inicializar histórico de chat na sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

# Função para gerar resposta
def generate_response(prompt):
    try:
        # Contexto do projeto
        system_prompt = """Você é um assistente especializado no projeto Vila Andriw, um projeto de construção civil com as seguintes características:

        - Projeto: Vila Andriw
        - Tipo: Residencial
        - Área: ~40m²
        - Pavimentos: 3 (Fundação, Térreo, Superior)
        - Custo Total: R$ 126.544,18
        - Material: R$ 93.845,16 (74.2%)
        - Mão de Obra: R$ 32.699,02 (25.8%)
        
        Especificações Técnicas:
        - Concreto: C25/C30 MPa
        - Aço: CA-50
        - Fundação: Sapatas corridas
        - Lajes: Nervuradas e maciças
        - Altura total: 4.5m
        - Pé-direito: 2.7m
        
        Responda às perguntas de forma técnica mas compreensível, usando os dados acima quando relevante."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Erro ao gerar resposta: {str(e)}"

# Interface do chat
st.markdown("### 💬 Chat")

# Exibir mensagens anteriores
for message in st.session_state.messages:
    with st.container():
        st.markdown(f"""
        <div class="chat-message {message['role']}">
            <div class="avatar">{' 👤 ' if message['role'] == 'user' else ' 🤖 '}</div>
            <div class="content">
                <p>{message['content']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Input do usuário
user_input = st.text_input("Digite sua pergunta sobre o projeto:", key="user_input")

# Botão de envio
if st.button("Enviar Pergunta"):
    if user_input:
        # Adicionar pergunta do usuário ao histórico
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Gerar e adicionar resposta ao histórico
        response = generate_response(user_input)
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Limpar input
        st.session_state.user_input = ""
        
        # Recarregar página para mostrar nova mensagem
        st.rerun()

# Botão para limpar histórico
if st.button("Limpar Histórico"):
    st.session_state.messages = []
    st.rerun()

# Informações adicionais
with st.expander("ℹ️ Sobre o Assistente"):
    st.markdown("""
    Este assistente usa IA para responder perguntas sobre o projeto Vila Andriw. Ele pode ajudar com:
    
    - 📊 Informações sobre custos e orçamento
    - 🏗️ Detalhes técnicos da construção
    - 📐 Especificações de materiais e dimensões
    - 💰 Análise financeira do projeto
    
    As respostas são baseadas nos dados reais do projeto.
    """)

# Dicas de uso
with st.expander("💡 Exemplos de Perguntas"):
    st.markdown("""
    - Qual é o custo total do projeto?
    - Como é feita a fundação do projeto?
    - Qual é a especificação do concreto usado?
    - Quanto custa o material em relação à mão de obra?
    - Quais são as dimensões do projeto?
    """)
