import p3dutil as pu
from panda3d.core import *


class Arrow(pu.NodePathUser):
    """
    Class to display a very simple arrow
    """

    def __init__(self, p: LVector3f = None, r: LVector3f = None,
                 length=0.1, thickness=0.01, color: LVector4f = LVector4f(1, 1, 1, 1),
                 parent: NodePath = None, ):
        """
        Constructor
        :param p: Position to display the arrow. Should be the point of the array
        :param length: Length of the arrow - SHOULD BE IN INTERVAL [0.0, 1.0]!
        :param thickness: Thickness of the arrow - SHOULD BE IN INTERVAL [0.0, 1.0]!
        :param color: Color of the arrow
        :param parent: Parent node (optional)
        """
        # Create the shaft (rectangle)
        shaft = self.create_rectangle(width=thickness, height=length)
        # shaft.setColor(color)

        # Create the head (triangle)
        base_scale = thickness * 3
        height_scale = thickness * 3
        head = self.create_triangle(base=base_scale, height=height_scale)
        # head.setColor(color)

        # Create a parent NodePath to hold the arrow components
        np = NodePath("Arrow-" + str(id(self)))  # make sure all arrow node names unique
        shaft.reparentTo(np)
        head.reparentTo(np)

        # Call the parent constructor
        super().__init__(np, parent=parent, p=p, r=r)

    def create_rectangle(self, width, height):
        # Create a rectangle for the arrow shaft
        format = GeomVertexFormat.getV3()
        vdata = GeomVertexData("rectangle", format, Geom.UHStatic)
        vertex = GeomVertexWriter(vdata, "vertex")

        # Define the rectangle vertices
        half_width = width / 2
        vertex.addData3(-half_width, 0, -height)  # Bottom left
        vertex.addData3(half_width, 0, -height)  # Bottom right
        vertex.addData3(half_width, 0, 0)  # Top right
        vertex.addData3(-half_width, 0, 0)  # Top left

        # Create the rectangle's geometry
        geom = Geom(vdata)
        # Define the rectangle's triangles (two triangles)
        tri1 = GeomTriangles(Geom.UHStatic)
        tri1.addVertices(0, 1, 2)  # First triangle
        tri1.addVertices(0, 2, 3)  # Second triangle
        geom.addPrimitive(tri1)

        node = GeomNode("rectangle")
        node.addGeom(geom)
        return NodePath(node)

    def create_triangle(self, base, height):
        # Create a triangle for the arrow head
        format = GeomVertexFormat.getV3()
        vdata = GeomVertexData("triangle", format, Geom.UHStatic)
        vertex = GeomVertexWriter(vdata, "vertex")

        # Define the triangle vertices
        vertex.addData3(0, 0, height)  # Tip of the triangle
        vertex.addData3(-base / 2, 0, 0)  # Bottom left
        vertex.addData3(base / 2, 0, 0)  # Bottom right

        # Create the triangle's geometry
        geom = Geom(vdata)
        tri = GeomTriangles(Geom.UHStatic)
        tri.addVertices(0, 1, 2)  # Single triangle
        geom.addPrimitive(tri)

        node = GeomNode("triangle")
        node.addGeom(geom)
        return NodePath(node)
