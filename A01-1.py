from collections import deque
import heapq
import networkx as nx
import matplotlib.pyplot as plt

# Predefined dictionary of valid words
DICTIONARY = set([
    "stone", "shone", "bone", "phone", "phony", "prone", "peony", "penny", "money", "honey",
    "cones", "bones", "tone", "tune", "tube", "cube", "lube", "love", "live", "life", "line", "pine",
    "wine", "wind", "wing", "ring", "king", "kind", "mind", "mine", "mint", "lint", "lent", "lend",
    "land", "lane", "lone", "none", "loan", "moan", "moon", "soon", "soot", "foot", "food", "good",
    "wood", "wool", "cool", "coal", "foal", "foam", "flam", "flame", "noon", "frame", "fame", "game", "gate",
    "gale", "gall", "ball", "bale", "bake", "brake", "cage", "came", "care", "core", "cork", "cook",
    "book", "look", "lock", "rock", "sock", "cake", "sack", "sick", "silk", "sill", "sell", "bell",
    "tale", "belt", "bolt", "boot", "boat", "coat", "coax", "coal", "foal", "foam", "flam", "flame",
    "fale"
])

MAX_MOVES = 10  # Maximum allowed moves for the player

# Difficulty-specific settings
DIFFICULTY_SETTINGS = {
    "beginner": {
        "min_steps": 3,
        "max_steps": 5,
        "banned_words": set(),
        "restricted_letters": set()
    },
    "advanced": {
        "min_steps": 6,
        "max_steps": 10,
        "banned_words": set(),
        "restricted_letters": set()
    },
    "challenge": {
        "min_steps": 5,
        "max_steps": 8,
        "banned_words": {"phone", "foam", "flame"},  # Example banned words
        "restricted_letters": {"x", "z"}  # Example restricted letters
    }
}

# Function to find all valid word transformations (one-letter changes)


def get_neighbors(word, banned_words, restricted_letters):
    neighbors = []
    for i in range(len(word)):
        for char in 'abcdefghijklmnopqrstuvwxyz':
            if char != word[i] and char not in restricted_letters:
                new_word = word[:i] + char + word[i+1:]
                if new_word in DICTIONARY and new_word not in banned_words:
                    neighbors.append(new_word)
    return neighbors

# Graph Visualization


def visualize_graph(path):
    G = nx.Graph()
    G.add_nodes_from(path)
    edges = [(path[i], path[i+1]) for i in range(len(path) - 1)]
    G.add_edges_from(edges)

    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='skyblue',
            node_size=2000, font_size=10, edge_color='gray')
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(
        path[i], path[i+1]): f'Step {i+1}' for i in range(len(path) - 1)})
    plt.title('Word Ladder Visualization')
    plt.show()

# Breadth-First Search (BFS)


def bfs(start, goal, banned_words, restricted_letters):
    queue = deque([(start, [start])])
    visited = set()
    while queue:
        current_word, path = queue.popleft()
        if current_word == goal:
            return path
        if current_word not in visited:
            visited.add(current_word)
            for neighbor in get_neighbors(current_word, banned_words, restricted_letters):
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
    return None

# Uniform Cost Search (UCS)


def ucs(start, goal, banned_words, restricted_letters):
    heap = [(0, start, [start])]
    visited = set()
    while heap:
        cost, current_word, path = heapq.heappop(heap)
        if current_word == goal:
            return path
        if current_word not in visited:
            visited.add(current_word)
            for neighbor in get_neighbors(current_word, banned_words, restricted_letters):
                if neighbor not in visited:
                    heapq.heappush(
                        heap, (cost + 1, neighbor, path + [neighbor]))
    return None

# A* Search Algorithm


def a_star(start, goal, banned_words, restricted_letters):
    def heuristic(word):
        return sum(1 for a, b in zip(word, goal) if a != b)

    heap = [(heuristic(start), 0, start, [start])]
    visited = set()
    while heap:
        _, cost, current_word, path = heapq.heappop(heap)
        if current_word == goal:
            return path
        if current_word not in visited:
            visited.add(current_word)
            for neighbor in get_neighbors(current_word, banned_words, restricted_letters):
                if neighbor not in visited:
                    heapq.heappush(
                        heap, (cost + 1 + heuristic(neighbor), cost + 1, neighbor, path + [neighbor]))
    return None

# Validate player's move


def is_valid_move(current_word, next_word, banned_words, restricted_letters):
    return next_word in get_neighbors(current_word, banned_words, restricted_letters)

# Game Logic


def word_ladder_game():
    print("Welcome to the Word Ladder Adventure Game!")
    print("Choose a difficulty level:")
    print("1. Beginner")
    print("2. Advanced")
    print("3. Challenge")
    difficulty_choice = input("Enter your choice (1/2/3): ").strip()

    if difficulty_choice == '1':
        difficulty = "beginner"
    elif difficulty_choice == '2':
        difficulty = "advanced"
    elif difficulty_choice == '3':
        difficulty = "challenge"
    else:
        print("Invalid choice. Defaulting to Beginner mode.")
        difficulty = "beginner"

    settings = DIFFICULTY_SETTINGS[difficulty]
    banned_words = settings["banned_words"]
    restricted_letters = settings["restricted_letters"]

    print(f"\nYou have selected {difficulty.capitalize()} mode.")
    if banned_words:
        print(f"Banned words: {', '.join(banned_words)}")
    if restricted_letters:
        print(f"Restricted letters: {', '.join(restricted_letters)}")

    start = input("Enter the starting word: ").strip().lower()
    goal = input("Enter the target word: ").strip().lower()

    if start not in DICTIONARY or goal not in DICTIONARY:
        print("Invalid words. Please ensure both words are in the dictionary.")
        return

    remaining_moves = MAX_MOVES
    current_word = start
    path = [start]

    while remaining_moves > 0 and current_word != goal:
        print(
            f"\nCurrent word: {current_word}, Remaining moves: {remaining_moves}")
        player_move = input(
            "Enter the next word or type 'hint' for AI assistance: ").strip().lower()

        if player_move == 'hint':
            print("\nChoose an AI assistance method:")
            print("1. Breadth-First Search (BFS)")
            print("2. Uniform Cost Search (UCS)")
            print("3. A* Search Algorithm")
            choice = input("Enter your choice (1/2/3): ").strip()

            if choice == '1':
                hint_path = bfs(current_word, goal,
                                banned_words, restricted_letters)
            elif choice == '2':
                hint_path = ucs(current_word, goal,
                                banned_words, restricted_letters)
            elif choice == '3':
                hint_path = a_star(current_word, goal,
                                   banned_words, restricted_letters)
            else:
                print("Invalid choice. Using BFS by default.")
                hint_path = bfs(current_word, goal,
                                banned_words, restricted_letters)

            if hint_path and len(hint_path) > 1:
                print(f"\nHint: The next best move is '{hint_path[1]}'")
            else:
                print("\nNo valid hint available.")
        else:
            if is_valid_move(current_word, player_move, banned_words, restricted_letters):
                current_word = player_move
                path.append(current_word)
            else:
                print("\nInvalid move. Please enter a valid one-letter transformation.")
            remaining_moves -= 1  # Decrement remaining moves regardless of validity

    if current_word == goal:
        score = MAX_MOVES - len(path) + 1
        print(f"\nCongratulations! You reached the goal word '{goal}'!")
        print(f"Your score: {score}")
        visualize_graph(path)
    else:
        print(
            f"\nGame Over! You couldn't reach '{goal}' in the allowed moves.")


if __name__ == "__main__":
    word_ladder_game()
