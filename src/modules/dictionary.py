from typing import Optional
import graphviz


class Node:
    def __init__(
        self,
        value: str,
        left: Optional["Node"] = None,
        right: Optional["Node"] = None,
        index: Optional[int] = None,
    ):
        self.value = value
        self.left = left
        self.right = right
        self.index = index

    def __repr__(self):
        return f"Node({self.value})"


def convert_list_to_str(input_list: list[str]) -> str:
    """
    asumption : array has been sorted
    Input: `['Abidin', 'Abilah', 'Abimana', 'Abing', 'Abiogenesis']`
    Output: `Abidin,Abilah,Abimana,Abing,Abiogenesis`
    """
    result = ",".join(input_list)
    return result


def parse_string_to_list(input_string: str) -> list[str]:
    """
    Input:  `Abidin,Abilah,Abimana,Abing,Abiogenesis`
    Output: `['Abidin', 'Abilah', 'Abimana', 'Abing', 'Abiogenesis']`
    """
    result = input_string.split(",")
    return result


def _generate_node(
    root: Node,
    graph: graphviz.Graph,
    input: list[str],
    index_list: list[str],
    direction: Optional[str] = "left",
    skip: Optional[int] = 3,
):
    if len(input) == 0:
        return

    if len(input) < (skip + 1):
        if direction == "left":
            prev = root
            for term in input:
                node = Node(value=term, index=index_list.index(term))
                graph.node(term, label=term)

                prev.left = node
                graph.edge(prev.value, term, color="green")

                prev = node
        else:
            reversed_input = input[::-1]

            node = Node(value=reversed_input[0], index=index_list.index(input[0]))
            graph.node(node.value, label=node.value)

            root.right = node
            graph.edge(root.value, node.value, color="red")

            # the rest is always on left
            _generate_node(node, graph, reversed_input[1:], index_list)
    else:
        # left
        new_root_node = Node(value=input[skip], index=index_list.index(input[skip]))
        graph.node(new_root_node.value, label=new_root_node.value)

        if direction == "left":
            root.left = new_root_node
        elif direction == "right":
            root.right = new_root_node
        color = "green"
        if direction == "right":
            color = "red"
        graph.edge(root.value, new_root_node.value, color=color)

        prev = new_root_node
        for i in range(skip):
            idx = skip - i - 1
            node = Node(value=input[idx], index=index_list.index(input[idx]))
            graph.node(node.value, label=node.value)

            prev.left = node
            graph.edge(prev.value, node.value, color="green")

            prev = node

        # right
        _generate_node(
            new_root_node, graph, input[skip + 1 :], index_list, direction="right"
        )


def generate_blocking_tree(
    input: list[str],
    index_list: list[str],
) -> tuple[Node, graphviz.Graph]:
    """
    Input: `['Abidin', 'Abilah', 'Abimana', 'Abing', 'Abiogenesis']`
    Output: The root node of the tree, graphviz.Graph object
    """
    if len(input) == 0:
        return None
    graph = graphviz.Graph(comment="Blocking Tree")
    sorted_input = sorted(input)

    mid = len(sorted_input) // 2
    value = sorted_input[mid]
    root = Node(value=value, index=index_list.index(value))
    graph.node(value, label=value)

    _generate_node(root, graph, sorted_input[:mid], index_list, "left")  # left
    _generate_node(root, graph, sorted_input[mid + 1 :], index_list, "right")  # right

    return root, graph


def _search_tree(term: str, tree: Optional[Node]):
    if tree is not None:
        if term == tree.value:
            return tree
        elif term < tree.value:
            left_node = tree.left
            while left_node is not None:
                if term == left_node.value:
                    return left_node
                else:
                    left_node = left_node.left
        elif term > tree.value:
            return _search_tree(term, tree.right)


def search_bloking_tree(
    term: str,
    tree: Node,
) -> Optional[Node]:
    if tree is None:
        return None

    if term == tree.value:
        return tree
    elif term < tree.value:
        return _search_tree(term, tree.left)
    elif term > tree.value:
        return _search_tree(term, tree.right)
    return None
