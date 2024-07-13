from typing import TYPE_CHECKING

from .node import Node

if TYPE_CHECKING:
    from turbine.engine import Turbine


class SceneTree:
    def __init__(self, turbine: "Turbine"):
        self.__turbine = turbine
        self.__current_scene: Node | None = None
        self.__groups: dict[str, set[Node]] = {}

    def set_current_scene(self, node: Node):
        node_tree = node.get_tree()
        if node_tree:
            node_tree.__current_scene = None
        self.__current_scene = node
        node.set_tree(self)

    def get_current_scene(self) -> Node | None:
        return self.__current_scene

    def has_group(self, name: str) -> bool:
        return name in self.__groups

    def get_nodes_by_group(self, name: str) -> set[Node]:
        if name not in self.__groups:
            return set()
        return self.__groups[name]

    def add_to_group(self, name: str, node: Node):
        if name not in self.__groups:
            self.__groups[name] = set()
        self.__groups[name].add(node)

    def remove_from_group(self, name: str, node: Node):
        if name in self.__groups:
            self.__groups[name].remove(node)
            if len(self.__groups[name]) == 0:
                del self.__groups[name]

    @property
    def groups(self) -> set[str]:
        return set(self.__groups.keys())

    def update(self, dt: float):
        if self.__current_scene:
            self.__current_scene._update(dt)

    def render(self):
        if self.__current_scene:
            self.__current_scene._render()
