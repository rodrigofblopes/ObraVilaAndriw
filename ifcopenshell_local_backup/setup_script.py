#!/usr/bin/env python3
"""
Script de configuração e instalação para o Extrator IFC
Configura o ambiente Python e instala dependências necessárias
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def verificar_python():
    """Verifica a versão do Python"""
    versao = sys.version_info
    print(f"🐍 Python {versao.major}.{versao.minor}.{versao.micro}")
    
    if versao.major < 3 or (versao.major == 3 and versao.minor < 8):
        print("❌ Python 3.8+ é necessário!")
        return False
    
    print("✅ Versão do Python compatível")
    return True

def verificar_pip():
    """Verifica se pip está instalado"""
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
        print("✅ pip está instalado")
        return True
    except subprocess.CalledProcessError:
        print("❌ pip não encontrado!")
        return False

def criar_ambiente_virtual():
    """Cria ambiente virtual Python"""
    venv_path = Path("venv_ifc")
    
    if venv_path.exists():
        print("📁 Ambiente virtual já existe")
        return True
    
    try:
        print("🔧 Criando ambiente virtual...")
        subprocess.run([sys.executable, "-m", "venv", "venv_ifc"], check=True)
        print("✅ Ambiente virtual criado: venv_ifc/")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao criar ambiente virtual: {e}")
        return False

def ativar_ambiente_virtual():
    """Fornece instruções para ativar o ambiente virtual"""
    sistema = platform.system().lower()
    
    print("\n🚀 Para ativar o ambiente virtual:")
    
    if sistema == "windows":
        print("   Windows: venv_ifc\\Scripts\\activate")
    else:
        print("   Linux/Mac: source venv_ifc/bin/activate")
    
    print("\n💡 Para desativar: deactivate")

def instalar_dependencias():
    """Instala as dependências necessárias"""
    
    # Determinar executável do Python no ambiente virtual
    sistema = platform.system().lower()
    if sistema == "windows":
        python_exe = Path("venv_ifc/Scripts/python.exe")
        pip_exe = Path("venv_ifc/Scripts/pip.exe")
    else:
        python_exe = Path("venv_ifc/bin/python")
        pip_exe = Path("venv_ifc/bin/pip")
    
    if not python_exe.exists():
        print("❌ Ambiente virtual não encontrado. Execute a criação primeiro.")
        return False
    
    try:
        print("📦 Instalando dependências...")
        
        # Atualizar pip
        print("   • Atualizando pip...")
        subprocess.run([str(pip_exe), "install", "--upgrade", "pip"], check=True)
        
        # Instalar ifcopenshell (dependência principal)
        print("   • Instalando ifcopenshell...")
        subprocess.run([str(pip_exe), "install", "ifcopenshell"], check=True)
        
        # Instalar outras dependências
        dependencias = [
            "numpy>=1.21.0",
            "pandas>=1.3.0", 
            "matplotlib>=3.5.0",
            "plotly>=5.0.0"
        ]
        
        for dep in dependencias:
            print(f"   • Instalando {dep}...")
            subprocess.run([str(pip_exe), "install", dep], check=True)
        
        print("✅ Todas as dependências instaladas!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def criar_arquivos_exemplo():
    """Cria arquivos de exemplo e documentação"""
    
    arquivos = {
        "README.md": gerar_readme(),
        "exemplo_uso.py": "# Arquivo de exemplo já criado separadamente",
        ".gitignore": gerar_gitignore(),
        "config.json": gerar_config_exemplo()
    }
    
    for nome, conteudo in arquivos.items():
        if not os.path.exists(nome):
            with open(nome, "w", encoding="utf-8") as f:
                f.write(conteudo)
            print(f"📄 Criado: {nome}")
        else:
            print(f"⚠️  Já existe: {nome}")

def gerar_readme():
    """Gera arquivo README.md"""
    return """# Extrator IFC para Dashboard de Volume de Aço

## Descrição
Este projeto extrai automaticamente informações de arquivos IFC (Industry Foundation Classes) e gera dashboards interativos para visualização do volume de aço estrutural.

## Funcionalidades
- ✅ Extração automática de dados de arquivos IFC
- ✅ Cálculo de volumes e pesos de aço por elemento
- ✅ Geração de dashboards HTML interativos
- ✅ Relatórios detalhados em JSON e TXT
- ✅ Análise por pavimento, bitola e tipo de elemento

## Instalação

1. **Clonar/baixar o projeto**
   ```bash
   git clone [url-do-projeto]
   cd extrator-ifc-aco
   ```

2. **Executar script de configuração**
   ```bash
   python setup.py
   ```

3. **Ativar ambiente virtual**
   ```bash
   # Windows
   venv_ifc\\Scripts\\activate
   
   # Linux/Mac
   source venv_ifc/bin/activate
   ```

## Uso Básico

### Linha de Comando
```bash
python ifc_extractor.py arquivo.ifc -o dados_aco.json
```

### Com Dashboard
```bash
python ifc_extractor.py arquivo.ifc -t dashboard_template.html -d dashboard_final.html
```

### Modo Interativo
```bash
python exemplo_uso.py
```

## Estrutura dos Dados

O extrator gera dados no seguinte formato:
```json
{
  "projeto": "Nome do Projeto",
  "data_atualizacao": "2025-01-13 10:00:00",
  "volume_aco": {
    "resumo": {
      "peso_total": 3296.68,
      "pavimentos": 3,
      "bitolas_diferentes": 5
    },
    "por_pavimento": [...],
    "por_bitola": [...],
    "por_elemento": [...]
  }
}
```

## Requisitos
- Python 3.8+
- ifcopenshell
- numpy, pandas (para análises)
- matplotlib, plotly (para gráficos)

## Limitações
- Baseado em estimativas padrão de taxas de armadura
- Requer arquivo IFC com elementos estruturais bem definidos
- Não processa armaduras explícitas (usa cálculos estimativos)

## Contribuição
1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## Licença
MIT License - veja arquivo LICENSE para detalhes
"""

def gerar_gitignore():
    """Gera arquivo .gitignore"""
    return """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv_ifc/
venv/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Arquivos do projeto
*.ifc
*.json
*.html
!dashboard_template.html
!config.json

# Logs
*.log

# OS
.DS_Store
Thumbs.db

# Dados temporários
temp/
output/
relatorios/
"""

def gerar_config_exemplo():
    """Gera arquivo de configuração exemplo"""
    return """{
  "configuracoes": {
    "densidades": {
      "aco": 7850,
      "concreto": 2500,
      "armadura": 7850
    },
    "taxas_armadura": {
      "pilares": 120,
      "vigas": 100,
      "lajes": 60,
      "sapatas": 80,
      "paredes": 40
    },
    "distribuicao_bitolas": {
      "default": {
        "5.0 mm": 0.20,
        "6.3 mm": 0.15,
    