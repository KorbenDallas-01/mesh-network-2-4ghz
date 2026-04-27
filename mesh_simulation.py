import math
import heapq

# ============================================================
# Simple 2.4 GHz Mesh Network Simulation
# ============================================================
# This script simulates a small mesh network with radio nodes.
# It calculates signal loss caused by distance and obstacles,
# then finds the best communication path between two nodes.
#
# Beginner-friendly version.
# ============================================================


# -----------------------------
# Network nodes
# -----------------------------
# Each node has a name and position: (x, y) in meters.
nodes = {
    "Node 1 - Base": (0, 0),
    "Node 2 - Relay": (120, 40),
    "Node 3 - Relay": (260, 90),
    "Node 4 - Group": (400, 120),
}


# -----------------------------
# Obstacle attenuation in dB
# -----------------------------
# Higher value = stronger signal loss.
obstacle_loss = {
    "glass": 3,
    "wood": 6,
    "brick": 12,
    "concrete": 25,
    "metal": 100,
}


# Obstacles between node pairs.
# For simplicity, we define them manually.
obstacles_between_nodes = {
    ("Node 1 - Base", "Node 2 - Relay"): ["wood"],
    ("Node 2 - Relay", "Node 3 - Relay"): ["brick"],
    ("Node 3 - Relay", "Node 4 - Group"): ["concrete"],
    ("Node 1 - Base", "Node 3 - Relay"): ["concrete", "brick"],
    ("Node 2 - Relay", "Node 4 - Group"): ["metal"],
    ("Node 1 - Base", "Node 4 - Group"): ["concrete", "metal"],
}


# -----------------------------
# Radio parameters
# -----------------------------
frequency_mhz = 2400
max_allowed_loss_db = 95


# -----------------------------
# Helper functions
# -----------------------------
def distance(point_a, point_b):
    """Calculate distance between two points."""
    x1, y1 = point_a
    x2, y2 = point_b
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def free_space_path_loss(distance_meters, frequency_mhz):
    """
    Calculate Free Space Path Loss (FSPL) in dB.

    Formula:
    FSPL = 20 log10(distance_km) + 20 log10(frequency_MHz) + 32.44
    """
    distance_km = distance_meters / 1000

    if distance_km <= 0:
        return 0

    return 20 * math.log10(distance_km) + 20 * math.log10(frequency_mhz) + 32.44


def get_obstacles(node_a, node_b):
    """Return obstacles between two nodes."""
    return obstacles_between_nodes.get((node_a, node_b), obstacles_between_nodes.get((node_b, node_a), []))


def total_link_loss(node_a, node_b):
    """Calculate total signal loss between two nodes."""
    point_a = nodes[node_a]
    point_b = nodes[node_b]

    d = distance(point_a, point_b)
    fspl = free_space_path_loss(d, frequency_mhz)

    obstacles = get_obstacles(node_a, node_b)
    obstacle_total_loss = sum(obstacle_loss[item] for item in obstacles)

    return fspl + obstacle_total_loss


def build_network_graph():
    """Build graph of possible radio links."""
    graph = {node: [] for node in nodes}

    node_names = list(nodes.keys())

    for i in range(len(node_names)):
        for j in range(i + 1, len(node_names)):
            node_a = node_names[i]
            node_b = node_names[j]

            loss = total_link_loss(node_a, node_b)

            if loss <= max_allowed_loss_db:
                graph[node_a].append((node_b, loss))
                graph[node_b].append((node_a, loss))

    return graph


def find_best_path(start, end):
    """
    Find the path with the lowest total signal loss.
    Uses Dijkstra algorithm.
    """
    graph = build_network_graph()

    queue = [(0, start, [])]
    visited = set()

    while queue:
        current_loss, current_node, path = heapq.heappop(queue)

        if current_node in visited:
            continue

        visited.add(current_node)
        path = path + [current_node]

        if current_node == end:
            return current_loss, path

        for neighbor, link_loss in graph[current_node]:
            if neighbor not in visited:
                heapq.heappush(queue, (current_loss + link_loss, neighbor, path))

    return None, []


# -----------------------------
# Main program
# -----------------------------
if __name__ == "__main__":
    print("2.4 GHz Mesh Network Simulation")
    print("=" * 40)

    print("\nAvailable links:")
    graph = build_network_graph()

    for node, links in graph.items():
        for neighbor, loss in links:
            print(f"{node} <--> {neighbor}: {loss:.2f} dB")

    start_node = "Node 1 - Base"
    end_node = "Node 4 - Group"

    best_loss, best_path = find_best_path(start_node, end_node)

    print("\nBest communication path:")

    if best_path:
        print(" -> ".join(best_path))
        print(f"Total path loss: {best_loss:.2f} dB")
    else:
        print("No available path found.")
