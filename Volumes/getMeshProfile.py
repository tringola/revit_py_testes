import math
from Autodesk.Revit.DB import *

def get_mesh_profile(mesh, axe_longitudinal, axe_transversal):
    """
    Extrait le profil d'un Autodesk.Revit.Mesh selon ses axes longitudinal et transversal.
    
    Args:
        mesh (Autodesk.Revit.DB.Mesh): Le maillage Revit dont on veut extraire le profil.
        axe_longitudinal (tuple): Tuple de deux points XYZ définissant l'axe longitudinal.
        axe_transversal (tuple): Tuple de deux points XYZ définissant l'axe transversal.
    
    Returns:
        dict: Dictionnaire avec les clés 'longitudinal' et 'transversal', chacune contenant une liste de tuples (distance, hauteur) représentant le profil du maillage.
    """
    # Récupérer les sommets du maillage
    vertices = [vertex.ToXYZ() for vertex in mesh.Vertices]
    
    # Projeter les sommets sur les axes longitudinal et transversal
    profile_longitudinal = []
    profile_transversal = []
    
    for vertex in vertices:
        # Projection sur l'axe longitudinal
        vect_long = axe_longitudinal[1] - axe_longitudinal[0]
        dist_long = (vertex - axe_longitudinal[0]).DotProduct(vect_long) / vect_long.GetLength()
        height_long = (vertex - axe_longitudinal[0]).CrossProduct(vect_long).GetLength() / vect_long.GetLength()
        profile_longitudinal.append((dist_long, height_long))
        
        # Projection sur l'axe transversal
        vect_trans = axe_transversal[1] - axe_transversal[0]
        dist_trans = (vertex - axe_transversal[0]).DotProduct(vect_trans) / vect_trans.GetLength()
        height_trans = (vertex - axe_transversal[0]).CrossProduct(vect_trans).GetLength() / vect_trans.GetLength()
        profile_transversal.append((dist_trans, height_trans))
    
    return {
        'longitudinal': profile_longitudinal,
        'transversal': profile_transversal
    }

# Exemple d'utilisation
# mesh = Autodesk.Revit.DB.Mesh.CreateFromGeometry(géométrie_revit)
# axe_longitudinal, axe_transversal = get_mesh_axes(mesh)
# profils = get_mesh_profile(mesh, axe_longitudinal, axe_transversal)
