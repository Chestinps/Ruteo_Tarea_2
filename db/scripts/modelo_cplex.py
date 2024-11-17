import cplex
import json

# Cargar datos del grafo
def load_graph_data(file_path="graph_data.json"):
    with open(file_path, "r") as f:
        return json.load(f)

# Modelo de optimización
def solve_shortest_path(graph_data, source, target):
    cpx = cplex.Cplex()

    # Cambiar el tipo de problema a lineal
    cpx.set_problem_type(cpx.problem_type.LP)

    nodes = {node["id"]: node for node in graph_data["nodes"]}
    edges = graph_data["edges"]

    # Variables de decisión: una por cada arista (binary)
    edge_vars = []
    for edge in edges:
        var_name = f"e_{edge['id']}"
        edge_vars.append(var_name)
        cpx.variables.add(obj=[edge["cost"]], names=[var_name], types=["B"])

    # Restricción 1: Flujo de entrada y salida para los nodos
    for node_id in nodes.keys():
        in_edges = list(set(f"e_{edge['id']}" for edge in edges if edge["target"] == node_id))
        out_edges = list(set(f"e_{edge['id']}" for edge in edges if edge["source"] == node_id))

        print(f"Nodo: {node_id}, in_edges: {in_edges}, out_edges: {out_edges}")  # Debugging

        if node_id == source:
            cpx.linear_constraints.add(
                lin_expr=[cplex.SparsePair(out_edges, [1] * len(out_edges))],
                senses=["E"],
                rhs=[1],
            )
        elif node_id == target:
            cpx.linear_constraints.add(
                lin_expr=[cplex.SparsePair(in_edges, [1] * len(in_edges))],
                senses=["E"],
                rhs=[1],
            )
        else:
            cpx.linear_constraints.add(
                lin_expr=[
                    cplex.SparsePair(in_edges + out_edges, [1] * len(in_edges) + [-1] * len(out_edges))
                ],
                senses=["E"],
                rhs=[0],
            )

    # Restricción 2: Penalización de tráfico, accidentes y reductores
    penalties = []
    for edge in edges:
        source_node = nodes[edge["source"]]
        penalty = (
            source_node["traffic_cost"]
            + (10 if source_node["has_accidents"] else 0)
            + (5 if source_node["has_traffic_bump"] else 0)
        )
        penalties.append(penalty)

    for i, edge_var in enumerate(edge_vars):
        cpx.objective.set_linear([(edge_var, penalties[i])])

    # Resolver
    cpx.solve()

    # Resultados
    solution = cpx.solution.get_values()
    selected_edges = [edges[i] for i in range(len(edges)) if solution[i] > 0.5]
    return selected_edges

# Ejecutar modelo
graph_data = load_graph_data()
source = 1  # Nodo inicial
target = 5  # Nodo final
result = solve_shortest_path(graph_data, source, target)

print("Ruta óptima:")
for edge in result:
    print(f"De {edge['source']} a {edge['target']} con costo {edge['cost']}")
