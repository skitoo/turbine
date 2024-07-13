from typing import TYPE_CHECKING, Optional

import pyray

from turbine.error import TurbineError

if TYPE_CHECKING:
    from .tree import SceneTree


class Node:
    def __init__(self):
        self.__children: set[Node] = set()
        self.__parent: Node | None = None
        self.__tree: Optional["SceneTree"] = None
        self.init()

    def init(self):
        pass

    @property
    def is_root(self) -> bool:
        return self.__parent is None and self.__tree is not None

    def add_child(self, node: "Node"):
        if node.is_root:
            raise TurbineError("This node is root. It cannot be add to another node")
        if node.__parent:
            node.__parent.remove_child(node)
        node.__parent = self
        self.__children.add(node)
        if self.__tree:
            node._enter()

    def remove_child(self, node: "Node"):
        if node not in self.__children:
            raise TurbineError("Node is not a child of current node")
        node.__parent = None
        self.__children.remove(node)
        self._exit()

    @property
    def children(self) -> set["Node"]:
        return self.__children

    @property
    def parent(self) -> Optional["Node"]:
        return self.__parent

    def get_tree(self) -> Optional["SceneTree"]:
        if self.__tree:
            return self.__tree
        if self.parent:
            return self.parent.get_tree()
        return None

    def set_tree(self, tree: "SceneTree"):
        self.__tree = tree
        self._enter()

    def _enter(self):
        self.enter()
        for child in self.__children:
            child._enter()

    def enter(self):
        pass

    def _exit(self):
        self.exit()
        for child in self.__children:
            child._exit()

    def exit(self):
        pass

    def _update(self, dt: float):
        self.update(dt)
        for child in self.__children:
            child._update(dt)

    def _render(self):
        self.render()
        for child in self.__children:
            child._render()

    def update(self, dt: float):
        pass

    def render(self):
        pass


class Node2D(Node):
    def __init__(self):
        self.position = pyray.vector2_zero()
        self.scale = pyray.vector2_one()
        self.rotation = 0.0
        self.visible = True
        super().__init__()

    def _render(self):
        if self.visible:
            super()._render()

    @property
    def global_position(self) -> pyray.Vector2:
        if isinstance(self.parent, Node2D):
            return pyray.vector2_add(self.parent.global_position, self.position)
        return self.position


class Sprite(Node2D):
    def __init__(self):
        self.center = pyray.vector2_zero()
        super().__init__()

    def set_image_path(self, image_path: str):
        self.__image_path = image_path
        self.image = pyray.load_texture(self.__image_path)
        self.rect = pyray.Rectangle(0, 0, self.image.width, self.image.height)

    def render(self):
        node_tree = self.get_tree()
        if node_tree:
            pyray.draw_texture_pro(
                self.image,
                self.rect,
                pyray.Rectangle(
                    self.global_position.x,
                    self.global_position.y,
                    self.image.width * self.scale.x,
                    self.image.height * self.scale.y,
                ),
                self.center,
                self.rotation,
                pyray.WHITE,
            )
            pyray.draw_circle(
                int(self.global_position.x), int(self.global_position.y), 2, pyray.BLUE
            )
