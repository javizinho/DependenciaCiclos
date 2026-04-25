import os
import re
import json

class AnalizadorDependenciasNextJS:
    def __init__(self):
        self.raiz = os.getcwd()
        self.grafo = {}
        self.ciclos = []
        self.alias_map = self._cargar_configuracion_paths()

    def _cargar_configuracion_paths(self):
        paths_config = {}
        for nombre in ['tsconfig.json', 'jsconfig.json']:
            ruta = os.path.join(self.raiz, nombre)
            if os.path.exists(ruta):
                try:
                    with open(ruta, 'r', encoding='utf-8') as f:
                        contenido = f.read()
                        contenido_limpio = re.sub(r'//.*|/\*[\s\S]*?\*/', '', contenido)
                        data = json.loads(contenido_limpio)
                        opts = data.get('compilerOptions', {})
                        baseUrl = opts.get('baseUrl', '.')
                        paths = opts.get('paths', {})
                        for alias, destino in paths.items():
                            clave = alias.replace('*', '')
                            valor = destino[0].replace('*', '')
                            paths_config[clave] = os.path.join(baseUrl, valor)
                except Exception:
                    pass
        return paths_config

    def resolver_ruta(self, import_path, archivo_origen):
        for alias, real_path in self.alias_map.items():
            if import_path.startswith(alias):
                import_path = import_path.replace(alias, real_path)
                break
        
        if import_path.startswith('.'):
            dir_actual = os.path.dirname(archivo_origen)
            import_path = os.path.normpath(os.path.join(dir_actual, import_path))

        extensiones = ['.tsx', '.ts', '.jsx', '.js']
        for ext in extensiones:
            p1 = import_path + ext
            if os.path.exists(os.path.join(self.raiz, p1)): 
                return p1.lower()
            
            p2 = os.path.join(import_path, f'index{ext}')
            if os.path.exists(os.path.join(self.raiz, p2)): 
                return p2.lower()
        
        return import_path.lower()

    def extraer_imports(self, ruta_abs):
        importaciones = set()
        try:
            with open(ruta_abs, 'r', encoding='utf-8') as f:
                contenido = f.read()
                patrones = [
                    r'from\s+[\'"](.+?)[\'"]',
                    r'import\s+[\'"](.+?)[\'"]',
                    r'require\([\'"](.+?)[\'"]\)'
                ]
                for p in patrones:
                    for target in re.findall(p, contenido):
                        if target.startswith('.') or any(target.startswith(a) for a in self.alias_map):
                            ruta_rel_origen = os.path.relpath(ruta_abs, self.raiz)
                            resuelto = self.resolver_ruta(target, ruta_rel_origen)
                            importaciones.add(resuelto)
        except Exception:
            pass
        return list(importaciones)

    def construir_grafo(self):
        ignorar = {'.next', 'node_modules', '.git', 'public', 'dist', 'out', '.vercel'}
        for root, dirs, files in os.walk(self.raiz):
            dirs[:] = [d for d in dirs if d not in ignorar]
            for file in files:
                if file.endswith(('.js', '.jsx', '.ts', '.tsx')):
                    ruta_abs = os.path.join(root, file)
                    ruta_rel = os.path.relpath(ruta_abs, self.raiz).lower()
                    self.grafo[ruta_rel] = self.extraer_imports(ruta_abs)

    def detectar_ciclos(self):
        visitados = set()
        pila_rec = set()
        camino = []

        def dfs(u):
            visitados.add(u)
            pila_rec.add(u)
            camino.append(u)

            for v in self.grafo.get(u, []):
                if v in pila_rec:
                    idx = camino.index(v)
                    nuevo_ciclo = camino[idx:] + [v]
                    if not any(set(nuevo_ciclo) == set(c) for c in self.ciclos):
                        self.ciclos.append(nuevo_ciclo)
                elif v not in visitados and v in self.grafo:
                    dfs(v)

            pila_rec.remove(u)
            camino.pop()

        for nodo in list(self.grafo.keys()):
            if nodo not in visitados:
                dfs(nodo)

    def generar_entregables(self):
        reporte = {
            "metadata": {
                "directorio": self.raiz,
                "total_archivos": len(self.grafo),
                "total_ciclos": len(self.ciclos)
            },
            "ciclos_detectados": self.ciclos,
            "grafo_completo": self.grafo
        }
        with open('reporte_dependencias.json', 'w', encoding='utf-8') as f:
            json.dump(reporte, f, indent=4)

        nodos_criticos = set(n for c in self.ciclos for n in c)
        with open('grafo_visual.dot', 'w', encoding='utf-8') as f:
            f.write('digraph G {\n')
            f.write('  rankdir=LR; node [fontname="Arial", shape=rect, style=filled, fillcolor="#F0F0F0"];\n')
            for u, vecinos in self.grafo.items():
                u_style = 'fillcolor="#FFCCCC", color="#CC0000", penwidth=2' if u in nodos_criticos else ''
                f.write(f'  "{u}" [{u_style}];\n')
                for v in vecinos:
                    if v in self.grafo:
                        v_style = 'color="#CC0000", penwidth=2' if (u in nodos_criticos and v in nodos_criticos) else ''
                        f.write(f'  "{u}" -> "{v}" [{v_style}];\n')
            f.write('}\n')

    def ejecutar(self):
        print(f"\n" + "="*50)
        print(f"🚀 INICIANDO ANÁLISIS: {os.path.basename(self.raiz)}")
        print("="*50)
        self.construir_grafo()
        self.detectar_ciclos()
        self.generar_entregables()
        print(f"✅ Análisis completado.")
        print(f"📂 Módulos: {len(self.grafo)} | ⚠️ Ciclos: {len(self.ciclos)}")
        print("="*50 + "\n")

if __name__ == "__main__":
    AnalizadorDependenciasNextJS().ejecutar()