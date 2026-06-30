import p3dutil as pu
from panda3d.core import *


class Arrow(pu.NodePathUser):
    """
    Class to display a very simple 2D arrow
    """

    def __init__(
            self, 
            p: LVector3f = None, 
            hpr: LVector3f = None, 
            length=0.1, 
            thickness=0.01,
            color: LVector4f = LVector4f(1, 1, 1, 1), 
            parent: NodePath = None):
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
        shaft.setColor(color)

        # Create the head (triangle)
        base_scale = thickness * 3
        height_scale = thickness * 3
        head = self.create_triangle(base=base_scale, height=height_scale)
        head.setColor(color)

        # Create a parent NodePath to hold the arrow components
        np = NodePath("Arrow-" + str(id(self)))  # make sure all arrow node names unique
        shaft.reparentTo(np)
        head.reparentTo(np)

        # Call the parent constructor
        super().__init__(np, parent=parent, p=p, r=hpr)

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
    
    @staticmethod
    def load_json(json_data: dict) -> "Arrow":
        """
        Loads Arrow NodePathUser from p3dutil from json data.
        Format should be as in main docstring, with additional optional
        attributes as follows:

        {
            "type": "arrow",
            ...
            "thickness": <float for arrow thickness/"girth" in meters>,
            "length": <float for arrow length in meters>,
        }

        :exception RuntimeError: if loading fails
        :return: p3dutils Arrow NodePathUser
        """
        p = json_data.get("p")
        hpr = json_data.get("hpr")
        length = json_data.get("length")
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

        # build params dict, but then remove all the keys with "None" as value,
        # then we can unpack "params" as the kwargs and let the Text constructor
        # handle defaults.
        params = {
            "p": p,
            "hpr": hpr,
            "length": length,
            "thickness": thickness,
            "color": color,
        }
        params = {key: value for key, value in params.items() if value is not None}
        return Arrow(**params)
