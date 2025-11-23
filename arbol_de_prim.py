import sys

class PrimSimulator:
    def __init__(self, vertices):
        self.V = vertices
        # Usamos una matriz de adyacencia para representar el grafo
        # Inicializamos con 0 (sin conexión)
        self.graph = [[0 for column in range(vertices)] for row in range(vertices)]

    def print_mst(self, parent):
        print("\n" + "="*40)
        print("RESULTADO FINAL: Árbol de Expansión Mínima")
        print("="*40)
        print(f"{'Arista':<10} {'Peso':<10}")
        total_weight = 0
        for i in range(1, self.V):
            print(f"{parent[i]} - {i} \t {self.graph[i][parent[i]]}")
            total_weight += self.graph[i][parent[i]]
        print(f"\nCosto Total del Camino: {total_weight}")

    def min_key(self, key, mst_set):
        """Encuentra el vértice con el valor mínimo de la arista,
        de los vértices que aún no están en el MST"""
        min_val = sys.maxsize
        min_index = -1

        for v in range(self.V):
            if key[v] < min_val and not mst_set[v]:
                min_val = key[v]
                min_index = v
        return min_index

    def ejecutar_simulacion(self):
        # Key values usados para elegir el peso mínimo
        key = [sys.maxsize] * self.V
        parent = [None] * self.V  # Array para guardar el árbol
        key[0] = 0
        mst_set = [False] * self.V

        parent[0] = -1  # El primer nodo es la raíz

        print(f"--- INICIO DE SIMULACIÓN (Nodos: {self.V}) ---\n")

        for cout in range(self.V):
            # 1. Escoger el vértice de distancia mínima del set que no está en el MST
            u = self.min_key(key, mst_set)
            
            # Nota: Si el grafo no es conexo, u podría ser -1 o inválido aquí.
            if u == -1: 
                break

            mst_set[u] = True
            
            if parent[u] is not None and parent[u] != -1:
                print(f"-> Paso {cout}: Conectando nodo {parent[u]} con nodo {u} (Peso: {self.graph[u][parent[u]]})")
            elif parent[u] == -1:
                 print(f"-> Paso {cout}: Iniciando en nodo raíz {u}")

            # 2. Actualizar el valor key de los vértices adyacentes
            print(f"   Explorando vecinos de {u}...")
            for v in range(self.V):
                # graph[u][v] > 0 indica que hay una arista
                # mst_set[v] == False indica que v no está incluido aún en el MST
                # Actualizamos key solo si el peso es menor al actual key[v]
                if 0 < self.graph[u][v] < key[v] and not mst_set[v]:
                    print(f"     * Vecino {v} encontrado. Actualizando costo para llegar a {v}: de {key[v]} a {self.graph[u][v]}")
                    key[v] = self.graph[u][v]
                    parent[v] = u
            print("   ----------------------------------------")

        self.print_mst(parent)

# --- BLOQUE DE EJECUCIÓN ---
if __name__ == '__main__':
    # Ejemplo: Creamos un grafo de 5 nodos (0 a 4)
    sim = PrimSimulator(5)
    
    sim.graph = [
        [0, 2, 0, 6, 0], # Nodo 0
        [2, 0, 3, 8, 5], # Nodo 1
        [0, 3, 0, 0, 7], # Nodo 2
        [6, 8, 0, 0, 9], # Nodo 3
        [0, 5, 7, 9, 0]  # Nodo 4
    ]

    sim.ejecutar_simulacion()