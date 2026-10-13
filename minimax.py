
from collections import deque

# --------------------------------
# MOVEMENT DIRECTIONS
# --------------------------------

DIRECTIONS = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1)
]


# --------------------------------
# VALID MOVES
# --------------------------------

def valid_moves(position, size, walls):
    row, col = position
    moves = []

    for dr, dc in DIRECTIONS:
        next_pos = (row + dr, col + dc)

        if (
            0 <= next_pos[0] < size
            and 0 <= next_pos[1] < size
            and next_pos not in walls
        ):
            moves.append(next_pos)

    return moves


# --------------------------------
# SHORTEST PATH AROUND WALLS
# --------------------------------

def shortest_distance(start, goal, size, walls):
    if start == goal:
        return 0

    queue = deque([(start, 0)])
    visited = {start}

    while queue:
        position, distance = queue.popleft()

        for next_pos in valid_moves(position, size, walls):
            if next_pos == goal:
                return distance + 1

            if next_pos not in visited:
                visited.add(next_pos)
                queue.append((next_pos, distance + 1))

    return size * size * 2


# --------------------------------
# EVALUATION FUNCTION
# --------------------------------

def evaluate(player, warden, size, walls, keys, exit_pos):
    """
    Higher scores favor the warden.

    The warden wants to:
    1. Catch the player.
    2. Get near the player's next objective.
    3. Block important escape routes.
    """

    if player == warden:
        return 1000

    player_distance = shortest_distance(
        warden, player, size, walls
    )

    # Player's next objective
    if keys:
        target = min(
            keys,
            key=lambda key: shortest_distance(
                player, key, size, walls
            )
        )
    else:
        target = exit_pos

    # Distance from warden to objective
    target_distance = shortest_distance(
        warden, target, size, walls
    )

    # Distance from player to objective
    player_target_distance = shortest_distance(
        player, target, size, walls
    )

    score = (
        -5 * player_distance
        -2 * target_distance
        -1 * player_target_distance
    )

    return score


# --------------------------------
# MINIMAX WITH ALPHA-BETA PRUNING
# --------------------------------

def minimax(
    player,
    warden,
    size,
    walls,
    keys,
    exit_pos,
    depth,
    alpha,
    beta,
    maximizing,
    stats
):
    stats["nodes"] += 1

    if player == warden or depth == 0:
        return evaluate(
            player, warden, size,
            walls, keys, exit_pos
        )

    if maximizing:
        best_score = float("-inf")
        moves = valid_moves(warden, size, walls)

        if not moves:
            return evaluate(
                player, warden, size,
                walls, keys, exit_pos
            )

        for next_warden in moves:
            score = minimax(
                player,
                next_warden,
                size,
                walls,
                keys,
                exit_pos,
                depth - 1,
                alpha,
                beta,
                False,
                stats
            )

            best_score = max(best_score, score)
            alpha = max(alpha, best_score)

            if beta <= alpha:
                stats["prunes"] += 1
                break

        return best_score

    else:
        best_score = float("inf")
        moves = valid_moves(player, size, walls)

        if not moves:
            return evaluate(
                player, warden, size,
                walls, keys, exit_pos
            )

        for next_player in moves:
            score = minimax(
                next_player,
                warden,
                size,
                walls,
                keys,
                exit_pos,
                depth - 1,
                alpha,
                beta,
                True,
                stats
            )

            best_score = min(best_score, score)
            beta = min(beta, best_score)

            if beta <= alpha:
                stats["prunes"] += 1
                break

        return best_score


# --------------------------------
# BEST WARDEN MOVE
# --------------------------------

def best_warden_move(
    player,
    warden,
    size,
    walls,
    keys,
    exit_pos,
    depth=3
):
    stats = {
        "nodes": 0,
        "prunes": 0
    }

    moves = valid_moves(warden, size, walls)

    if not moves:
        return (
            warden,
            evaluate(
                player, warden, size,
                walls, keys, exit_pos
            ),
            stats
        )

    best_move = warden
    best_score = float("-inf")

    for move in moves:
        score = minimax(
            player,
            move,
            size,
            walls,
            keys,
            exit_pos,
            depth - 1,
            float("-inf"),
            float("inf"),
            False,
            stats
        )

        if score > best_score:
            best_score = score
            best_move = move

    return best_move, best_score, stats
