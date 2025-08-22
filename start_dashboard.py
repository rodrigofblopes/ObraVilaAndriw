#!/usr/bin/env python3
"""
Script simples para iniciar o Dashboard Vila Andriw
"""

import subprocess
import sys
import os

def main():
    print("🚀 Iniciando Dashboard Vila Andriw...")
    print("📱 A aplicação será aberta automaticamente no navegador")
    print("🌐 URL: http://localhost:8501")
    print("\n⏹️ Para parar a aplicação, pressione Ctrl+C")
    print("="*50)
    
    try:
        # Executa o Streamlit usando subprocess
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "dashboard.py",
            "--server.headless=false",
            "--server.port=8501",
            "--browser.gatherUsageStats=false"
        ], check=True)
    except KeyboardInterrupt:
        print("\n\n⏹️ Aplicação finalizada pelo usuário")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erro ao executar aplicação: {e}")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")

if __name__ == "__main__":
    main()
