import p3dutil as pu
from panda3d.core import *
import math

class CurvedIdealLine(pu.NodePathUser):
    def __init__(
        self,
        p=None,
        hpr=None,
        length=0.2,
        pre_length=0.05,
        lateral=0.08,
        thickness=8,
        color=None,
        parent=None,
        segments=50,
        curve_bias=2.0,
        turn_direction=-1
    ):
        p = p if p is not None else LVector3f(0.30, -0.10, 0.0)
        hpr = hpr if hpr is not None else LVector3f(0, 0, 0)
        color = color if color is not None else LVector4f(1, 0, 0, 1)

        lines = LineSegs()
        lines.setThickness(thickness)
        lines.setColor(color)

        total_length = length + pre_length
        t_origin = pre_length / total_length
        smooth_origin = 1 - (1 - t_origin) ** curve_bias
        x_scale = 1 - smooth_origin   # guarantees x == lateral at t=1

        first = True
        for i in range(segments + 1):
            t = i / segments
            smooth = 1 - (1 - t) ** curve_bias
            x = turn_direction * lateral * (smooth - smooth_origin) / x_scale
            y = total_length * t - pre_length

            if first:
                lines.moveTo(x, -y, 0)
                first = False
            else:
                lines.drawTo(x, -y, 0)

        node = lines.create(False)
        np = NodePath(node)
        super().__init__(np, parent=parent, p=p, r=hpr)

    def set_lateral(self, error_mm):
        self.lateral = error_mm
        self.turn_direction = -1 if error_mm > 0 else 1
