import sys
# Importamos las librerías para graficar
import networkx as nx
import matplotlib.pyplot as plt

class PrimSimulatorVis:
    def __init__(self, vertices):
        self.V = vertices
        # Matriz de adyacencia para el algoritmo
        self.graph = [[0 for column in range(vertices)] for row in range(vertices)]
        # Grafo de NetworkX para la visualización
        self.nx_graph = nx.Graph()

    # --- MÉTODO AUXILIAR PARA PREPARAR GRÁFICO ---
    def _setup_visual_graph(self):
        """Convierte la matriz de adyacencia a un grafo NetworkX para poder dibujarlo"""
        self.nx_graph.clear()
        # Añadir nodos
        self.nx_graph.add_nodes_from(range(self.V))
        # Añadir aristas con pesos desde la matriz
        for i in range(self.V):
            for j in range(i + 1, self.V): # Iteramos el triángulo superior para no duplicar aristas
                if self.graph[i][j] > 0:
                    self.nx_graph.add_edge(i, j, weight=self.graph[i][j])

    # --- MÉTODO DE VISUALIZACIÓN Y RESULTADOS ---
    def show_results(self, parent):
        # 1. Imprimir resultado en consola (Texto)
        print("\n" + "="*40)
        print("RESULTADO FINAL: Árbol de Expansión Mínima")
        print("="*40)
        print(f"{'Arista (U - V)':<15} {'Peso':<10}")
        total_weight = 0
        mst_edges_list = [] # Lista para guardar las aristas del resultado final
        for i in range(1, self.V):
            # parent[i] es el nodo U, i es el nodo V
            u, v = parent[i], i
            weight = self.graph[u][v]
            print(f"   {u} - {v} \t\t  {weight}")
            total_weight += weight
            mst_edges_list.append((u, v))
        print(f"\nCosto Total del Árbol Mínimo: {total_weight}")
        print("="*40)
        print("Generando visualización gráfica...")

        # 2. Generar visualización gráfica con Matplotlib/NetworkX
        self._setup_visual_graph()

        # Definir la posición de los nodos (seed fija para que siempre se vea igual)
        pos = nx.spring_layout(self.nx_graph, seed=42) # 'spring_layout' intenta separar los nodos visualmente

        plt.figure(figsize=(10, 7)) # Tamaño de la ventana

        # A. Dibujar los nodos
        nx.draw_networkx_nodes(self.nx_graph, pos, node_size=700, node_color='lightblue', edgecolors='black')

        # B. Dibujar las etiquetas de los nodos (números)
        nx.draw_networkx_labels(self.nx_graph, pos, font_size=12, font_weight='bold')

        # C. Dibujar TODAS las aristas del grafo original (fondo gris, punteado)
        nx.draw_networkx_edges(self.nx_graph, pos, alpha=0.3, edge_color='gray', style='dashed', width=1)
        
        # D. Dibujar SOLO las aristas del MST (Resultado) (rojo, grueso)
        nx.draw_networkx_edges(self.nx_graph, pos, edgelist=mst_edges_list, width=3, edge_color='red', alpha=0.8)

        # E. Dibujar los pesos (etiquetas de aristas)
        edge_weights = nx.get_edge_attributes(self.nx_graph, 'weight')
        nx.draw_networkx_edge_labels(self.nx_graph, pos, edge_labels=edge_weights, font_size=10)

        plt.title("Visualización: Árbol de Expansión Mínima (Prim)", fontsize=15)
        plt.axis('off') # Ocultar ejes cartesianos
        print("Visualización mostrada en ventana emergente.")
        plt.show() # Mostrar la ventana gráfica

    # --- LÓGICA DEL ALGORITMO (Igual que antes) ---
    def min_key(self, key, mst_set):
        min_val = sys.maxsize
        min_index = -1
        for v in range(self.V):
            if key[v] < min_val and not mst_set[v]:
                min_val = key[v]
                min_index = v
        return min_index

    def ejecutar_simulacion(self):
        key = [sys.maxsize] * self.V
        parent = [None] * self.V
        key[0] = 0
        mst_set = [False] * self.V
        parent[0] = -1

        print(f"--- INICIO DE SIMULACIÓN (Nodos: {self.V}) ---\n")

        for cout in range(self.V):
            u = self.min_key(key, mst_set)
            if u == -1: break
            mst_set[u] = True
            
            if parent[u] is not None and parent[u] != -1:
                print(f"-> Paso {cout}: Se selecciona nodo {u} (conectado a {parent[u]} con peso {self.graph[u][parent[u]]})")
            elif parent[u] == -1:
                 print(f"-> Paso {cout}: Iniciando en nodo raíz {u}")

            print(f"   Explorando vecinos de {u}...")
            for v in range(self.V):
                if 0 < self.graph[u][v] < key[v] and not mst_set[v]:
                    print(f"     * Vecino {v} encontrado. Frontera actualizada: Peso hacia {v} es ahora {self.graph[u][v]}")
                    key[v] = self.graph[u][v]
                    parent[v] = u
            print("   ----------------------------------------")

        # Al finalizar, llamamos a la nueva función de visualización
        self.show_results(parent)

# --- BLOQUE DE EJECUCIÓN ---
if __name__ == '__main__':
    # Usamos el mismo ejemplo anterior
    sim = PrimSimulatorVis(5)
    
    # Grafo de ejemplo
    sim.graph = [
        [0, 2, 0, 6, 0], # Nodo 0
        [2, 0, 3, 8, 5], # Nodo 1
        [0, 3, 0, 0, 7], # Nodo 2
        [6, 8, 0, 0, 9], # Nodo 3
        [0, 5, 7, 9, 0]  # Nodo 4
    ]

    sim.ejecutar_simulacion()