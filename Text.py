import p3dutil as pu
from panda3d.core import *
from direct.gui.OnscreenText import OnscreenText


class Text(pu.NodePathUser):
    """
    Class to display text
    """
    def __init__(self, p: LVector3f = None, r: LVector3f = None,
                 text: str = None, scale: float = 0.07, color: LVector4f = LVector4f(1, 1, 1, 1),
                 align=TextNode.ACenter, parent: NodePath = None):
        """
        Constructor
        :param p: Position to display the text
        :param r: Rotation to display the text - (yaw, pitch, roll)
        :param text: Text to display
        :param scale: Scale of the text (default 1.0)
        :param color: Color of the text (default white = (1,1,1,1) )
        :param align: Alignment of the text (left, center, right... defaults to center)
        :param parent: Optional parent node
        """
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

        super().__init__(np, parent=parent, p=p, r=r)
