import copy


class Node:
    data = None  # Contains the state
    parent = None  # Contains the parent
    children = []   # Contains the children
    path = []   # Contains the previous steps

    def __init__(self, data, parent=None):
        self.data = data
        self.parent = parent

    def add_child(self, child):
        self.children.append(child)
        child.path = self.path + [self.data]
        return child


solutions = []  # List of possible solutions


def generator(node):  # Start the program
    for x in node.data[0]:  # Do the left side
        if move_right(node, {x, "F"}) in node.path:  # If the state already happened skip
            continue
        child = node.add_child(Node(move_right(node, {x, "F"}), node))  # Get the next state
        if not is_valid(child):  # Check if next state is valid
            continue
        if len(child.data[1]) == 4:  # If the state is a goal state, add it to solutions
            solutions.append(child)
            continue
        for y in child.data[1]:  # Do the right side
            if move_left(child, {y, "F"}) in child.path:
                continue
            grand_child = child.add_child(Node(move_left(child, {y, "F"}), node))
            if is_valid(grand_child):
                generator(grand_child)
    return


def is_valid(node):
    for x in node.data:
        if "W" in x and "G" in x:
            if "F" in x:
                continue
            else:
                return False
        if "C" in x and "G" in x:
            if "F" in x:
                continue
            else:
                return False
    return True


def print_solutions(solution):
    for x in solution:
        for y in x.path:
            print(y, end="")
            print(" -> ", end="")
        print(x.data)


def move_right(node, action):
    new_node = copy.deepcopy(node)
    for x in action:
        new_node.data[0].remove(x)
        new_node.data[1].add(x)
    return new_node.data


def move_left(node, action):
    new_node = copy.deepcopy(node)
    for x in action:
        new_node.data[1].remove(x)
        new_node.data[0].add(x)
    return new_node.data


generator(Node(({"F", "C", "G", "W"}, set())))
print_solutions(solutions)
