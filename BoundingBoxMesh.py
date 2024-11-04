import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

def get_mesh_bbox(mesh):
    """
    Retourne le bounding box d'un Autodesk.Revit.DB.Mesh
    
    Args:
        mesh: Autodesk.Revit.DB.Mesh - L'objet mesh Revit
        
    Returns:
        BoundingBoxXYZ - Le bounding box du mesh
    """
    # Obtenir tous les points du mesh
    vertices = mesh.Vertices
    
    # Initialiser les min/max avec le premier point
    min_x = max_x = vertices[0].X
    min_y = max_y = vertices[0].Y
    min_z = max_z = vertices[0].Z
    
    # Parcourir tous les points pour trouver les min/max
    for vertex in vertices:
        min_x = min(min_x, vertex.X)
        max_x = max(max_x, vertex.X)
        min_y = min(min_y, vertex.Y)
        max_y = max(max_y, vertex.Y)
        min_z = min(min_z, vertex.Z)
        max_z = max(max_z, vertex.Z)
    
    # Créer les points min et max
    min_point = XYZ(min_x, min_y, min_z)
    max_point = XYZ(max_x, max_y, max_z)
    
    # Créer et retourner le bounding box
    bbox = BoundingBoxXYZ()
    bbox.Min = min_point
    bbox.Max = max_point
    
    return bbox
def get_solid_bbox(solid):
    """
    Retourne le bounding box d'un solide Revit
    
    Args:
        solid: Autodesk.Revit.DB.Solid
    Returns:
        BoundingBoxXYZ
    """
    # Obtenir le BoundingBox directement du solide
    bbox = solid.GetBoundingBox()
    
    # Convertir en BoundingBoxXYZ global si nécessaire
    if bbox is not None:
        global_bbox = BoundingBoxXYZ()
        global_bbox.Min = bbox.Transform.OfPoint(bbox.Min)
        global_bbox.Max = bbox.Transform.OfPoint(bbox.Max)
        return global_bbox
    return None


def create_bbox_solid(doc, bbox, material_id=None):
    """
    Crée un solide 3D représentant le bounding box
    """
    min_pt = bbox.Min
    max_pt = bbox.Max
    
    # Créer le profil rectangulaire
    profile_points = [
        XYZ(min_pt.X, min_pt.Y, min_pt.Z),
        XYZ(max_pt.X, min_pt.Y, min_pt.Z),
        XYZ(max_pt.X, max_pt.Y, min_pt.Z),
        XYZ(min_pt.X, max_pt.Y, min_pt.Z)
    ]
    
    # Créer la boucle de courbes
    profile_loop = CurveLoop()
    for i in range(4):
        line = Line.CreateBound(profile_points[i], profile_points[(i + 1) % 4])
        profile_loop.Append(line)
    
    # Créer le solide par extrusion
    height = max_pt.Z - min_pt.Z
    solid_options = SolidOptions(ElementId.InvalidElementId, ElementId.InvalidElementId)
    
    extrusion = GeometryCreationUtilities.CreateExtrusionGeometry(
        [profile_loop],
        XYZ(0, 0, 1),
        height,
        solid_options
    )
    
    # Créer le DirectShape
    category_id = ElementId(BuiltInCategory.OST_GenericModel)
    ds = DirectShape.CreateElement(doc, category_id)
    ds.SetShape([extrusion])
    
    if material_id is not None:
        ds.SetMaterialId(material_id)
    
    return ds

# Exemple d'utilisation
def example_usage():
    # Supposons que nous avons déjà un élément mesh
    # mesh = some_revit_element.Geometry[0]
    bbox = get_mesh_bbox(mesh)
    
    # Accéder aux dimensions du bounding box
    width = bbox.Max.X - bbox.Min.X
    height = bbox.Max.Y - bbox.Min.Y
    depth = bbox.Max.Z - bbox.Min.Z
    
    print(f"Dimensions du mesh:")
    print(f"Largeur: {width}")
    print(f"Hauteur: {height}")
    print(f"Profondeur: {depth}")
