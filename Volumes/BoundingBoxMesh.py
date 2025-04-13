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
