import p3dutil as pu
from panda3d.core import *
from direct.gui.OnscreenText import OnscreenText


class Text(pu.NodePathUser):
    """
    Class to display text
    """
    def __init__(
            self, 
            p: LVector3f = None, 
            hpr: LVector3f = None, 
            text: str = None,
            scale: float = 0.03, 
            color: LVector4f = None,
            align=TextNode.ACenter, 
            parent: NodePath = None):
        """
        Constructor
        :param p: Position to display the text
        :param hpr: Rotation to display the text - (yaw, pitch, roll)
        :param text: Text to display
        :param scale: Scale of the text (default 1.0)
        :param color: Color of the text (default white = (1,1,1,1) )
        :param align: Alignment of the text (left, center, right... defaults to center)
        :param parent: Optional parent node
        """
        p = p if p is not None else LVector3f(0.07, 0.09, 0.18)
        hpr = hpr if hpr is not None else LVector3f(0, -60, 0)
        color = color if color is not None else LVector4f(1, 1, 1, 1)
        if text is None:
            text = 'TEXT NOT PROVIDED'

        node = OnscreenText(
            text=text,
            pos=p,
            scale=scale,
            fg=color,
            align=align
        )

        np = NodePath(node)

        # enabling this unfortunately does not fix that the text
        # disappears when pitch > ~25 degrees
        # np.setTwoSided(True)

        # this should make text always point at camera?
        # np.setBillboardPointEye()

        super().__init__(np, parent=parent, p=p, r=hpr)
    
    @staticmethod
    def load_json(json_data: dict) -> "Text":
        """
        Create a Text object from JSON data.

        Expected format:

        {
            "type": "text",
            "p": [x, y, z],
            "hpr": [h, p, r],
            "text": "Example",
            "scale": 0.05,
            "color": [1, 1, 1, 1]
        }

        :param json_data: Dictionary loaded from JSON
        :return: Text instance
        :raises RuntimeError: If parsing fails
        """

        p = json_data.get("p")
        hpr = json_data.get("hpr")
        text = json_data.get("text")
        scale = json_data.get("scale")
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
            "text": text,
            "scale": scale,
            "color": color,
        }

        # Remove None values so constructor defaults are preserved
        params = {
            key: value
            for key, value in params.items()
            if value is not None
        }

        return Text(**params)
