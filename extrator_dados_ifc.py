#!/usr/bin/env python3
"""
Extrator de Dados IFC para Vila Andriw
Utiliza ifcopenshell para extrair informações estruturais do arquivo VilaAndriw.ifc
e gerar dados em CSV e JSON para alimentar o dashboard
"""

import ifcopenshell
import json
import csv
import os
from collections import defaultdict
from datetime import datetime

class ExtratorVilaAndriw:
    def __init__(self, arquivo_ifc="VilaAndriw.ifc"):
        """
        Inicializa o extrator com o arquivo IFC
        """
        self.arquivo_ifc = arquivo_ifc
        self.modelo = None
        self.dados_extraidos = {
            "projeto": "Vila Andriw",
            "data_extracao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "arquivo_ifc": arquivo_ifc,
            "resumo": {},
            "por_pavimento": [],
            "por_elemento": [],
            "detalhamento": []
        }
        
    def carregar_modelo(self):
        """
        Carrega o modelo IFC
        """
        try:
            if not os.path.exists(self.arquivo_ifc):
                raise FileNotFoundError(f"Arquivo {self.arquivo_ifc} não encontrado")
                
            print(f"🔄 Carregando modelo IFC: {self.arquivo_ifc}")
            self.modelo = ifcopenshell.open(self.arquivo_ifc)
            print(f"✅ Modelo carregado com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao carregar modelo: {e}")
            return False
    
    def extrair_elementos_estruturais(self):
        """
        Extrai elementos estruturais do modelo
        """
        if not self.modelo:
            print("❌ Modelo não carregado")
            return {}
            
        elementos = {
            "vigas": [],
            "pilares": [],
            "lajes": [],
            "sapatas": [],
            "fundacoes": []
        }
        
        try:
            # Vigas
            vigas = self.modelo.by_type("IfcBeam")
            for viga in vigas:
                elementos["vigas"].append(self.extrair_dados_elemento(viga))
            
            # Pilares
            pilares = self.modelo.by_type("IfcColumn")
            for pilar in pilares:
                elementos["pilares"].append(self.extrair_dados_elemento(pilar))
                
            # Lajes
            lajes = self.modelo.by_type("IfcSlab")
            for laje in lajes:
                elementos["lajes"].append(self.extrair_dados_elemento(laje))
                
            # Fundações
            fundacoes = self.modelo.by_type("IfcFooting")
            for fundacao in fundacoes:
                elementos["fundacoes"].append(self.extrair_dados_elemento(fundacao))
                
            print(f"📊 Elementos extraídos:")
            print(f"   - Vigas: {len(elementos['vigas'])}")
            print(f"   - Pilares: {len(elementos['pilares'])}")
            print(f"   - Lajes: {len(elementos['lajes'])}")
            print(f"   - Fundações: {len(elementos['fundacoes'])}")
            
            return elementos
            
        except Exception as e:
            print(f"❌ Erro ao extrair elementos: {e}")
            return {}
    
    def extrair_dados_elemento(self, elemento):
        """
        Extrai dados específicos de um elemento
        """
        dados = {
            "id": elemento.GlobalId if hasattr(elemento, 'GlobalId') else 'N/A',
            "nome": elemento.Name if hasattr(elemento, 'Name') else 'Sem nome',
            "tipo": elemento.is_a(),
            "materiais": [],
            "dimensoes": {},
            "volume": 0,
            "pavimento": self.identificar_pavimento(elemento)
        }
        
        try:
            # Extrai propriedades de quantidade
            for relacao in elemento.IsDefinedBy:
                if relacao.is_a("IfcRelDefinesByProperties"):
                    prop_set = relacao.RelatingPropertyDefinition
                    if prop_set.is_a("IfcElementQuantity"):
                        for quantidade in prop_set.Quantities:
                            if quantidade.is_a("IfcQuantityVolume"):
                                dados["volume"] = quantidade.VolumeValue
                            elif quantidade.is_a("IfcQuantityLength"):
                                dados["dimensoes"]["comprimento"] = quantidade.LengthValue
                            elif quantidade.is_a("IfcQuantityArea"):
                                dados["dimensoes"]["area"] = quantidade.AreaValue
            
            # Extrai materiais
            if hasattr(elemento, 'HasAssociations'):
                for associacao in elemento.HasAssociations:
                    if associacao.is_a("IfcRelAssociatesMaterial"):
                        material = associacao.RelatingMaterial
                        if material.is_a("IfcMaterial"):
                            dados["materiais"].append(material.Name)
                            
        except Exception as e:
            print(f"⚠️ Erro ao extrair propriedades do elemento {dados['id']}: {e}")
        
        return dados
    
    def identificar_pavimento(self, elemento):
        """
        Identifica o pavimento do elemento baseado na altura/localização
        """
        try:
            if hasattr(elemento, 'ObjectPlacement'):
                # Implementação simplificada - baseada na coordenada Z
                # Em um caso real, seria mais complexo analisando o IfcBuildingStorey
                return "Térreo"  # Placeholder
        except:
            pass
        return "Não identificado"
    
    def calcular_volumes_concreto(self, elementos):
        """
        Calcula volumes de concreto por elemento e pavimento
        """
        volumes = defaultdict(lambda: defaultdict(float))
        
        for tipo, lista_elementos in elementos.items():
            for elemento in lista_elementos:
                pavimento = elemento.get('pavimento', 'Não identificado')
                volume = elemento.get('volume', 0)
                volumes[pavimento][tipo] += volume
                
        return dict(volumes)
    
    def estimar_custos(self, volumes):
        """
        Estima custos baseado nos volumes e tabela SINAPI
        """
        # Preços SINAPI 07/2025 (valores de referência)
        precos = {
            "concreto_fck25": 740.54,  # R$/m³
            "armacao_ca50_8mm": 15.05,  # R$/kg
            "armacao_ca50_10mm": 13.45,  # R$/kg
            "armacao_ca50_12_5mm": 11.33,  # R$/kg
            "forma_madeira": 93.02,  # R$/m²
        }
        
        custos = defaultdict(dict)
        
        for pavimento, tipos in volumes.items():
            custo_pavimento = 0
            for tipo, volume in tipos.items():
                # Estimativa simplificada de custo por m³ de concreto
                custo_concreto = volume * precos["concreto_fck25"]
                # Estimativa de armação (kg/m³ varia por elemento)
                kg_aco_por_m3 = {"vigas": 120, "pilares": 150, "lajes": 80, "fundacoes": 100}.get(tipo, 100)
                kg_aco = volume * kg_aco_por_m3
                custo_armacao = kg_aco * precos["armacao_ca50_8mm"]  # Usando preço médio
                
                custo_total = custo_concreto + custo_armacao
                custo_pavimento += custo_total
                
                custos[pavimento][tipo] = {
                    "volume": volume,
                    "kg_aco": kg_aco,
                    "custo_concreto": custo_concreto,
                    "custo_armacao": custo_armacao,
                    "custo_total": custo_total
                }
            
            custos[pavimento]["total"] = custo_pavimento
            
        return dict(custos)
    
    def processar_modelo_completo(self):
        """
        Executa extração completa do modelo
        """
        if not self.carregar_modelo():
            return False
            
        print("🔄 Extraindo elementos estruturais...")
        elementos = self.extrair_elementos_estruturais()
        
        if not elementos:
            print("❌ Nenhum elemento extraído")
            return False
            
        print("🔄 Calculando volumes e custos...")
        volumes = self.calcular_volumes_concreto(elementos)
        custos = self.estimar_custos(volumes)
        
        # Monta dados finais
        self.dados_extraidos["resumo"] = {
            "total_elementos": sum(len(lista) for lista in elementos.values()),
            "total_volume_concreto": sum(
                sum(tipos.values()) for tipos in volumes.values()
            ),
            "total_custo_estimado": sum(
                pav.get("total", 0) for pav in custos.values()
            )
        }
        
        # Por pavimento
        for pavimento in volumes:
            if pavimento != "Não identificado":
                self.dados_extraidos["por_pavimento"].append({
                    "nome": pavimento,
                    "volume_total": sum(volumes[pavimento].values()),
                    "custo_total": custos[pavimento].get("total", 0),
                    "elementos": volumes[pavimento]
                })
        
        # Por elemento
        for tipo in ["vigas", "pilares", "lajes", "fundacoes"]:
            volume_total = sum(
                volumes[pav].get(tipo, 0) for pav in volumes
            )
            if volume_total > 0:
                self.dados_extraidos["por_elemento"].append({
                    "tipo": tipo,
                    "volume_total": volume_total,
                    "quantidade": len(elementos.get(tipo, [])),
                    "custo_estimado": sum(
                        custos[pav].get(tipo, {}).get("custo_total", 0) 
                        for pav in custos
                    )
                })
        
        print("✅ Extração completa finalizada!")
        return True
    
    def salvar_dados(self, formato="ambos"):
        """
        Salva dados extraídos em JSON e/ou CSV
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if formato in ["json", "ambos"]:
            arquivo_json = f"dados_vila_andriw_extraidos_{timestamp}.json"
            with open(arquivo_json, 'w', encoding='utf-8') as f:
                json.dump(self.dados_extraidos, f, ensure_ascii=False, indent=2)
            print(f"💾 Dados salvos em: {arquivo_json}")
        
        if formato in ["csv", "ambos"]:
            arquivo_csv = f"dados_vila_andriw_extraidos_{timestamp}.csv"
            with open(arquivo_csv, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Cabeçalho
                writer.writerow([
                    "Pavimento", "Elemento", "Volume_m3", "Quantidade", 
                    "Custo_Estimado", "Observacoes"
                ])
                
                # Dados por elemento
                for elemento in self.dados_extraidos["por_elemento"]:
                    writer.writerow([
                        "Geral",
                        elemento["tipo"].title(),
                        round(elemento["volume_total"], 2),
                        elemento["quantidade"],
                        f"R$ {elemento['custo_estimado']:,.2f}",
                        "Estimativa baseada em extração IFC"
                    ])
                    
            print(f"💾 Dados CSV salvos em: {arquivo_csv}")
    
    def gerar_relatorio(self):
        """
        Gera relatório resumido
        """
        print("\n" + "="*60)
        print("📋 RELATÓRIO VILA ANDRIW - EXTRAÇÃO IFC")
        print("="*60)
        
        resumo = self.dados_extraidos["resumo"]
        print(f"🏗️ Total de Elementos: {resumo.get('total_elementos', 0)}")
        print(f"🧱 Volume Total Concreto: {resumo.get('total_volume_concreto', 0):.2f} m³")
        print(f"💰 Custo Total Estimado: R$ {resumo.get('total_custo_estimado', 0):,.2f}")
        
        print("\n📊 Por Pavimento:")
        for pav in self.dados_extraidos["por_pavimento"]:
            print(f"   - {pav['nome']}: {pav['volume_total']:.2f} m³ - R$ {pav['custo_total']:,.2f}")
        
        print("\n🔧 Por Elemento:")
        for elem in self.dados_extraidos["por_elemento"]:
            print(f"   - {elem['tipo'].title()}: {elem['quantidade']} unidades, {elem['volume_total']:.2f} m³")
        
        print("="*60)

def main():
    """
    Função principal
    """
    print("🚀 Extrator de Dados IFC - Vila Andriw")
    print("Utilizando ifcopenshell para análise estrutural\n")
    
    extrator = ExtratorVilaAndriw("VilaAndriw.ifc")
    
    if extrator.processar_modelo_completo():
        extrator.gerar_relatorio()
        
        # Pergunta sobre salvamento
        salvar = input("\n💾 Deseja salvar os dados extraídos? (s/n): ").lower().strip()
        if salvar in ['s', 'sim', 'y', 'yes']:
            formato = input("Formato (json/csv/ambos): ").lower().strip()
            if formato not in ['json', 'csv', 'ambos']:
                formato = 'ambos'
            extrator.salvar_dados(formato)
        
        print("\n✅ Processo concluído!")
        print("Os dados podem ser utilizados para alimentar o dashboard HTML.")
        
    else:
        print("❌ Falha na extração. Verifique se o arquivo VilaAndriw.ifc existe.")

if __name__ == "__main__":
    main()
