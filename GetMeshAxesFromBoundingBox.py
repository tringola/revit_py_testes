import math
from Autodesk.Revit.DB import *

def get_mesh_axes(mesh):
    """
    Extrait les axes longitudinaux et transversaux d'un Autodesk.Revit.Mesh à partir de son bounding box.
    
    Args:
        mesh (Autodesk.Revit.DB.Mesh): Le maillage Revit dont on veut extraire les axes.
    
    Returns:
        tuple: (axe_longitudinal, axe_transversal), où chaque axe est un tuple (point_départ, point_fin)
    """
    # Récupérer la boîte englobante du maillage
    bbox = mesh.GetBoundingBox()
    min_point = bbox.Min
    max_point = bbox.Max
    
    # Calculer la longueur, largeur et hauteur du volume
    length = max_point.X - min_point.X
    width = max_point.Y - min_point.Y
    height = max_point.Z - min_point.Z
    
    # Déterminer l'axe longitudinal (le plus long)
    if length >= width and length >= height:
        axe_longitudinal = (
            XYZ(min_point.X, min_point.Y, min_point.Z),
            XYZ(max_point.X, min_point.Y, min_point.Z)
        )
    elif width >= length and width >= height:
        axe_longitudinal = (
            XYZ(min_point.X, min_point.Y, min_point.Z),
            XYZ(min_point.X, max_point.Y, min_point.Z)
        )
    else:
        axe_longitudinal = (
            XYZ(min_point.X, min_point.Y, min_point.Z),
            XYZ(min_point.X, min_point.Y, max_point.Z)
        )
    
    # Déterminer l'axe transversal (le plus court)
    if length <= width and length <= height:
        axe_transversal = (
            XYZ(min_point.X, min_point.Y, min_point.Z),
            XYZ(max_point.X, min_point.Y, min_point.Z)
        )
    elif width <= length and width <= height:
        axe_transversal = (
            XYZ(min_point.X, min_point.Y, min_point.Z),
            XYZ(min_point.X, max_point.Y, min_point.Z)
        )
    else:
        axe_transversal = (
            XYZ(min_point.X, min_point.Y, min_point.Z),
            XYZ(min_point.X, min_point.Y, max_point.Z)
        )
    
    return (axe_longitudinal, axe_transversal)

# Exemple d'utilisation
# mesh = Autodesk.Revit.DB.Mesh.CreateFromGeometry(géométrie_revit)
# axe_longitudinal, axe_transversal = get_mesh_axes(mesh)
