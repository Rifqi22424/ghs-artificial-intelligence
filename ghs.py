def clear(state, block):
    return f"CLEAR({block})" in state

def holding(state, block):
    return f"HOLDING({block})" in state

def on(state, block1, block2):
    return f"on ({block1},{block2})" in state

def on_table(state, block):
    return f"onTable ({block})" in state

def arm_empty(state):
    return "armepty" in state

def stack(x, y):
    return f"CLEAR({y}) ^ HOLDING({x})"

def unstack(x, y):
    return f"ON({x},{y}) ^ CLEAR({x}) ^ ARMEMPTY"

def pickup(x):
    return f"ONTABLE({x}) ^ CLEAR({x}) ^ ARMEMPTY"

def putdown(x):
    return f"HOLDING({x})"

def apply_action(state, action):
    preconditions, action_type, effects = action
    for pre in preconditions:
        if pre not in state:
            return state, False
    new_state = state.copy()
    new_state.difference_update(preconditions)
    new_state.update(effects)
    return new_state, True

def planning(initial_state, goal_state):
    stack_action = (stack("x", "y"), "P", {"on(x,y)"})
    unstack_action = (unstack("x", "y"), "UNSTACK", {"HOLDING(x)", "CLEAR(y)"})
    pickup_action = (pickup("x"), "PICKUP", {"HOLDING(x)"})
    putdown_action = (putdown("x"), "PUTDOWN", {"ONTABLE(x)", "ARMEMPTY"})

    actions = [stack_action, unstack_action, pickup_action, putdown_action]

    state = set(initial_state.split(" ^ "))
    goal = set(goal_state.split(" ^ "))

    plan = []

    while state != goal:
        applicable_actions = []
        for action in actions:
            _, action_type, _ = action
            if action_type == "P":
                x, y = action[0].split('(')[1].split(')')[0].split(',')
                if holding(state, x) and clear(state, y):
                    applicable_actions.append(action)
            elif action_type == "UNSTACK":
                x, y = action[0].split('(')[1].split(')')[0].split(',')
                if on(state, x, y) and clear(state, x) and arm_empty(state):
                    applicable_actions.append(action)
            elif action_type == "PICKUP":
                x = action[0].split('(')[1].split(')')[0]
                if on_table(state, x) and clear(state, x) and arm_empty(state):
                    applicable_actions.append(action)
            elif action_type == "PUTDOWN":
                x = action[0].split('(')[1].split(')')[0]
                if holding(state, x):
                    applicable_actions.append(action)

        chosen_action = applicable_actions[0]
        for action in applicable_actions:
            _, _, effects = action
            if len(effects) > len(chosen_action[2]):
                chosen_action = action

        plan.append(chosen_action)
        state, _ = apply_action(state, chosen_action)

    return plan

initial_state = "on (B,A) ^ onTable (A) ^ onTable (B) ^ on (D,C) ^ onTable (C) ^ onTable (F) ^ onTable (G) ^ on (H,I) ^ on (J,H) ^ onTable (I) ^ armepty"
goal_state = "on (B,A) ^ onTable (A) ^ on (D,C) ^ on (E,D) ^ onTable (C) ^ on (F,G) ^ onTable (G) ^ on (H,I) ^ onTable (I) ^ onTable (J) ^ armepty"

plan = planning(initial_state, goal_state)

print("Plan to achieve the goal state:")
for action in plan:
    print(f"{action[1]}:\t{action[0]}")