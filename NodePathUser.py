from abc import ABC
from typing import overload
from panda3d.core import *


class NodePathUser(ABC):
    """
    Base class for classes that uses a Panda3d NodePath
    """
    def __init__(self, node: NodePath, p: LVector3 = None, r: LVector3f = None,
                 mat: LMatrix4 = None, parent: NodePath = None):
        """
        Constructor
        node: Panda3d Node
        p: position vector (optional
        r: rotation vector (heading/yaw, pitch, roll - optional)
        mat: transformation matrix (optional)
        parent: parent Panda3d Node
        """
        self._node = node

        if parent:
            self.reparentTo(parent)

        if p:
            self.setPos(p)

        if r:
            self.setHpr(r)

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

    def setHpr(self, r: LVector3f = None):
        """
        Sets the rotation component of the transform
        Heading, Pitch, and Roll
        """
        if r:
            self._node.setHpr(r.x, r.y, r.z)

    @property
    def node(self) -> NodePath:
        """
        Node property - gets the node path we are using
        :return:
        """
        return self._node
