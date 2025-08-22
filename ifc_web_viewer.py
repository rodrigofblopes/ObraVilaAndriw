#!/usr/bin/env python3
"""
Visualizador Web IFC com Three.js
Integra ifcopenshell com three.js para renderização 3D no navegador
"""

import os
import json
import base64
import tempfile
import streamlit as st
import streamlit.components.v1 as components

try:
    import ifcopenshell
    import ifcopenshell.geom
    HAS_IFCOPENSHELL = True
except ImportError:
    HAS_IFCOPENSHELL = False

class IFCWebViewer:
    """Conversor IFC para visualização web com Three.js"""
    
    def __init__(self):
        self.viewer_html = None
        self.geometry_data = None
    
    def load_ifc_file(self, ifc_path):
        """Carrega arquivo IFC e extrai geometria para web"""
        if not HAS_IFCOPENSHELL:
            return self._generate_fallback_data()
        
        try:
            # Carregar arquivo IFC
            ifc_file = ifcopenshell.open(ifc_path)
            
            # Configurar settings para melhor performance web
            settings = ifcopenshell.geom.settings()
            settings.set('use-world-coords', True)
            settings.set('weld-vertices', True)
            settings.set('validate', False)  # Acelerar processamento
            
            # Extrair elementos estruturais
            geometry_data = {
                'elements': [],
                'materials': {},
                'project_info': {
                    'name': 'Vila Andriw',
                    'description': 'Projeto Estrutural'
                }
            }
            
            # Buscar elementos estruturais principais
            structural_elements = (
                ifc_file.by_type("IfcBeam") +      # Vigas
                ifc_file.by_type("IfcColumn") +    # Pilares  
                ifc_file.by_type("IfcSlab") +      # Lajes
                ifc_file.by_type("IfcWall") +      # Paredes
                ifc_file.by_type("IfcFooting")     # Fundações
            )
            
            print(f"🔍 Processando {len(structural_elements)} elementos...")
            
            # Configurar cores por tipo
            element_colors = {
                'IfcBeam': {'r': 0.8, 'g': 0.4, 'b': 0.0},     # Laranja - Vigas
                'IfcColumn': {'r': 0.8, 'g': 0.0, 'b': 0.0},   # Vermelho - Pilares
                'IfcSlab': {'r': 0.0, 'g': 0.6, 'b': 0.8},     # Azul - Lajes
                'IfcWall': {'r': 0.6, 'g': 0.6, 'b': 0.6},     # Cinza - Paredes
                'IfcFooting': {'r': 0.4, 'g': 0.2, 'b': 0.0}   # Marrom - Fundações
            }
            
            # Processar cada elemento (todos os elementos)
            processed_count = 0
            for i, element in enumerate(structural_elements):  # Processar todos os elementos
                # Mostrar progresso a cada 50 elementos
                if i % 50 == 0:
                    print(f"📊 Processando elemento {i+1} de {len(structural_elements)}...")
                try:
                    # Criar geometria do elemento
                    shape = ifcopenshell.geom.create_shape(settings, element)
                    geometry = shape.geometry
                    
                    if hasattr(geometry, 'verts') and hasattr(geometry, 'faces'):
                        # Extrair vértices e faces
                        vertices = geometry.verts
                        faces = geometry.faces
                        
                        if len(vertices) >= 9 and len(faces) >= 3:
                            element_type = element.is_a()
                            color = element_colors.get(element_type, {'r': 0.5, 'g': 0.5, 'b': 0.5})
                            
                            # Adicionar elemento à estrutura de dados
                            geometry_data['elements'].append({
                                'id': f"element_{i}",
                                'name': getattr(element, 'Name', f"{element_type}_{i}") or f"{element_type}_{i}",
                                'type': element_type,
                                'vertices': list(vertices),
                                'faces': list(faces),
                                'color': color,
                                'visible': True
                            })
                            processed_count += 1
                            
                except Exception as e:
                    print(f"⚠️ Erro ao processar elemento {i}: {e}")
                    continue
            
            self.geometry_data = geometry_data
            print(f"✅ {processed_count} de {len(structural_elements)} elementos processados com sucesso!")
            return geometry_data
            
        except Exception as e:
            print(f"❌ Erro ao carregar IFC: {e}")
            return self._generate_fallback_data()
    
    def _generate_fallback_data(self):
        """Gera dados de fallback quando IFC real não pode ser carregado"""
        print("📐 Gerando modelo esquemático...")
        
        return {
            'elements': [
                # Fundações
                {
                    'id': 'foundation_1',
                    'name': 'Fundação Base',
                    'type': 'IfcFooting',
                    'vertices': [
                        -5, -3, -1.5,  5, -3, -1.5,  5,  3, -1.5, -5,  3, -1.5,  # Base inferior
                        -5, -3, -1.0,  5, -3, -1.0,  5,  3, -1.0, -5,  3, -1.0   # Base superior
                    ],
                    'faces': [0,1,2, 0,2,3, 4,7,6, 4,6,5, 0,4,5, 0,5,1, 1,5,6, 1,6,2, 2,6,7, 2,7,3, 3,7,4, 3,4,0],
                    'color': {'r': 0.4, 'g': 0.2, 'b': 0.0},
                    'visible': True
                },
                # Pilares
                {
                    'id': 'column_1',
                    'name': 'Pilar P1',
                    'type': 'IfcColumn',
                    'vertices': [
                        -4, -2, -1.5, -3.5, -2, -1.5, -3.5, -1.5, -1.5, -4, -1.5, -1.5,
                        -4, -2,  3, -3.5, -2,  3, -3.5, -1.5,  3, -4, -1.5,  3
                    ],
                    'faces': [0,1,2, 0,2,3, 4,7,6, 4,6,5, 0,4,5, 0,5,1, 1,5,6, 1,6,2, 2,6,7, 2,7,3, 3,7,4, 3,4,0],
                    'color': {'r': 0.8, 'g': 0.0, 'b': 0.0},
                    'visible': True
                },
                # Vigas
                {
                    'id': 'beam_1',
                    'name': 'Viga V1',
                    'type': 'IfcBeam',
                    'vertices': [
                        -4, -2, 0, 4, -2, 0, 4, -1.8, 0, -4, -1.8, 0,
                        -4, -2, 0.3, 4, -2, 0.3, 4, -1.8, 0.3, -4, -1.8, 0.3
                    ],
                    'faces': [0,1,2, 0,2,3, 4,7,6, 4,6,5, 0,4,5, 0,5,1, 1,5,6, 1,6,2, 2,6,7, 2,7,3, 3,7,4, 3,4,0],
                    'color': {'r': 0.8, 'g': 0.4, 'b': 0.0},
                    'visible': True
                },
                # Laje
                {
                    'id': 'slab_1',
                    'name': 'Laje L1',
                    'type': 'IfcSlab',
                    'vertices': [
                        -4, -2, 0, 4, -2, 0, 4, 2, 0, -4, 2, 0,
                        -4, -2, 0.15, 4, -2, 0.15, 4, 2, 0.15, -4, 2, 0.15
                    ],
                    'faces': [0,1,2, 0,2,3, 4,7,6, 4,6,5, 0,4,5, 0,5,1, 1,5,6, 1,6,2, 2,6,7, 2,7,3, 3,7,4, 3,4,0],
                    'color': {'r': 0.0, 'g': 0.6, 'b': 0.8},
                    'visible': True
                }
            ],
            'materials': {},
            'project_info': {
                'name': 'Vila Andriw (Esquemático)',
                'description': 'Modelo 3D esquemático - ifcopenshell não disponível'
            }
        }
    
    def generate_threejs_viewer(self, geometry_data, height=600):
        """Gera visualizador Three.js embarcado"""
        
        # Converter dados para JSON
        geometry_json = json.dumps(geometry_data, indent=2)
        
        html_content = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visualizador 3D - Vila Andriw</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #0a0a0a, #1a1a1a);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: white;
        }}
        
        #container {{
            position: relative;
            width: 100%;
            height: {height}px;
        }}
        
        #viewer {{
            width: 100%;
            height: 100%;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 8px 32px rgba(25, 118, 210, 0.15);
        }}
        
        #controls {{
            position: absolute;
            top: 10px;
            left: 10px;
            background: rgba(0, 0, 0, 0.8);
            padding: 15px;
            border-radius: 10px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(25, 118, 210, 0.3);
            z-index: 100;
        }}
        
        .control-group {{
            margin-bottom: 10px;
        }}
        
        .control-group label {{
            display: block;
            font-size: 12px;
            margin-bottom: 5px;
            color: #b0b0b0;
        }}
        
        button {{
            background: linear-gradient(135deg, #1976d2, #42a5f5);
            color: white;
            border: none;
            padding: 8px 12px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 11px;
            margin: 2px;
            transition: all 0.2s ease;
        }}
        
        button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(25, 118, 210, 0.3);
        }}
        
        select {{
            background: rgba(255, 255, 255, 0.1);
            color: white;
            border: 1px solid rgba(25, 118, 210, 0.3);
            padding: 5px;
            border-radius: 4px;
            font-size: 11px;
        }}
        
        #info {{
            position: absolute;
            bottom: 10px;
            left: 10px;
            background: rgba(0, 0, 0, 0.8);
            padding: 10px;
            border-radius: 8px;
            font-size: 11px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(25, 118, 210, 0.3);
        }}
        
        .status {{
            color: #4caf50;
            font-weight: 600;
        }}
        
        .loading {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            z-index: 50;
        }}
        
        @media (max-width: 768px) {{
            #controls {{
                font-size: 10px;
                padding: 10px;
            }}
            
            button {{
                padding: 6px 10px;
                font-size: 10px;
            }}
        }}
    </style>
</head>
<body>
    <div id="container">
        <div id="loading" class="loading">
            <h3>🔄 Carregando Modelo 3D...</h3>
            <p>Processando geometria do Vila Andriw</p>
        </div>
        
        <div id="viewer"></div>
        
        <div id="controls">
            <div class="control-group">
                <label>🎮 Visualização</label>
                <button onclick="resetCamera()">📍 Reset</button>
                <button onclick="toggleWireframe()">🔗 Wireframe</button>
                <button onclick="fitToView()">🔍 Ajustar</button>
            </div>
            
            <div class="control-group">
                <label>🏗️ Elementos</label>
                <select id="elementFilter" onchange="filterElements()">
                    <option value="all">Todos</option>
                    <option value="IfcBeam">Vigas</option>
                    <option value="IfcColumn">Pilares</option>
                    <option value="IfcSlab">Lajes</option>
                    <option value="IfcFooting">Fundações</option>
                </select>
            </div>
            
            <div class="control-group">
                <label>🌟 Qualidade</label>
                <button onclick="setQuality('low')">Baixa</button>
                <button onclick="setQuality('high')">Alta</button>
            </div>
        </div>
        
        <div id="info">
            <div class="status">✅ Modelo Carregado</div>
            <div id="elementCount">Elementos: 0</div>
            <div>🏗️ Vila Andriw - Projeto Estrutural</div>
        </div>
    </div>

    <!-- Three.js CDN -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>

    <script>
        // Dados de geometria vindos do Python
        const geometryData = {geometry_json};
        
        // Variáveis globais Three.js
        let scene, camera, renderer, controls;
        let elements = [];
        let wireframe = false;
        
        // Inicializar visualizador
        function init() {{
            console.log('🚀 Inicializando visualizador 3D...');
            
            // Configurar cena
            scene = new THREE.Scene();
            scene.background = new THREE.Color(0x0a0a0a);
            
            // Configurar câmera
            const container = document.getElementById('viewer');
            camera = new THREE.PerspectiveCamera(
                75, 
                container.clientWidth / container.clientHeight, 
                0.1, 
                1000
            );
            camera.position.set(15, 15, 15);
            
            // Configurar renderizador
            renderer = new THREE.WebGLRenderer({{ antialias: true }});
            renderer.setSize(container.clientWidth, container.clientHeight);
            renderer.shadowMap.enabled = true;
            renderer.shadowMap.type = THREE.PCFSoftShadowMap;
            container.appendChild(renderer.domElement);
            
            // Configurar controles
            controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            controls.dampingFactor = 0.05;
            
            // Adicionar iluminação
            addLights();
            
            // Carregar geometria
            loadGeometry();
            
            // Configurar responsividade
            window.addEventListener('resize', onWindowResize);
            
            // Esconder loading
            document.getElementById('loading').style.display = 'none';
            
            // Iniciar loop de renderização
            animate();
            
            console.log('✅ Visualizador inicializado!');
        }}
        
        function addLights() {{
            // Luz ambiente
            const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
            scene.add(ambientLight);
            
            // Luz direcional principal
            const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
            directionalLight.position.set(50, 50, 50);
            directionalLight.castShadow = true;
            directionalLight.shadow.mapSize.width = 2048;
            directionalLight.shadow.mapSize.height = 2048;
            scene.add(directionalLight);
            
            // Luz de preenchimento
            const fillLight = new THREE.DirectionalLight(0x42a5f5, 0.3);
            fillLight.position.set(-50, 25, -50);
            scene.add(fillLight);
        }}
        
        function loadGeometry() {{
            console.log('📐 Carregando geometria...', geometryData);
            
            const elementCount = geometryData.elements.length;
            document.getElementById('elementCount').textContent = `Elementos: ${{elementCount}}`;
            
            geometryData.elements.forEach((elementData, index) => {{
                createMeshFromData(elementData, index);
            }});
            
            // Ajustar câmera para visualizar todos os elementos
            fitToView();
        }}
        
        function createMeshFromData(elementData, index) {{
            try {{
                const vertices = new Float32Array(elementData.vertices);
                const faces = new Uint16Array(elementData.faces);
                
                const geometry = new THREE.BufferGeometry();
                geometry.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
                geometry.setIndex(new THREE.BufferAttribute(faces, 1));
                geometry.computeVertexNormals();
                
                const color = new THREE.Color(
                    elementData.color.r,
                    elementData.color.g,
                    elementData.color.b
                );
                
                const material = new THREE.MeshLambertMaterial({{
                    color: color,
                    transparent: true,
                    opacity: 0.9
                }});
                
                const mesh = new THREE.Mesh(geometry, material);
                mesh.castShadow = true;
                mesh.receiveShadow = true;
                mesh.userData = {{
                    id: elementData.id,
                    name: elementData.name,
                    type: elementData.type,
                    originalMaterial: material
                }};
                
                scene.add(mesh);
                elements.push(mesh);
                
            }} catch (error) {{
                console.warn(`⚠️ Erro ao criar mesh para elemento ${{index}}:`, error);
            }}
        }}
        
        function resetCamera() {{
            camera.position.set(15, 15, 15);
            controls.reset();
        }}
        
        function toggleWireframe() {{
            wireframe = !wireframe;
            elements.forEach(mesh => {{
                mesh.material.wireframe = wireframe;
            }});
        }}
        
        function fitToView() {{
            if (elements.length === 0) return;
            
            const box = new THREE.Box3();
            elements.forEach(mesh => {{
                box.expandByObject(mesh);
            }});
            
            const center = box.getCenter(new THREE.Vector3());
            const size = box.getSize(new THREE.Vector3());
            
            const maxDim = Math.max(size.x, size.y, size.z);
            const fov = camera.fov * (Math.PI / 180);
            const cameraDistance = maxDim / (2 * Math.tan(fov / 2));
            
            camera.position.copy(center);
            camera.position.z += cameraDistance * 1.5;
            camera.lookAt(center);
            controls.target.copy(center);
        }}
        
        function filterElements() {{
            const filter = document.getElementById('elementFilter').value;
            
            elements.forEach(mesh => {{
                if (filter === 'all' || mesh.userData.type === filter) {{
                    mesh.visible = true;
                }} else {{
                    mesh.visible = false;
                }}
            }});
        }}
        
        function setQuality(quality) {{
            if (quality === 'low') {{
                renderer.setPixelRatio(1);
                renderer.shadowMap.enabled = false;
            }} else {{
                renderer.setPixelRatio(window.devicePixelRatio);
                renderer.shadowMap.enabled = true;
            }}
        }}
        
        function onWindowResize() {{
            const container = document.getElementById('viewer');
            camera.aspect = container.clientWidth / container.clientHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(container.clientWidth, container.clientHeight);
        }}
        
        function animate() {{
            requestAnimationFrame(animate);
            controls.update();
            renderer.render(scene, camera);
        }}
        
        // Inicializar quando página carregar
        document.addEventListener('DOMContentLoaded', init);
    </script>
</body>
</html>
        """
        
        self.viewer_html = html_content
        return html_content

def create_ifc_viewer(ifc_path="VilaAndriw.ifc", height=600):
    """
    Cria visualizador IFC integrado ao Streamlit
    
    Args:
        ifc_path: Caminho para arquivo IFC
        height: Altura do visualizador em pixels
    
    Returns:
        Componente HTML para Streamlit
    """
    
    # Verificar se arquivo existe
    if not os.path.exists(ifc_path):
        st.error(f"❌ Arquivo IFC não encontrado: {ifc_path}")
        return None
    
    # Criar visualizador
    viewer = IFCWebViewer()
    
    # Carregar dados do IFC
    with st.spinner("🔄 Processando modelo IFC..."):
        geometry_data = viewer.load_ifc_file(ifc_path)
    
    if not geometry_data or len(geometry_data['elements']) == 0:
        st.warning("⚠️ Nenhum elemento geométrico encontrado no arquivo IFC")
        return None
    
    # Gerar visualizador web
    html_content = viewer.generate_threejs_viewer(geometry_data, height)
    
    # Exibir no Streamlit
    components.html(html_content, height=height + 50)
    
    # Mostrar informações
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📐 Elementos", len(geometry_data['elements']))
    with col2:
        st.metric("📁 Arquivo", os.path.basename(ifc_path))
    with col3:
        if HAS_IFCOPENSHELL:
            st.metric("🔧 Processamento", "IFC Real")
        else:
            st.metric("📋 Modo", "Esquemático")
    
    return viewer

# Função de demonstração
def demo_viewer():
    """Demonstração do visualizador IFC"""
    st.title("🏗️ Visualizador IFC - Vila Andriw")
    
    st.markdown("""
    ### 🎮 Visualizador 3D Interativo
    - **Rotação**: Clique e arraste
    - **Zoom**: Roda do mouse
    - **Pan**: Clique direito e arraste
    - **Reset**: Botão reset no painel
    """)
    
    # Tentar carregar arquivo IFC
    ifc_files = ["VilaAndriw.ifc", "ifcopenshell/VilaAndriw.ifc"]
    ifc_path = None
    
    for path in ifc_files:
        if os.path.exists(path):
            ifc_path = path
            break
    
    if ifc_path:
        create_ifc_viewer(ifc_path, height=600)
    else:
        st.error("❌ Arquivo VilaAndriw.ifc não encontrado!")
        st.info("📁 Certifique-se de que o arquivo IFC está na pasta do projeto")

if __name__ == "__main__":
    demo_viewer()
