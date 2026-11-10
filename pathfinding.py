
import heapq


def heuristic(position, goal):

    # Manhattan Distance
    row1, col1 = position
    row2, col2 = goal

    return abs(row1 - row2) + abs(col1 - col2)


def astar(environment, start, goal):

    # Priority Queue
    open_list = []

    heapq.heappush(
        open_list,
        (0, start)
    )

    # Store previous positions
    came_from = {}

    # Cost from start
    g_score = {start: 0}

    # Estimated total cost
    f_score = {
        start: heuristic(start, goal)
    }

    visited = set()

    while open_list:

        current_f, current = heapq.heappop(open_list)

        # Skip already visited nodes
        if current in visited:
            continue

        visited.add(current)

        # Destination reached
        if current == goal:

            path = []

            while current in came_from:

                path.append(current)

                current = came_from[current]

            path.append(start)

            path.reverse()

            return path

        # Check neighboring cells
        for neighbor in environment.get_neighbors(current):

            if neighbor in visited:
                continue

            tentative_g = g_score[current] + 1

            if tentative_g < g_score.get(neighbor, float("inf")):

                came_from[neighbor] = current

                g_score[neighbor] = tentative_g

                f_score[neighbor] = (
                    tentative_g +
                    heuristic(neighbor, goal)
                )

                heapq.heappush(
                    open_list,
                    (f_score[neighbor], neighbor)
                )

    # No path found
    return []
