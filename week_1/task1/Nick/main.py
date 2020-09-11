import copy


class Node:
    data = None  # Contains the state
    path = []   # Contains the previous steps

    def __init__(self, data):
        self.data = data

    def make_child(self, child):  # make child node
        child.path = self.path + [self.data]  # Add this node state and previous states to the path of the child
        return child


solutions = []  # List of possible solutions


def generator(node):  # Start the program
    for x in node.data[0]:  # Do the left side
        if move_right(node, {x, "F"}) in node.path:  # If the state already happened skip
            continue
        child = node.make_child(Node(move_right(node, {x, "F"})))  # Get and add the next state
        if not is_valid(child):  # Check if next state is valid
            continue
        if len(child.data[1]) == 4:  # If the state is a goal state, add it to solutions
            solutions.append(child)
            continue
        for y in child.data[1]:  # Do the right side
            if move_left(child, {y, "F"}) in child.path:  # If the state already happened skip
                continue
            grand_child = child.make_child(Node(move_left(child, {y, "F"})))  # Get and add the next state
            if is_valid(grand_child):  # Check if next state is valid
                generator(grand_child)  # Continue the generator with the new state


def is_valid(node):  # Check if state is valid for left and right side
    for x in node.data:
        if "W" in x and "G" in x:  # Check if wolf and goat are together
            if "F" in x:  # Check if the farmer is with them
                continue
            else:  # Non-valid state
                return False
        if "C" in x and "G" in x:  # Check if cabbage and goat are together
            if "F" in x:   # Check if the farmer is with them
                continue
            else:  # Non-valid state
                return False
    return True  # Valid state


def print_solutions(solution):  # Print the found solutions
    for x in solution:
        for y in x.path:
            print(y, end="")
            print(" -> ", end="")
        print(x.data)


def move_right(node, action):  # Move the objects to the right
    new_node = copy.deepcopy(node)
    for x in action:
        new_node.data[0].remove(x)
        new_node.data[1].add(x)
    return new_node.data


def move_left(node, action):  # Move the objects to the left
    new_node = copy.deepcopy(node)
    for x in action:
        new_node.data[1].remove(x)
        new_node.data[0].add(x)
    return new_node.data


generator(Node(({"F", "C", "G", "W"}, set())))
print_solutions(solutions)
