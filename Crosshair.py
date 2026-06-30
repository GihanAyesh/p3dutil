import p3dutil as pu
from panda3d.core import *


import p3dutil as pu
from panda3d.core import *


class Crosshair(pu.NodePathUser):
    """
    X-shaped crosshair centered at position p.
    """

    def __init__(
        self,
        p=None,
        size=0.02,
        thickness=3,
        color=LVector4f(0, 0, 0, 1),
        parent=None
    ):
        """
        :param p: Center position of the crosshair
        :param size: Total width/height of the X
        :param thickness: Line thickness
        :param color: Line color
        :param parent: Optional parent NodePath
        """

        lines = LineSegs()
        lines.setThickness(thickness)
        lines.setColor(color)

        half = size / 2

        # First diagonal (\)
        lines.moveTo(-half, 0, -half)
        lines.drawTo(+half, 0, +half)

        # Second diagonal (/)
        lines.moveTo(-half, 0, +half)
        lines.drawTo(+half, 0, -half)

        node = lines.create()
        np = NodePath(node)

        super().__init__(
            np,
            parent=parent,
            p=p
        )

