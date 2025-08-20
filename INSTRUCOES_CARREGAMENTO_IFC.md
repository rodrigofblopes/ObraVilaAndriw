# 🤖 Carregamento Automático IFC - Vila Andriw

## 🎯 Sistema Implementado

O dashboard agora possui **carregamento automático** do arquivo VilaAndriw.ifc real, eliminando a necessidade de seleção manual e **sem modelos demo**.

## 📁 Como Configurar o Carregamento Automático

### Opção 1: Carregamento Automático (Recomendado)
1. **Coloque o arquivo `VilaAndriw.ifc` na mesma pasta** que o `dashboard_vila_andriw_csv.html`
2. **Abra o dashboard** no navegador
3. **Vá para a aba "Visualização 3D"**
4. **O sistema carrega automaticamente** o VilaAndriw.ifc

### Opção 2: Seleção Manual (Fallback)
1. **Clique em "Seleção Manual"** na aba 3D
2. **Selecione o arquivo** VilaAndriw.ifc de qualquer pasta
3. **Aguarde o carregamento** do modelo real

## 🔧 Estrutura de Pastas Recomendada

```
Projeto_Vila_Andriw/
├── dashboard_vila_andriw_csv.html          # Dashboard principal
├── VilaAndriw.ifc                          # Arquivo IFC real
├── Vila Andriw - Sintético....csv          # Dados orçamentários
└── README_Vila_Andriw_Dashboard.md         # Documentação
```

## 🚀 Funcionalidades do Sistema

### ✅ Carregamento Automático
- **Detecta automaticamente** VilaAndriw.ifc na pasta
- **Carrega geometria real** extraída do arquivo IFC
- **Materiais coloridos** por tipo de elemento
- **Informações precisas** extraídas do modelo

### ✅ Sistema Robusto
- **Logs detalhados** no console do navegador
- **Verificação de integridade** do arquivo
- **Tratamento de erros** elegante
- **Fallback para seleção manual** se automático falhar

### ✅ Visualização Profissional
- **Cores por elemento**: Vigas (roxo), Pilares (verde), Lajes (amarelo), Fundações (cinza)
- **Controles 3D**: Rotação, zoom, pan com mouse
- **Contagem real**: Número exato de elementos do IFC
- **Metadados**: Tamanho, versão IFC, status

## 🎮 Como Usar

### Primeira Vez:
1. **Coloque VilaAndriw.ifc** na mesma pasta do HTML
2. **Abra dashboard_vila_andriw_csv.html** no navegador
3. **Clique na aba "Visualização 3D"**
4. **Aguarde** - sistema carrega automaticamente
5. **Explore** o modelo 3D real do Vila Andriw

### Controles do Visualizador:
- **Mouse**: Rotação da câmera
- **Scroll**: Zoom in/out
- **Botão direito + arraste**: Pan (mover visualização)
- **Botão "Reset"**: Volta para posição inicial

## 🔍 Verificação de Funcionamento

### Console do Navegador (F12):
```
🚀 Sistema de visualização IFC REAL inicializado
🎯 MODO AUTOMÁTICO ATIVADO:
   ✅ Abre aba "Visualização 3D" → Carrega VilaAndriw.ifc automaticamente
   📁 Se automático falhar → Use seleção manual
   🚫 SEM modelo demo - apenas IFC real!

💡 Dica: Coloque VilaAndriw.ifc na mesma pasta do HTML para carregamento automático
```

### Se Carregamento Automático Funcionar:
```
🎯 Aba 3D aberta - tentando carregamento automático...
🔍 Tentando carregar VilaAndriw.ifc automaticamente...
🚀 Iniciando carregamento automático do VilaAndriw.ifc...
📦 Carregando VilaAndriw.ifc da pasta...
✅ VilaAndriw.ifc carregado automaticamente!
🎨 Configurando materiais IFC...
📋 Extraindo informações do modelo IFC...
📊 Elementos encontrados: {vigas: X, pilares: Y, lajes: Z, fundacoes: W}
```

### Se Precisar de Seleção Manual:
```
ℹ️ Carregamento automático falhou: [motivo]
📁 Para carregar manualmente: clique no botão e selecione VilaAndriw.ifc
```

## ⚠️ Solução de Problemas

### 1. Carregamento Automático Não Funciona:
- **Verifique** se VilaAndriw.ifc está na mesma pasta do HTML
- **Use seleção manual** como alternativa
- **Verifique console** (F12) para detalhes do erro

### 2. Arquivo IFC Não Carrega:
- **Verifique** se o arquivo não está corrompido
- **Confirme** que é realmente um arquivo .ifc válido
- **Tente novamente** após alguns segundos

### 3. Modelo Não Aparece:
- **Aguarde** o carregamento completo
- **Use controles de mouse** para navegar
- **Clique "Reset"** para centralizar visualização

## 📊 Dados Extraídos do IFC Real

O sistema extrai automaticamente:
- **Contagem de elementos** por tipo (vigas, pilares, lajes, fundações)
- **Propriedades dos materiais** (concreto, aço)
- **Informações do projeto** (versão IFC, metadados)
- **Geometria 3D real** para visualização

## 🎊 Resultado Final

Dashboard com **visualização IFC real** que:
- ✅ **Carrega automaticamente** o VilaAndriw.ifc
- ✅ **Mostra geometria real** da estrutura
- ✅ **Elimina modelos demo** completamente
- ✅ **Extrai dados precisos** do arquivo IFC
- ✅ **Interface profissional** com controles intuitivos

---
*Sistema desenvolvido com web-ifc-three para máxima compatibilidade e precisão.*
