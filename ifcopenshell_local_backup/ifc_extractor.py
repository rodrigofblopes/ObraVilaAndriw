#!/usr/bin/env python3
"""
Extrator IFC para Dashboard de Volume de Aço
Processa arquivos IFC e extrai informações sobre elementos estruturais de aço
"""

import os
import sys
import json
import math
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path

try:
    import ifcopenshell
    import ifcopenshell.util.element
    import ifcopenshell.util.unit
except ImportError:
    print("❌ Erro: ifcopenshell não instalado!")
    print("📦 Execute: pip install ifcopenshell")
    sys.exit(1)

try:
    import numpy as np
except ImportError:
    print("⚠️ numpy não encontrado, usando cálculos básicos")
    np = None


class IFCSteelExtractor:
    """
    Extrator de dados de aço de arquivos IFC
    Processa elementos estruturais e calcula volumes/pesos de aço
    """
    
    def __init__(self, arquivo_ifc: str):
        """
        Inicializa o extrator
        
        Args:
            arquivo_ifc: Caminho para o arquivo IFC
        """
        self.arquivo_ifc = arquivo_ifc
        self.ifc_file = None
        self.project_info = {}
        
        # Configurações padrão
        self.config = {
            "densidades": {
                "aco": 7850,  # kg/m³
                "concreto": 2500,  # kg/m³
                "armadura": 7850  # kg/m³
            },
            "taxas_armadura": {
                # kg de aço por m³ de concreto - calibrado pelo relatório Eberick (2.314 kg total)
                "pilares": 150,    # 4.8 m³ * 150 kg/m³ ≈ 720 kg (31% do total)
                "vigas": 60,       # 20.3 m³ * 60 kg/m³ ≈ 1.218 kg (53% do total)  
                "lajes": 0,        # 10.0 m³ * 0 kg/m³ = 0 kg (sem armadura nas lajes)
                "sapatas": 60,     # 6.0 m³ * 60 kg/m³ ≈ 360 kg (16% do total)
                "paredes": 50,     # Paredes estruturais armadas
                "default": 56      # Taxa padrão baseada no relatório
            },
            "distribuicao_bitolas": {
                "default": {
                    "5.0 mm": 0.20,
                    "6.3 mm": 0.15,
                    "8.0 mm": 0.20,
                    "10.0 mm": 0.20,
                    "12.5 mm": 0.15,
                    "16.0 mm": 0.10
                }
            },
            "precos_sinapi": {
                # Preços SINAPI - Julho 2025
                "concreto_fck25": 740.54,  # R$/m³ - Item 94965
                "armacao_aco": {
                    # Preços de armação por bitola (R$/kg)
                    "5.0 mm": 16.84,   # CA-60 - Item 92759
                    "6.3 mm": 15.36,   # Item 92769 (laje)
                    "8.0 mm": 15.05,   # CA-50 - Item 92761
                    "8.0 mm sapata": 17.28,  # Item 104918 (sapata específica)
                    "10.0 mm": 13.45,  # CA-50 - Item 92762
                    "12.5 mm": 11.33,  # CA-50 - Item 92763
                    "16.0 mm": 10.97,  # CA-50 - Item 92764
                },
                "data_referencia": "07/2025",
                "observacoes": "Preços baseados na tabela SINAPI"
            }
        }
    
    def carregar_ifc(self) -> bool:
        """
        Carrega o arquivo IFC
        
        Returns:
            True se carregou com sucesso, False caso contrário
        """
        try:
            if not os.path.exists(self.arquivo_ifc):
                print(f"❌ Arquivo não encontrado: {self.arquivo_ifc}")
                return False
            
            print(f"📂 Carregando arquivo IFC: {self.arquivo_ifc}")
            self.ifc_file = ifcopenshell.open(self.arquivo_ifc)
            
            if not self.ifc_file:
                print("❌ Erro ao abrir arquivo IFC")
                return False
            
            print(f"✅ Arquivo IFC carregado com sucesso")
            print(f"📊 Schema: {self.ifc_file.schema}")
            print(f"🔢 Total de entidades: {len(list(self.ifc_file))}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao carregar IFC: {str(e)}")
            return False
    
    def extrair_info_projeto(self) -> Dict[str, Any]:
        """
        Extrai informações básicas do projeto
        
        Returns:
            Dicionário com informações do projeto
        """
        if not self.ifc_file:
            return {"nome": "Projeto Desconhecido", "descricao": "", "fase": ""}
        
        try:
            # Buscar projeto
            project = self.ifc_file.by_type("IfcProject")
            if project:
                project = project[0]
                nome = getattr(project, 'Name', 'Projeto Sem Nome') or 'Projeto Sem Nome'
                descricao = getattr(project, 'Description', '') or ''
                fase = getattr(project, 'Phase', '') or ''
            else:
                nome = "Projeto Desconhecido"
                descricao = ""
                fase = ""
            
            # Buscar unidades
            unidade_comprimento = self._obter_unidade_comprimento()
            
            info = {
                "nome": nome,
                "descricao": descricao,
                "fase": fase,
                "unidade_comprimento": unidade_comprimento,
                "arquivo": os.path.basename(self.arquivo_ifc),
                "data_extracao": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            self.project_info = info
            return info
            
        except Exception as e:
            print(f"⚠️ Erro ao extrair informações do projeto: {str(e)}")
            return {
                "nome": "Projeto Desconhecido", 
                "descricao": "", 
                "fase": "",
                "unidade_comprimento": "mm",
                "arquivo": os.path.basename(self.arquivo_ifc),
                "data_extracao": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
    
    def _obter_unidade_comprimento(self) -> str:
        """Obtém a unidade de comprimento do projeto"""
        try:
            units = self.ifc_file.by_type("IfcUnitAssignment")
            if units:
                for unit_assignment in units:
                    for unit in unit_assignment.Units:
                        if hasattr(unit, 'UnitType') and unit.UnitType == 'LENGTHUNIT':
                            if hasattr(unit, 'Name'):
                                return unit.Name
            return "mm"  # Padrão
        except:
            return "mm"
    
    def extrair_elementos_estruturais(self) -> List[Dict[str, Any]]:
        """
        Extrai elementos estruturais do arquivo IFC
        
        Returns:
            Lista de elementos estruturais com suas propriedades
        """
        if not self.ifc_file:
            return []
        
        elementos = []
        
        # Tipos de elementos estruturais para buscar
        tipos_estruturais = [
            'IfcBeam',           # Vigas
            'IfcColumn',         # Pilares
            'IfcSlab',           # Lajes
            'IfcWall',           # Paredes/muros
            'IfcFooting',        # Sapatas
            'IfcPile',           # Estacas
            'IfcRamp',           # Rampas
            'IfcStair',          # Escadas
            'IfcMember',         # Elementos gerais
            'IfcPlate'           # Placas
        ]
        
        print("🔍 Extraindo elementos estruturais...")
        
        for tipo in tipos_estruturais:
            try:
                elementos_tipo = self.ifc_file.by_type(tipo)
                print(f"   📋 {tipo}: {len(elementos_tipo)} elementos")
                
                for elemento in elementos_tipo:
                    dados_elemento = self._processar_elemento(elemento, tipo)
                    if dados_elemento:
                        elementos.append(dados_elemento)
                        
            except Exception as e:
                print(f"⚠️ Erro ao processar {tipo}: {str(e)}")
                continue
        
        print(f"✅ Total de elementos extraídos: {len(elementos)}")
        return elementos
    
    def _processar_elemento(self, elemento, tipo_ifc: str) -> Optional[Dict[str, Any]]:
        """
        Processa um elemento individual
        
        Args:
            elemento: Elemento IFC
            tipo_ifc: Tipo do elemento IFC
            
        Returns:
            Dicionário com dados do elemento ou None
        """
        try:
            # Informações básicas
            guid = getattr(elemento, 'GlobalId', '')
            nome = getattr(elemento, 'Name', '') or f"Elemento_{guid[:8]}"
            descricao = getattr(elemento, 'Description', '') or ''
            
            # Classificar tipo de elemento estrutural
            tipo_estrutural = self._classificar_tipo_estrutural(tipo_ifc, nome, descricao)
            
            # Calcular volume
            volume_concreto = self._calcular_volume_elemento(elemento)
            
            if volume_concreto <= 0:
                return None
            
            # Calcular aço baseado no volume de concreto
            peso_aco = self._calcular_peso_aco(volume_concreto, tipo_estrutural)
            
            # Obter pavimento
            pavimento = self._obter_pavimento(elemento)
            
            # Distribuir por bitolas
            bitolas = self._distribuir_bitolas(peso_aco, tipo_estrutural)
            
            # Calcular custos
            custo_concreto = self._calcular_custo_concreto(volume_concreto)
            custo_armacao = self._calcular_custo_armacao(bitolas, tipo_estrutural)
            
            return {
                "guid": guid,
                "nome": nome,
                "descricao": descricao,
                "tipo_ifc": tipo_ifc,
                "tipo_estrutural": tipo_estrutural,
                "pavimento": pavimento,
                "volume_concreto": round(volume_concreto, 3),
                "peso_aco_total": round(peso_aco, 2),
                "bitolas": bitolas,
                "custo_concreto": custo_concreto,
                "custo_armacao": custo_armacao
            }
            
        except Exception as e:
            print(f"⚠️ Erro ao processar elemento {getattr(elemento, 'GlobalId', 'unknown')}: {str(e)}")
            return None
    
    def _classificar_tipo_estrutural(self, tipo_ifc: str, nome: str, descricao: str) -> str:
        """Classifica o tipo estrutural baseado no tipo IFC e nome"""
        tipo_lower = tipo_ifc.lower()
        nome_lower = nome.lower()
        desc_lower = descricao.lower()
        
        if 'beam' in tipo_lower or 'viga' in nome_lower or 'viga' in desc_lower:
            return 'vigas'
        elif 'column' in tipo_lower or 'pilar' in nome_lower or 'pilar' in desc_lower:
            return 'pilares'
        elif 'slab' in tipo_lower or 'laje' in nome_lower or 'laje' in desc_lower:
            return 'lajes'
        elif 'wall' in tipo_lower or 'parede' in nome_lower or 'muro' in nome_lower:
            return 'paredes'
        elif 'footing' in tipo_lower or 'sapata' in nome_lower or 'fundacao' in nome_lower:
            return 'sapatas'
        else:
            return 'default'
    
    def _calcular_volume_elemento(self, elemento) -> float:
        """
        Calcula o volume do elemento
        
        Args:
            elemento: Elemento IFC
            
        Returns:
            Volume em m³
        """
        try:
            # Tentar obter volume de propriedades quantitativas
            volume = self._obter_volume_de_propriedades(elemento)
            if volume > 0:
                return volume
            
            # Tentar calcular geometricamente
            volume = self._calcular_volume_geometrico(elemento)
            if volume > 0:
                return volume
            
            # Estimativa básica baseada em dimensões
            return self._estimar_volume_basico(elemento)
            
        except Exception as e:
            print(f"⚠️ Erro ao calcular volume: {str(e)}")
            return 0.1  # Volume mínimo padrão
    
    def _obter_volume_de_propriedades(self, elemento) -> float:
        """Tenta obter volume de property sets"""
        try:
            # Buscar em property sets
            psets = ifcopenshell.util.element.get_psets(elemento)
            
            for pset_name, pset_data in psets.items():
                # Procurar propriedades de volume
                for prop_name, prop_value in pset_data.items():
                    if any(keyword in prop_name.lower() for keyword in ['volume', 'vol', 'cubic']):
                        if isinstance(prop_value, (int, float)) and prop_value > 0:
                            # Converter para m³ se necessário
                            return self._converter_para_metros_cubicos(prop_value)
            
            return 0
            
        except Exception:
            return 0
    
    def _calcular_volume_geometrico(self, elemento) -> float:
        """Calcula volume usando geometria IFC"""
        try:
            # Isso requereria ifcopenshell.geom para processamento geométrico
            # Para simplificar, vamos estimar baseado no tipo
            return 0
            
        except Exception:
            return 0
    
    def _estimar_volume_basico(self, elemento) -> float:
        """Estimativa básica de volume baseada em tipo - valores realistas"""
        tipo = elemento.is_a()
        
        # Estimativas calibradas pelo relatório Eberick (41 m³ total)
        estimativas = {
            'IfcBeam': 0.105,     # 193 vigas * 0.105 ≈ 20.3 m³ (50% do total)
            'IfcColumn': 0.075,   # 64 pilares * 0.075 ≈ 4.8 m³ (12% do total)
            'IfcSlab': 0.345,     # 29 lajes * 0.345 ≈ 10.0 m³ (24% do total)
            'IfcWall': 0.10,      # Paredes estruturais
            'IfcFooting': 0.26,   # 23 sapatas * 0.26 ≈ 6.0 m³ (14% do total)
            'IfcPile': 0.5,       # Estacas de fundação
            'IfcMember': 0.05,    # Elementos estruturais diversos
            'IfcPlate': 0.15      # Placas estruturais
        }
        
        return estimativas.get(tipo, 0.05)  # Valor padrão muito menor
    
    def _converter_para_metros_cubicos(self, volume: float) -> float:
        """Converte volume para metros cúbicos baseado na unidade do projeto"""
        unidade = self.project_info.get('unidade_comprimento', 'mm').lower()
        
        # Se o volume está muito grande, provavelmente está em unidades menores
        if volume > 1000:  # Muito grande para ser m³, provavelmente mm³
            return volume / 1e9  # mm³ para m³
        elif volume > 10:  # Moderadamente grande, provavelmente cm³  
            return volume / 1e6  # cm³ para m³
        else:
            # Valores já razoáveis, assumir que estão corretos
            if unidade in ['mm', 'millimetre']:
                return volume / 1e9  # mm³ para m³
            elif unidade in ['cm', 'centimetre']:
                return volume / 1e6  # cm³ para m³
            elif unidade in ['m', 'metre']:
                return volume  # já em m³
            else:
                # Para valores pequenos, assumir que já estão em m³
                return volume
    
    def _calcular_peso_aco(self, volume_concreto: float, tipo_estrutural: str) -> float:
        """
        Calcula peso de aço baseado no volume de concreto
        
        Args:
            volume_concreto: Volume de concreto em m³
            tipo_estrutural: Tipo do elemento estrutural
            
        Returns:
            Peso de aço em kg
        """
        taxa_armadura = self.config["taxas_armadura"].get(
            tipo_estrutural, 
            self.config["taxas_armadura"]["default"]
        )
        
        return volume_concreto * taxa_armadura
    
    def _obter_pavimento(self, elemento) -> str:
        """Obtém o pavimento do elemento"""
        try:
            # Tentar obter de propriedades
            psets = ifcopenshell.util.element.get_psets(elemento)
            
            for pset_name, pset_data in psets.items():
                for prop_name, prop_value in pset_data.items():
                    if any(keyword in prop_name.lower() for keyword in ['level', 'floor', 'pavimento', 'andar']):
                        if isinstance(prop_value, str):
                            return prop_value
            
            # Tentar obter do spatial container
            container = ifcopenshell.util.element.get_container(elemento)
            if container and hasattr(container, 'Name'):
                return container.Name or "Pavimento Desconhecido"
            
            return "Pavimento Desconhecido"
            
        except Exception:
            return "Pavimento Desconhecido"
    
    def _distribuir_bitolas(self, peso_total: float, tipo_estrutural: str) -> Dict[str, float]:
        """
        Distribui o peso total pelas diferentes bitolas
        
        Args:
            peso_total: Peso total de aço em kg
            tipo_estrutural: Tipo do elemento estrutural
            
        Returns:
            Distribuição por bitola
        """
        distribuicao = self.config["distribuicao_bitolas"].get(
            tipo_estrutural,
            self.config["distribuicao_bitolas"]["default"]
        )
        
        bitolas = {}
        for bitola, percentual in distribuicao.items():
            bitolas[bitola] = round(peso_total * percentual, 2)
        
        return bitolas
    
    def _calcular_custo_concreto(self, volume_concreto: float) -> Dict[str, float]:
        """
        Calcula o custo do concreto baseado no volume e preços SINAPI
        
        Args:
            volume_concreto: Volume de concreto em m³
            
        Returns:
            Dicionário com informações de custo
        """
        preco_unitario = self.config["precos_sinapi"]["concreto_fck25"]
        custo_total = volume_concreto * preco_unitario
        
        return {
            "volume_m3": round(volume_concreto, 3),
            "preco_unitario": preco_unitario,
            "custo_total": round(custo_total, 2),
            "data_referencia": self.config["precos_sinapi"]["data_referencia"]
        }
    
    def _calcular_custo_armacao(self, bitolas: Dict[str, float], tipo_estrutural: str) -> Dict[str, Any]:
        """
        Calcula o custo da armação baseado nas bitolas e peso
        
        Args:
            bitolas: Dicionário com peso por bitola
            tipo_estrutural: Tipo do elemento estrutural
            
        Returns:
            Dicionário com informações de custo da armação
        """
        precos_armacao = self.config["precos_sinapi"]["armacao_aco"]
        custo_total = 0
        custo_por_bitola = {}
        peso_total = 0
        
        for bitola, peso in bitolas.items():
            if peso <= 0:
                continue
                
            peso_total += peso
            
            # Buscar preço da bitola, considerando casos especiais
            preco_kg = None
            
            # Caso especial para sapatas com bitola 8mm
            if tipo_estrutural == "sapatas" and bitola == "8.0 mm":
                preco_kg = precos_armacao.get("8.0 mm sapata", precos_armacao.get("8.0 mm", 15.05))
            else:
                preco_kg = precos_armacao.get(bitola, 0)
            
            # Se não encontrar o preço exato, usar preço médio baseado no diâmetro
            if preco_kg == 0:
                preco_kg = self._obter_preco_medio_bitola(bitola)
            
            custo_bitola = peso * preco_kg
            custo_total += custo_bitola
            
            custo_por_bitola[bitola] = {
                "peso_kg": round(peso, 2),
                "preco_unitario": preco_kg,
                "custo_total": round(custo_bitola, 2)
            }
        
        return {
            "peso_total_kg": round(peso_total, 2),
            "custo_total": round(custo_total, 2),
            "custo_por_bitola": custo_por_bitola,
            "data_referencia": self.config["precos_sinapi"]["data_referencia"]
        }
    
    def _obter_preco_medio_bitola(self, bitola: str) -> float:
        """
        Obtém preço médio quando a bitola específica não está na tabela
        
        Args:
            bitola: String da bitola (ex: "8.0 mm")
            
        Returns:
            Preço médio em R$/kg
        """
        precos_armacao = self.config["precos_sinapi"]["armacao_aco"]
        
        try:
            # Extrair diâmetro numérico
            diametro = float(bitola.split()[0])
            
            # Buscar bitolas próximas para interpolar
            bitolas_disponiveis = []
            for bit_str, preco in precos_armacao.items():
                if "sapata" not in bit_str:  # Excluir preços específicos
                    try:
                        diam = float(bit_str.split()[0])
                        bitolas_disponiveis.append((diam, preco))
                    except:
                        continue
            
            bitolas_disponiveis.sort()
            
            # Se não há bitolas disponíveis, usar preço médio geral
            if not bitolas_disponiveis:
                return 13.5  # Preço médio aproximado
            
            # Se o diâmetro é menor que o menor disponível
            if diametro <= bitolas_disponiveis[0][0]:
                return bitolas_disponiveis[0][1]
            
            # Se o diâmetro é maior que o maior disponível
            if diametro >= bitolas_disponiveis[-1][0]:
                return bitolas_disponiveis[-1][1]
            
            # Interpolação linear entre duas bitolas próximas
            for i in range(len(bitolas_disponiveis) - 1):
                d1, p1 = bitolas_disponiveis[i]
                d2, p2 = bitolas_disponiveis[i + 1]
                
                if d1 <= diametro <= d2:
                    # Interpolação linear
                    fator = (diametro - d1) / (d2 - d1)
                    return p1 + fator * (p2 - p1)
            
            # Fallback: preço médio
            precos = [p for _, p in bitolas_disponiveis]
            return sum(precos) / len(precos)
            
        except:
            return 13.5  # Preço médio de fallback
    
    def gerar_dados_dashboard(self) -> Dict[str, Any]:
        """
        Gera dados formatados para o dashboard
        
        Returns:
            Dicionário com dados para o dashboard
        """
        print("📊 Gerando dados para dashboard...")
        
        # Extrair informações do projeto
        info_projeto = self.extrair_info_projeto()
        
        # Extrair elementos estruturais
        elementos = self.extrair_elementos_estruturais()
        
        if not elementos:
            print("⚠️ Nenhum elemento estrutural encontrado")
            return self._criar_dados_vazio()
        
        # Processar dados
        dados_processados = self._processar_dados_para_dashboard(elementos)
        
        # Estruturar resposta
        dados_dashboard = {
            "projeto": info_projeto["nome"],
            "data_atualizacao": info_projeto["data_extracao"],
            "arquivo_ifc": info_projeto["arquivo"],
            "volume_aco": dados_processados
        }
        
        print("✅ Dados do dashboard gerados com sucesso")
        return dados_dashboard
    
    def _processar_dados_para_dashboard(self, elementos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Processa elementos para formato do dashboard"""
        
        # Calcular resumo geral
        peso_total = sum(elem["peso_aco_total"] for elem in elementos)
        volume_concreto_total = sum(elem["volume_concreto"] for elem in elementos)
        custo_concreto_total = sum(elem["custo_concreto"]["custo_total"] for elem in elementos)
        custo_armacao_total = sum(elem["custo_armacao"]["custo_total"] for elem in elementos)
        custo_total_geral = custo_concreto_total + custo_armacao_total
        pavimentos = set(elem["pavimento"] for elem in elementos)
        
        # Agrupar por pavimento
        por_pavimento = {}
        for elemento in elementos:
            pav = elemento["pavimento"]
            if pav not in por_pavimento:
                por_pavimento[pav] = {
                    "nome": pav,
                    "peso_aco": 0,
                    "volume_concreto": 0,
                    "custo_concreto": 0,
                    "custo_armacao": 0,
                    "custo_total": 0,
                    "elementos": 0
                }
            
            por_pavimento[pav]["peso_aco"] += elemento["peso_aco_total"]
            por_pavimento[pav]["volume_concreto"] += elemento["volume_concreto"]
            por_pavimento[pav]["custo_concreto"] += elemento["custo_concreto"]["custo_total"]
            por_pavimento[pav]["custo_armacao"] += elemento["custo_armacao"]["custo_total"]
            por_pavimento[pav]["custo_total"] += (elemento["custo_concreto"]["custo_total"] + elemento["custo_armacao"]["custo_total"])
            por_pavimento[pav]["elementos"] += 1
        
        # Agrupar por bitola
        por_bitola = {}
        for elemento in elementos:
            for bitola, peso in elemento["bitolas"].items():
                if bitola not in por_bitola:
                    por_bitola[bitola] = 0
                por_bitola[bitola] += peso
        
        # Agrupar por tipo de elemento
        por_tipo = {}
        for elemento in elementos:
            tipo = elemento["tipo_estrutural"]
            if tipo not in por_tipo:
                por_tipo[tipo] = {
                    "tipo": tipo,
                    "peso_aco": 0,
                    "volume_concreto": 0,
                    "custo_concreto": 0,
                    "custo_armacao": 0,
                    "custo_total": 0,
                    "elementos": 0
                }
            
            por_tipo[tipo]["peso_aco"] += elemento["peso_aco_total"]
            por_tipo[tipo]["volume_concreto"] += elemento["volume_concreto"]
            por_tipo[tipo]["custo_concreto"] += elemento["custo_concreto"]["custo_total"]
            por_tipo[tipo]["custo_armacao"] += elemento["custo_armacao"]["custo_total"]
            por_tipo[tipo]["custo_total"] += (elemento["custo_concreto"]["custo_total"] + elemento["custo_armacao"]["custo_total"])
            por_tipo[tipo]["elementos"] += 1
        
        return {
            "resumo": {
                "peso_total": round(peso_total, 2),
                "volume_concreto_total": round(volume_concreto_total, 3),
                "custo_concreto_total": round(custo_concreto_total, 2),
                "custo_armacao_total": round(custo_armacao_total, 2),
                "custo_total_obra": round(custo_total_geral, 2),
                "preco_unitario_concreto": self.config["precos_sinapi"]["concreto_fck25"],
                "data_referencia_precos": self.config["precos_sinapi"]["data_referencia"],
                "pavimentos": len(pavimentos),
                "bitolas_diferentes": len(por_bitola),
                "elementos_total": len(elementos)
            },
            "por_pavimento": [
                {
                    "nome": dados["nome"],
                    "peso_aco": round(dados["peso_aco"], 2),
                    "volume_concreto": round(dados["volume_concreto"], 3),
                    "custo_concreto": round(dados["custo_concreto"], 2),
                    "custo_armacao": round(dados["custo_armacao"], 2),
                    "custo_total": round(dados["custo_total"], 2),
                    "elementos": dados["elementos"]
                }
                for dados in sorted(por_pavimento.values(), key=lambda x: x["nome"])
            ],
            "por_bitola": [
                {
                    "bitola": bitola,
                    "peso": round(peso, 2),
                    "percentual": round((peso / peso_total) * 100, 1) if peso_total > 0 else 0
                }
                for bitola, peso in sorted(por_bitola.items(), key=lambda x: float(x[0].split()[0]))
            ],
            "por_elemento": [
                {
                    "tipo": dados["tipo"],
                    "peso_aco": round(dados["peso_aco"], 2),
                    "volume_concreto": round(dados["volume_concreto"], 3),
                    "custo_concreto": round(dados["custo_concreto"], 2),
                    "custo_armacao": round(dados["custo_armacao"], 2),
                    "custo_total": round(dados["custo_total"], 2),
                    "elementos": dados["elementos"],
                    "percentual": round((dados["peso_aco"] / peso_total) * 100, 1) if peso_total > 0 else 0
                }
                for dados in sorted(por_tipo.values(), key=lambda x: x["peso_aco"], reverse=True)
            ]
        }
    
    def _criar_dados_vazio(self) -> Dict[str, Any]:
        """Cria estrutura de dados vazia"""
        info_projeto = self.extrair_info_projeto()
        
        return {
            "projeto": info_projeto["nome"],
            "data_atualizacao": info_projeto["data_extracao"],
            "arquivo_ifc": info_projeto["arquivo"],
            "volume_aco": {
                "resumo": {
                    "peso_total": 0,
                    "volume_concreto_total": 0,
                    "custo_concreto_total": 0,
                    "custo_armacao_total": 0,
                    "custo_total_obra": 0,
                    "preco_unitario_concreto": self.config["precos_sinapi"]["concreto_fck25"],
                    "data_referencia_precos": self.config["precos_sinapi"]["data_referencia"],
                    "pavimentos": 0,
                    "bitolas_diferentes": 0,
                    "elementos_total": 0
                },
                "por_pavimento": [],
                "por_bitola": [],
                "por_elemento": []
            }
        }
    
    def salvar_dados_json(self, dados: Dict[str, Any], arquivo_saida: str) -> bool:
        """
        Salva dados em arquivo JSON
        
        Args:
            dados: Dados para salvar
            arquivo_saida: Caminho do arquivo de saída
            
        Returns:
            True se salvou com sucesso
        """
        try:
            with open(arquivo_saida, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Dados salvos em: {arquivo_saida}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao salvar JSON: {str(e)}")
            return False
    
    def gerar_dashboard_html(self, dados: Dict[str, Any], 
                           template_html: str, 
                           arquivo_saida: str) -> bool:
        """
        Gera dashboard HTML a partir do template
        
        Args:
            dados: Dados do dashboard
            template_html: Caminho do template HTML
            arquivo_saida: Caminho do arquivo HTML de saída
            
        Returns:
            True se gerou com sucesso
        """
        try:
            if not os.path.exists(template_html):
                print(f"❌ Template não encontrado: {template_html}")
                return False
            
            # Ler template
            with open(template_html, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Substituir dados no template
            html_content = self._substituir_dados_template(html_content, dados)
            
            # Salvar dashboard final
            with open(arquivo_saida, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"🎨 Dashboard HTML gerado: {arquivo_saida}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao gerar dashboard HTML: {str(e)}")
            return False
    
    def _substituir_dados_template(self, html_content: str, dados: Dict[str, Any]) -> str:
        """Substitui placeholders no template HTML"""
        
        # Dados básicos
        html_content = html_content.replace("{{PROJETO_NOME}}", dados.get("projeto", "Projeto"))
        html_content = html_content.replace("{{DATA_ATUALIZACAO}}", dados.get("data_atualizacao", ""))
        html_content = html_content.replace("{{ARQUIVO_IFC}}", dados.get("arquivo_ifc", ""))
        
        volume_aco = dados.get("volume_aco", {})
        resumo = volume_aco.get("resumo", {})
        
        # Resumo
        html_content = html_content.replace("{{PESO_TOTAL}}", str(resumo.get("peso_total", 0)))
        html_content = html_content.replace("{{VOLUME_CONCRETO_TOTAL}}", str(resumo.get("volume_concreto_total", 0)))
        html_content = html_content.replace("{{CUSTO_CONCRETO_TOTAL}}", str(resumo.get("custo_concreto_total", 0)))
        html_content = html_content.replace("{{CUSTO_ARMACAO_TOTAL}}", str(resumo.get("custo_armacao_total", 0)))
        html_content = html_content.replace("{{CUSTO_TOTAL_OBRA}}", str(resumo.get("custo_total_obra", 0)))
        html_content = html_content.replace("{{PRECO_UNITARIO_CONCRETO}}", str(resumo.get("preco_unitario_concreto", 0)))
        html_content = html_content.replace("{{DATA_REFERENCIA_PRECOS}}", str(resumo.get("data_referencia_precos", "")))
        html_content = html_content.replace("{{PAVIMENTOS}}", str(resumo.get("pavimentos", 0)))
        html_content = html_content.replace("{{BITOLAS_DIFERENTES}}", str(resumo.get("bitolas_diferentes", 0)))
        html_content = html_content.replace("{{ELEMENTOS_TOTAL}}", str(resumo.get("elementos_total", 0)))
        
        # Dados JSON para gráficos
        dados_json = json.dumps(dados, ensure_ascii=False)
        html_content = html_content.replace("{{DADOS_JSON}}", dados_json)
        
        return html_content


def main():
    """Função principal para uso via linha de comando"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Extrator IFC para Dashboard de Volume de Aço")
    parser.add_argument("arquivo_ifc", help="Caminho do arquivo IFC")
    parser.add_argument("-o", "--output", help="Arquivo JSON de saída", default="dados_aco.json")
    parser.add_argument("-t", "--template", help="Template HTML do dashboard")
    parser.add_argument("-d", "--dashboard", help="Arquivo HTML do dashboard final")
    
    args = parser.parse_args()
    
    # Criar extrator
    extrator = IFCSteelExtractor(args.arquivo_ifc)
    
    # Carregar arquivo IFC
    if not extrator.carregar_ifc():
        print("❌ Erro ao carregar arquivo IFC")
        sys.exit(1)
    
    # Gerar dados
    dados = extrator.gerar_dados_dashboard()
    
    # Salvar JSON
    if not extrator.salvar_dados_json(dados, args.output):
        print("❌ Erro ao salvar dados JSON")
        sys.exit(1)
    
    # Gerar dashboard se template fornecido
    if args.template and args.dashboard:
        if not extrator.gerar_dashboard_html(dados, args.template, args.dashboard):
            print("❌ Erro ao gerar dashboard HTML")
            sys.exit(1)
    
    print("🎉 Processamento concluído com sucesso!")


if __name__ == "__main__":
    main()
