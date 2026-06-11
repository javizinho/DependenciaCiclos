import json

class DeliveryDependencyAnalyzer:

    DEPENDENCY_GRAPH = {
        "app/page.tsx": [
            "screens/HomeScreen",
            "screens/CartScreen",
            "screens/OrderScreen",
        ],
        "screens/HomeScreen": [
            "components/RestaurantCard",
            "hooks/useRestaurants",
        ],
        "screens/CartScreen": [
            "components/ProductItem",
            "hooks/useCart",
        ],
        "screens/OrderScreen": [
            "components/OrderTracker",
            "components/MapView",
            "hooks/useOrder",
        ],
        "components/RestaurantCard": [
            "hooks/useRestaurants",
        ],
        "components/ProductItem": [
            "hooks/useCart",
        ],
        "components/OrderTracker": [
            "hooks/useOrder",
            "services/trackingApi",
        ],
        "components/MapView": [
            "hooks/useLocation",
            "services/trackingApi",
        ],
        # CYCLE: useCart ↔ useOrder
        "hooks/useCart": [
            "services/orderApi",
            "hooks/useOrder",
        ],
        "hooks/useOrder": [
            "services/orderApi",
            "hooks/useCart",
        ],
        "hooks/useRestaurants": [
            "services/restaurantApi",
        ],
        "hooks/useLocation": [
            "services/trackingApi",
        ],
        "services/restaurantApi": [],
        "services/orderApi": [],
        "services/trackingApi": [],
    }

    DISPLAY_NAMES = {
        "app/page.tsx":             "Inicio de la app",
        "screens/HomeScreen":       "Pantalla principal",
        "screens/CartScreen":       "Pantalla del carrito",
        "screens/OrderScreen":      "Pantalla del pedido",
        "components/RestaurantCard":"Tarjeta de restaurante",
        "components/ProductItem":   "Ítem del menú",
        "components/OrderTracker":  "Seguimiento del pedido",
        "components/MapView":       "Mapa del repartidor",
        "hooks/useRestaurants":     "useRestaurants",
        "hooks/useCart":            "useCart",
        "hooks/useOrder":           "useOrder",
        "hooks/useLocation":        "useLocation",
        "services/restaurantApi":   "API de restaurantes",
        "services/orderApi":        "API de pedidos",
        "services/trackingApi":     "API de rastreo GPS",
    }

    def __init__(self):
        self.graph = self.DEPENDENCY_GRAPH
        self.cycles = []

    def detect_cycles(self):
        visited = set()
        rec_stack = set()
        path = []

        def dfs(u):
            visited.add(u)
            rec_stack.add(u)
            path.append(u)
            for v in self.graph.get(u, []):
                if v in rec_stack:
                    idx = path.index(v)
                    new_cycle = path[idx:] + [v]
                    if not any(set(new_cycle) == set(c) for c in self.cycles):
                        self.cycles.append(new_cycle)
                elif v not in visited and v in self.graph:
                    dfs(v)
            rec_stack.remove(u)
            path.pop()

        for node in list(self.graph.keys()):
            if node not in visited:
                dfs(node)

    def generate_outputs(self):
        report = {
            "metadata": {
                "project": "Delivery App",
                "total_modules": len(self.graph),
                "total_cycles": len(self.cycles),
            },
            "cycles_detected": self.cycles,
            "full_graph": self.graph,
        }
        with open("dependency_report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4)

        critical_nodes = set(n for c in self.cycles for n in c)

        LAYER_COLORS = {
            "Entrypoint": "#D8B4FE",
            "Screens":    "#BFDBFE",
            "Components": "#99F6E4",
            "Hooks":      "#FDE68A",
            "Services":   "#D1D5DB",
        }

        layers = {
            "Entrypoint": ["app/page.tsx"],
            "Screens":    [n for n in self.graph if n.startswith("screens/")],
            "Components": [n for n in self.graph if n.startswith("components/")],
            "Hooks":      [n for n in self.graph if n.startswith("hooks/")],
            "Services":   [n for n in self.graph if n.startswith("services/")],
        }

        with open("dependency_graph.dot", "w", encoding="utf-8") as f:
            f.write("digraph DeliveryApp {\n")
            f.write('  rankdir=TB;\n')
            f.write('  node [fontname="Arial", shape=rect, style=filled, fillcolor="#F0F0F0"];\n\n')

            for layer, nodes in layers.items():
                f.write(f'  subgraph cluster_{layer} {{\n')
                f.write(f'    label="{layer}";\n')
                f.write(f'    style=dashed;\n')
                for node in nodes:
                    color  = '#FFCCCC' if node in critical_nodes else LAYER_COLORS[layer]
                    border = 'color="#CC0000", penwidth=2' if node in critical_nodes else 'color="#666666"'
                    label  = self.DISPLAY_NAMES.get(node, node)
                    f.write(f'    "{node}" [label="{label}", fillcolor="{color}", {border}];\n')
                f.write("  }\n\n")

            f.write("  // Edges\n")
            for u, neighbors in self.graph.items():
                for v in neighbors:
                    if v in self.graph:
                        is_cycle = (u in critical_nodes and v in critical_nodes)
                        style = 'color="#CC0000", penwidth=2, style=dashed' if is_cycle else 'color="#555555"'
                        f.write(f'  "{u}" -> "{v}" [{style}];\n')
            f.write("}\n")

    def run(self):
        print("\n" + "="*52)
        print("🚀  DEPENDENCY ANALYZER — Delivery App")
        print("="*52)
        self.detect_cycles()
        self.generate_outputs()
        print(f"✅  Modules analyzed : {len(self.graph)}")
        print(f"⚠️   Cycles detected  : {len(self.cycles)}")
        if self.cycles:
            print("\n📛  Cycles found:")
            for i, cycle in enumerate(self.cycles, 1):
                print(f"   {i}. {' → '.join(cycle)}")
        print("\n📄  Output files:")
        print("   • dependency_report.json")
        print("   • dependency_graph.dot")
        print("="*52 + "\n")

if __name__ == "__main__":
    DeliveryDependencyAnalyzer().run()