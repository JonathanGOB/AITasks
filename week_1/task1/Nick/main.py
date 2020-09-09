# Variables setup
f = "F"
c = "C"
g = "G"
w = "W"

# States
state_start = ({f, c, g, w}, set())
state1 = ({f}, {c, g, w})
state2 = ({c}, {f, g, w})
state3 = ({g}, {f, c, w})
state4 = ({w}, {f, c, g})
state5 = ({f, c}, {g, w})
state6 = ({f, g}, {c, w})
state7 = ({f, w}, {c, g})
state8 = ({g, w}, {f, c})
state9 = ({c, w}, {f, g})
state10 = ({c, g}, {f, w})
state11 = ({c, g, w}, {f})
state12 = ({f, g, w}, {c})
state13 = ({f, c, w}, {g})
state14 = ({f, c, g}, {w})
state_goal = (set(), {f, c, g, w})

# List of all states
list_of_states = [state_start, state1, state2, state3, state4, state5, state6, state7, state8, state9, state10,
                  state11, state12, state13, state14, state_goal]

# Actions
action1 = {f}
action2 = {f, c}
action3 = {f, g}
action4 = {f, w}

# Cache
cache = [state_start]

# Visited
visited = set()


# Move item(s) to the left
def move_left(current_action, current_state):
    for x in current_action:
        current_state[1].remove(x)
        current_state[0].add(x)
    visited.add(current_state)


# Move item(s) to the right
def move_right(current_action, current_state):
    for x in current_action:
        current_state[0].remove(x)
        current_state[1].add(x)
    visited.add(current_state)


# Checks if the state is a solution
def check_is_solution(current_state):
    if len(current_state[1]) == 4:  # Everybody is on the right side
        print_solution()
    else:
        return False


# Checks if the state is valid
def check_is_valid(current_state):
    for x in current_state:
        if len(x) == 2:
            if "W" in x and "G" in x:  # Wolf eats Goat
                return False
            elif "G" in x and "C" in x:  # Goat eats Cabbage
                return False
    return True


# Print solution
def print_solution():
    for x in cache:
        print(x)


# Gives possible next states
def get_next_states():
    # TODO
    pass


# Run the program
def run():
    if not check_is_valid(cache[-1]):  # State is not valid
        cache.pop()
        get_next_states(cache[-1])
    else:  # State is valid
        if not check_is_solution(cache[-1]):  # State is not the solution
            get_next_states(cache[-1])
        else:  # State is the solution
            print_solution()