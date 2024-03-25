# Rancangan initial_state
initial_state = {
    "stacks": [[], [], [], [], [], [], [], [], [], []],  # Semua tumpukan awal kosong
    "holding": None,  # tidak ada balok yang dipegang
    "on_table": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],  # Semua balok ada di meja
    "clear": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],  # Semua balok di atas tumpukan
    "arm_empty": True  # lengan robot kosong
}

# Rancangan goal_state
goal_state = {
    "stacks": [[10], [9], [8], [7], [6], [5], [4], [3], [2], [1]],  # 10 tumpukan akhir
    "holding": None,
    "on_table": [],
    "clear": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "arm_empty": True
}

# Implementasi fungsi untuk melakukan aksi
def stack(x, y, state):
    # P: CLEAR(y) ∧ HOLDING(x)
    if state["clear"][y-1] and state["holding"] == x and x in state["stacks"][x-1]:
        new_state = state.copy()
        new_state["stacks"][y-1].append(x)
        new_state["stacks"][x-1].remove(x)
        new_state["holding"] = None
        new_state["clear"][x-1] = False
        new_state["arm_empty"] = True
        return new_state
    return None

def unstack(x, y, state):
    # P: ON(x,y) ∧ CLEAR(x) ∧ ARMEMPTY
    if x in state["stacks"][y-1] and state["clear"][x-1] and state["arm_empty"] and y in state["stacks"][x-1]:
        new_state = state.copy()
        new_state["stacks"][x-1].append(x)
        new_state["stacks"][y-1].remove(x)
        new_state["clear"][x-1] = True
        new_state["holding"] = x
        new_state["arm_empty"] = False
        return new_state
    return None

def pickup(x, state):
    # P: ONTABLE(x) ∧ CLEAR(x) ∧ ARMEMPTY
    if x in state["on_table"] and state["clear"][x-1] and state["arm_empty"]:
        new_state = state.copy()
        new_state["on_table"].remove(x)
        new_state["holding"] = x
        new_state["arm_empty"] = False
        return new_state
    return None

def putdown(x, state):
    # P: HOLDING(x)
    if state["holding"] == x:
        new_state = state.copy()
        new_state["on_table"].append(x)
        new_state["holding"] = None
        new_state["arm_empty"] = True
        return new_state
    return None

def graphplan(initial_state, goal_state):
    current_level = [initial_state]
    graph = {0: current_level}

    while True:
        next_level = []
        for state in current_level:
            if state == goal_state:
                return True  # Goal state tercapai

            # Generate aksi dan tambahkan ke level berikutnya
            actions = [stack, unstack, pickup, putdown]
            for action in actions:
                for x in range(1, 11):
                    if action == pickup and state["arm_empty"] and x in state["on_table"]:
                        new_state = action(x, state)
                        if new_state and new_state not in next_level:
                            next_level.append(new_state)
                    elif action == putdown and state["holding"] is not None:
                        new_state = action(state["holding"], state)
                        if new_state and new_state not in next_level:
                            next_level.append(new_state)
                    elif action != pickup and action != putdown:
                        for y in range(1, 11):
                            new_state = action(x, y, state)
                            if new_state and new_state not in next_level:
                                next_level.append(new_state)

        # Pruning
        next_level = remove_duplicates(next_level)

        if not next_level:
            return False  # Tidak ada solusi

        # Heuristik: Prioritaskan aksi yang mendekati goal state
        next_level.sort(key=lambda x: heuristic(x, goal_state))

        current_level = next_level
        graph[len(graph)] = current_level

def remove_duplicates(states):
    unique_states = []
    for state in states:
        if state not in unique_states:
            unique_states.append(state)
    return unique_states

def heuristic(state, goal_state):
    correct_stacks = sum(1 for stack, correct_stack in zip(state["stacks"], goal_state["stacks"]) if stack == correct_stack)
    return correct_stacks

plan_exists = graphplan(initial_state, goal_state)
if plan_exists:
    print("Solusi ditemukan!")
else:
    print("Tidak ada solusi untuk masalah ini.")

