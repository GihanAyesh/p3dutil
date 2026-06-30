import p3dutil as pu
from panda3d.core import *
import math


class CurvedDoubleLine(pu.NodePathUser):
    """
    Parallel curved lines using spline-sampled offset curves.
    """

    def __init__(
        self,
        p=None,
        hpr=None,
        radius_x=0.2,
        radius_y=0.5,
        angle_deg=90,
        separation=0.02,
        thickness=3,
        color=LVector4f(1, 1, 1, 1),
        parent=None,
        segments=120,
        curve_bias=1.0,
        turn_direction = -1,
    ):

        lines = LineSegs()
        lines.setThickness(thickness)
        lines.setColor(color)

        angle_rad = math.radians(angle_deg)

        base = []

        for i in range(segments + 1):
            t = i / segments
            theta = (t ** curve_bias) * angle_rad

            x = turn_direction * radius_x * (1 - math.cos(theta))
            y =  radius_y * math.sin(theta)
            base.append((x, y))

        tangents = []

        for i in range(len(base)):
            if i == 0:
                dx = base[1][0] - base[0][0]
                dy = base[1][1] - base[0][1]
            elif i == len(base) - 1:
                dx = base[-1][0] - base[-2][0]
                dy = base[-1][1] - base[-2][1]
            else:
                dx = base[i + 1][0] - base[i - 1][0]
                dy = base[i + 1][1] - base[i - 1][1]

            length = math.sqrt(dx * dx + dy * dy)
            tangents.append((dx / length, dy / length))

        for side in (-1, 1):

            offset = side * separation * 0.5
            first = True

            for i in range(len(base)):

                cx, cy = base[i]
                tx, ty = tangents[i]

                nx = -ty
                ny = tx

                nlen = math.sqrt(nx * nx + ny * ny)
                nx /= nlen
                ny /= nlen

                x = cx + nx * offset
                y = cy + ny * offset
                z = 0

                if first:
                    lines.moveTo(x, y, z)
                    first = False
                else:
                    lines.drawTo(x, y, z)

        node = lines.create(False)
        np = NodePath(node)

        super().__init__(np, parent=parent, p=p, r=hpr)
    
    @staticmethod
    def load_json(json_data: dict) -> "CurvedDoubleLine":
        """
        Loads DoubleCurve NodePathUser from json data.

        Example JSON:
        {    
            "type": "curve_double",
            "p": [0, 0, 0],
            "hpr": [0, 0, 0],
            "radius_x": 10.0,
            "radius_y: 10.0,
            "length": 1.0,
            "angle_deg": 45,
            "separation": 0.05,
            "thickness": 3,
            "color": [1, 1, 1, 1],
            "segments": 100,
            "amplitude": 0.1,
            "turn_direction": -1
        }
        """

        p = json_data.get("p", None)
        hpr = json_data.get("hpr", None)
        radius_x = json_data.get("radius_x", None)
        radius_y = json_data.get("radius_y", None)
        length = json_data.get("length", None)
        angle_deg = json_data.get("angle_deg", None)
        separation = json_data.get("separation", None)
        thickness = json_data.get("thickness", None)
        color = json_data.get("color", None)
        turn_direction = json_data.get("turn_direction", None)

        # New curve params
        segments = json_data.get("segments", None)
        amplitude = json_data.get("amplitude", None)

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
            "radius_x": radius_x,
            "radius_y": radius_y,
            "length": length,
            "angle_deg" : angle_deg,
            "separation": separation,
            "thickness": thickness,
            "color": color,
            "segments": segments,
            "amplitude": amplitude,
            "turn_direction": turn_direction
        }

        # Remove None values (same as your pattern)
        params = {k: v for k, v in params.items() if v is not None}

        return CurvedDoubleLine(**params)