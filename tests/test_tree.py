from unittest.mock import Mock

from turbine.node import Node
from turbine.tree import SceneTree


def test_scene_tree_init():
    tree = SceneTree(Mock())
    assert tree.get_current_scene() is None
    assert tree.groups == set()


def test_scene_tree_set_current_scene():
    tree1 = SceneTree(Mock())
    tree2 = SceneTree(Mock())
    node = Node()
    tree1.set_current_scene(node)
    assert tree1.get_current_scene() == node
    assert node.get_tree() == tree1

    tree2.set_current_scene(node)
    assert tree2.get_current_scene() == node
    assert tree1.get_current_scene() is None
    assert node.get_tree() == tree2


def test_scene_tree_add_to_group():
    tree = SceneTree(Mock())
    node1 = Node()
    node2 = Node()
    node3 = Node()
    tree.add_to_group("player", node1)
    tree.add_to_group("ennemies", node2)
    tree.add_to_group("ennemies", node3)

    assert tree.has_group("player")
    assert tree.has_group("ennemies")
    assert tree.get_nodes_by_group("player") == {node1}
    assert tree.get_nodes_by_group("ennemies") == {node2, node3}
    assert tree.groups == {"player", "ennemies"}


def test_scene_tree_remove_from_group():
    tree = SceneTree(Mock())
    node1 = Node()
    node2 = Node()
    tree.add_to_group("player", node1)
    tree.add_to_group("all", node1)
    tree.add_to_group("all", node2)

    tree.remove_from_group("player", node1)

    assert not tree.has_group("player")
    assert tree.has_group("all")
    assert tree.get_nodes_by_group("player") == set()
    assert tree.get_nodes_by_group("all") == {node1, node2}
    assert tree.groups == {"all"}
