from unittest.mock import Mock

import pytest

from turbine.error import TurbineError
from turbine.node import Node
from turbine.tree import SceneTree


def test_node_init():
    node = Node()
    assert node.get_tree() is None
    assert node.parent is None
    assert node.children == set()


def test_node_with_tree():
    tree = SceneTree(Mock())
    node1 = Node()
    node2 = Node()
    node3 = Node()
    node1.add_child(node2)
    node1.add_child(node3)
    tree.set_current_scene(node1)

    assert node1.get_tree() == tree
    assert node2.get_tree() == tree
    assert node3.get_tree() == tree
    assert node1.parent is None
    assert node2.parent == node1
    assert node3.parent == node1
    assert node1.children == {node2, node3}

    node2.add_child(node3)
    assert node3.get_tree() == tree
    assert node3.parent == node2
    assert node1.children == {node2}
    assert node2.children == {node3}


def test_node_is_root():
    node1, node2, node3 = Node(), Node(), Node()
    tree = SceneTree(Mock())
    tree.set_current_scene(node1)
    node1.add_child(node2)
    assert node1.is_root
    assert not node2.is_root
    assert not node3.is_root


def test_node_add_child_when_is_root():
    node1, node2, node3 = Node(), Node(), Node()
    tree = SceneTree(Mock())
    tree.set_current_scene(node1)
    node1.add_child(node2)
    node1.add_child(node3)
    with pytest.raises(TurbineError):
        node3.add_child(node1)


def test_node_remove_child():
    node1, node2, node3 = Node(), Node(), Node()
    tree = SceneTree(Mock())
    tree.set_current_scene(node1)
    node1.add_child(node2)
    node2.add_child(node3)

    node1.remove_child(node2)
    assert node1.children == set()
    assert node2.parent is None
    assert node3.parent == node2
    assert node2.get_tree() is None
    assert node3.get_tree() is None


def test_node_remove_child_not_found():
    node1, node2, node3 = Node(), Node(), Node()
    tree = SceneTree(Mock())
    tree.set_current_scene(node1)
    node1.add_child(node2)
    with pytest.raises(TurbineError):
        node1.remove_child(node3)
