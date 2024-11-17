import psycopg2
import cplex
from cplex.exceptions import CplexError

conn = psycopg2.connect(
    dbname="ruteo_db",
    user="admin",
    password="admin123",
    host="localhost",
    port="5432"
)

cur = conn.cursor()
cur.execute("""
    SELECT id, lat, lon, traffic_cost, has_traffic_bump, has_accidents
    FROM nodes;
""")
nodos = cur.fetchall()


cur.execute("""
    SELECT id, source, target, cost, reverse_cost
    FROM edges;
""")
aristas = cur.fetchall()


cur.close()
conn.close()

nodos_dict = {nodo[0]: nodo for nodo in nodos}

aristas_actualizadas = []

for arista in aristas:
    arista_id, source, target, cost, reverse_cost = arista
    
    nodo_source = nodos_dict[source]
    nodo_target = nodos_dict[target]
    
    if nodo_source[4]:
        cost *= 1.2 
    if nodo_target[4]:
        cost *= 1.2
    
    if nodo_source[5]:
        cost *= 1.5
    if nodo_target[5]:
        cost *= 1.5

    aristas_actualizadas.append((arista_id, source, target, cost, reverse_cost))

aristas_actualizadas_sin_duplicados = []
aristas_vistas = set()

for arista in aristas_actualizadas:
    arista_id, source, target, cost, reverse_cost = arista
    arista_tupla = (source, target)
    
    if arista_tupla not in aristas_vistas:
        aristas_vistas.add(arista_tupla)
        aristas_actualizadas_sin_duplicados.append(arista)

# MAndamos las aristas actualizadas al modelo
def crear_modelo_cplex(aristas_actualizadas):
    try:
        # Crear un objeto Cplex
        prob = cplex.Cplex()
        
        # Definir el nombre del problema
        prob.set_problem_name("Optimización de Rutas con Aristas Actualizadas")

        # Función objetivo (minimizar el costo total de las aristas seleccionadas)
        prob.objective.set_sense(prob.objective.sense.minimize)
        
        # Crear variables de decisión (x_ij para cada arista)
        variables = [f"x_{source}_{target}" for (arista_id, source, target, _, _) in aristas_actualizadas]

        # Definir el tipo de variables (binarias)
        prob.variables.add(names=variables, types=["B"] * len(variables))
        
        # Función objetivo: Minimizar la suma de los costos de las aristas seleccionadas
        coeficientes_objetivo = [cost for (_, _, _, cost, _) in aristas_actualizadas]
        prob.objective.set_linear(list(zip(variables, coeficientes_objetivo)))
        
        # Restricciones de conectividad (aseguramos que cada nodo esté conectado)
        nodos_unicos = set([source for (_, source, _, _, _) in aristas_actualizadas] + [target for (_, _, target, _, _) in aristas_actualizadas])

        print("Agregando restricciones de conectividad...")

        for nodo in nodos_unicos:
            flujo_entrante = [f"x_{source}_{target}" for (arista_id, source, target, _, _) in aristas_actualizadas if target == nodo]
            flujo_saliente = [f"x_{source}_{target}" for (arista_id, source, target, _, _) in aristas_actualizadas if source == nodo]

            # Verificar que las longitudes de las listas coincidan con los coeficientes
            coeficientes = [1] * len(flujo_entrante) + [-1] * len(flujo_saliente)
            assert len(flujo_entrante) + len(flujo_saliente) == len(coeficientes)

            # Agregar la restricción de conectividad
            prob.linear_constraints.add(
                lin_expr=[[flujo_entrante + flujo_saliente, coeficientes]],
                senses="E",  # 'E' para igual a
                rhs=[0]  # El lado derecho de la restricción
            )
            print(f"Nodo {nodo}: flujo_entrante = {flujo_entrante}, flujo_saliente = {flujo_saliente}")

        # Resolver el problema
        prob.solve()
        
        # Mostrar resultados
        print("Estado de la solución:", prob.solution.status[prob.solution.get_status()])
        print("Valor de la función objetivo:", prob.solution.get_objective_value())
        
        # Obtener y mostrar las variables seleccionadas
        valores_variables = prob.solution.get_values()
        
        # Mostrar las aristas seleccionadas (con valor 1)
        for i, valor in enumerate(valores_variables):
            if valor > 0.5:
                print(f"Arista seleccionada: {variables[i]}")

    except CplexError as exc:
        print(exc)

# Ejecutar el modelo con las aristas actualizadas
crear_modelo_cplex(aristas_actualizadas_sin_duplicados)
