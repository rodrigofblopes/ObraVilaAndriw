#!/usr/bin/env python3
"""
Script para executar o Dashboard Vila Andriw localmente
"""

import subprocess
import sys
import os

def verificar_dependencias():
    """Verifica se todas as dependências estão instaladas"""
    print("🔍 Verificando dependências...")
    
    dependencias = ['streamlit', 'pandas', 'plotly', 'numpy']
    faltando = []
    
    for dep in dependencias:
        try:
            __import__(dep)
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep} - não instalado")
            faltando.append(dep)
    
    # Verificar ifcopenshell separadamente (opcional)
    try:
        import ifcopenshell
        print("✅ ifcopenshell (3D IFC)")
    except ImportError:
        print("⚠️ ifcopenshell - não instalado (opcional para 3D real)")
        print("💡 Para modelo 3D real: pip install ifcopenshell")
    
    if faltando:
        print(f"\n⚠️ Dependências faltando: {', '.join(faltando)}")
        print("📦 Instalando dependências...")
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + faltando)
        print("✅ Dependências instaladas!")
    
    return True

def executar_app():
    """Executa a aplicação Streamlit"""
    print("\n🚀 Iniciando Dashboard Vila Andriw...")
    print("📱 A aplicação será aberta automaticamente no navegador")
    print("🌐 URL: http://localhost:8501")
    print("\n⏹️ Para parar a aplicação, pressione Ctrl+C")
    print("="*50)
    
    try:
        # Executa o Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "dashboard.py",
            "--server.headless=false",
            "--server.port=8501",
            "--browser.gatherUsageStats=false"
        ])
    except KeyboardInterrupt:
        print("\n\n⏹️ Aplicação finalizada pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro ao executar aplicação: {e}")

def main():
    """Função principal"""
    print("🏗️ Dashboard Vila Andriw - Startup Script")
    print("="*50)
    
    # Verifica se está no diretório correto
    if not os.path.exists("dashboard.py"):
        print("❌ Erro: arquivo dashboard.py não encontrado!")
        print("📁 Certifique-se de estar no diretório correto")
        sys.exit(1)
    
    # Verifica dependências
    if verificar_dependencias():
        print("\n💡 DICA DE DEPLOY:")
        print("📁 Para deploy online, veja: GUIA_DEPLOY_GITHUB.md")
        print("🌐 GitHub + Streamlit Cloud = Deploy gratuito!")
        executar_app()

if __name__ == "__main__":
    main()
