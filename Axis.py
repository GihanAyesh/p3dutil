import p3dutil as pu
from panda3d.core import *


class Axis(pu.NodePathUser):
    """
    Simple class to display a coordinate axis
    """

    def __init__(
        self, 
        p: LVector3f = None, 
        mat: LMatrix4 = None, 
        size=0.5, 
        thickness=3,
        parent: NodePath = None, 
        axis=None
        ):
        """
        Constructor
        :param p: Position to display the coordinate axis
        :param mat: Matrix to place the coordinate axis (optional)
        :param size: Size of the axis (total width, height, depth, default=10)
        :param thickness: Line thickness (default=3)
        :param parent: Optional parent to set for the node
        """
        axis = axis if axis is not None else LVector3f(1, -1, 1)
        lines = LineSegs()
        lines.setThickness(thickness)
        lines.setColor(LVecBase4f(1, 0, 0, 1))
        lines.moveTo(0, 0, 0)
        lines.drawTo(axis[0] * size, 0, 0)

        lines.setColor(LVecBase4f(0, 1, 0, 1))
        lines.moveTo(0, 0, 0)
        lines.drawTo(0, axis[1] * size, 0)

        lines.setColor(LVecBase4f(0, 0, 1, 1))
        lines.moveTo(0, 0, 0)
        lines.drawTo(0, 0, axis[2] * size)

        node = lines.create(False)
        np = NodePath(node)
        super().__init__(np, parent=parent, p=p, mat=mat)

    @staticmethod
    def load_json(json_data: dict) -> "Axis":
        """
        Create an Axis object from JSON data.

        Expected format:

        {
            "type": "axis",
            "p": [x, y, z],
            "axis": [x, y, z],
            "size": float,
            "thickness": float
        }

        :param json_data: Dictionary loaded from JSON
        :return: Axis instance
        :raises RuntimeError: If parsing fails
        """

        p = json_data.get("p")
        axis = json_data.get("axis")
        size = json_data.get("size")
        thickness = json_data.get("thickness")

        try:
            p = LVecBase3f(*p) if p else None
        except Exception as e:
            raise RuntimeError(f"Error loading `p` for Axis:\n{e}")

        try:
            axis = LVecBase3f(*axis) if axis else None
        except Exception as e:
            raise RuntimeError(f"Error loading `axis` for Axis:\n{e}")

        params = {
            "p": p,
            "axis": axis,
            "size": size,
            "thickness": thickness,
        }

        # Remove None values so constructor defaults are preserved
        params = {
            key: value
            for key, value in params.items()
            if value is not None
        }

        return Axis(**params)
