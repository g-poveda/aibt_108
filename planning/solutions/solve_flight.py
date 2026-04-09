def flight_graph_heuristic(flight_graph, n):
    return flight_graph.compute_great_circle_distance(n.data, flight_graph.arrival)
    
astar = Astar(
    flight_graph,
    lambda n : flight_graph_heuristic(flight_graph, n),
    verbose=False,
    render=False  # set to true if you want visual rendering of the search
)
solution = astar.solve_from(FlightGraph.Node(flight_graph.departure))
path = [n[0].data for n in solution[1]]
flight_graph.render(path[-1], path)