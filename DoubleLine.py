import p3dutil as pu
from panda3d.core import *

class DoubleLine(pu.NodePathUser):
    """
    Draw two continuous parallel lines
    """
    def __init__(
        self,
        p=None,
        hpr=None,
        length=0.2,
        separation=0.04,
        thickness=8,
        color=None,
        parent=None,
        dash_length=0.02,
        gap_length=0.01
    ):
        p = p if p is not None else LVector3f(0.30, -0.10, 0.0)
        hpr = hpr if hpr is not None else LVector3f(0, -90, 0)
        color = color if color is not None else LVector4f(0, 1, 0, 0)

        lines = LineSegs()
        lines.setThickness(thickness)
        lines.setColor(color)

        for x_offset in (-separation / 2, separation / 2):
            z = 0.0

            while z > -length:

                dash_end = max(z - dash_length, -length)

                lines.moveTo(x_offset, 0, z)
                lines.drawTo(x_offset, 0, dash_end)

                z -= dash_length + gap_length

        node = lines.create(False)
        np = NodePath(node)

        super().__init__(np, parent=parent, p=p, r=hpr)
    
    @staticmethod
    def load_json(json_data: dict) -> "DoubleLine":
        """
        Loads DoubleLine NodePathUser from json data.
        Format should be as in main docstring, with additional optional
        attributes as follows:

        {
            "type": "double_line",
            ...
            "thickness": <float for line thickness>,
            "length": <float for total line length in meters>,
            "separation": <float for distance between the two parallel lines>,
            "color": [r, g, b, a]
        }

        :exception RuntimeError: if loading fails
        :return: DoubleLine NodePathUser
        """
        p = json_data.get("p")
        hpr = json_data.get("hpr")
        length = json_data.get("length")
        separation = json_data.get("separation")
        thickness = json_data.get("thickness")
        color = json_data.get("color")

        try:
            p = LVecBase3f(*p) if p else None
        except Exception as e:
            raise RuntimeError(f"Error loading `p` for Text:\n{e}")

        try:
            hpr = LVecBase3f(*hpr) if hpr else None
        except Exception as e:
            raise RuntimeError(f"Error loading `hpr` for Text:\n{e}")

        try:
            color = LVecBase4f(*color) if color else None
        except Exception as e:
            raise RuntimeError(f"Error loading `color` for Text:\n{e}")

        params = {
            "p": p,
            "hpr": hpr,
            "length": length,
            "separation": separation,
            "thickness": thickness,
            "color": color,
        }
        params = {key: value for key, value in params.items() if value is not None}
        return DoubleLine(**params)