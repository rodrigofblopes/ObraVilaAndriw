#!/usr/bin/env python3
"""
Exemplo de uso do Extrator IFC para Dashboard de Volume de Aço
"""

import os
import json
from ifc_extractor import IFCSteelExtractor

def exemplo_basico():
    """Exemplo básico de uso do extrator"""
    
    # Caminho do arquivo IFC (substitua pelo seu arquivo)
    arquivo_ifc = "exemplo_projeto.ifc"
    
    # Verificar se o arquivo existe
    if not os.path.exists(arquivo_ifc):
        print(f"❌ Arquivo não encontrado: {arquivo_ifc}")
        print("📝 Crie um arquivo IFC ou altere o caminho no código")
        return
    
    print("🚀 Iniciando extração de dados IFC...")
    
    # Criar instância do extrator
    extrator = IFCSteelExtractor(arquivo_ifc)
    
    # Carregar arquivo IFC
    if not extrator.carregar_ifc():
        print("❌ Erro ao carregar arquivo IFC")
        return
    
    # Extrair informações do projeto
    info_projeto = extrator.extrair_info_projeto()
    print(f"📋 Projeto: {info_projeto['nome']}")
    
    # Gerar dados do dashboard
    dados = extrator.gerar_dados_dashboard()
    
    # Exibir resumo dos resultados
    resumo = dados['volume_aco']['resumo']
    print(f"\n📊 Resumo dos Resultados:")
    print(f"   💪 Peso total de aço: {resumo['peso_total']:.2f} kg")
    print(f"   🏢 Pavimentos: {resumo['pavimentos']}")
    print(f"   🔧 Bitolas diferentes: {resumo['bitolas_diferentes']}")
    
    # Salvar dados em JSON
    arquivo_json = "dados_extraidos.json"
    extrator.salvar_dados_json(dados, arquivo_json)
    print(f"�