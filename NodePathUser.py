from abc import ABC
from typing import overload
from panda3d.core import *


class NodePathUser(ABC):
    """
    Base closs for classes that uses a Panda3d NodePath
    """
    def __init__(self, node: NodePath, p: LVector3 = None, mat: LMatrix4 = None, parent:NodePath=None):
        self._node = node

        if parent:
            self.reparentTo(parent)

        if p:
            self.setPos(p)

        if mat:
            self.setMat(mat)

    def reparentTo(self, parent: NodePath):
        """
        Reparent the actor to a renderer
        :param parent: New parent to set
        """
        self._node.reparentTo(parent)


    def setPos(self, *args):
        self._node.setPos(*args)

    def setMat(self, mat: LMatrix4):
        self._node.setMat(mat)

    def setHpr(self, *args):
        """
        Sets the rotation component of the transform
        Heading, Pitch, and Roll
        """
        self._node.setHpr(args)

    @property
    def node(self) -> NodePath:
        """
        Node property - gets the node path we are using
        :return:
        """
        return self._node
