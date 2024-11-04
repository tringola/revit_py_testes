import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *

def draw_bbox(doc, bbox, view3D=None):
    """
    Dessine un bounding box dans la vue 3D active en utilisant des lignes de modèle
    
    Args:
        doc: Document Revit actif
        bbox: BoundingBoxXYZ à dessiner
        view3D: Vue 3D spécifique (optionnel)
    """
    # Si aucune vue 3D n'est spécifiée, prendre la vue 3D active
    if view3D is None:
        view3D = doc.ActiveView
        if not isinstance(view3D, View3D):
            raise Exception("La vue active n'est pas une vue 3D")

    # Points du bounding box
    min_pt = bbox.Min
    max_pt = bbox.Max
    
    # Créer tous les points des coins
    corners = [
        XYZ(min_pt.X, min_pt.Y, min_pt.Z), # 0
        XYZ(max_pt.X, min_pt.Y, min_pt.Z), # 1
        XYZ(max_pt.X, max_pt.Y, min_pt.Z), # 2
        XYZ(min_pt.X, max_pt.Y, min_pt.Z), # 3
        XYZ(min_pt.X, min_pt.Y, max_pt.Z), # 4
        XYZ(max_pt.X, min_pt.Y, max_pt.Z), # 5
        XYZ(max_pt.X, max_pt.Y, max_pt.Z), # 6
        XYZ(min_pt.X, max_pt.Y, max_pt.Z)  # 7
    ]
    
    # Définir les lignes à créer (paires d'indices de points)
    lines_indices = [
        (0,1), (1,2), (2,3), (3,0),  # Base inférieure
        (4,5), (5,6), (6,7), (7,4),  # Base supérieure
        (0,4), (1,5), (2,6), (3,7)   # Lignes verticales
    ]
    
    # Démarrer une transaction
    with Transaction(doc, "Dessiner Bounding Box") as trans:
        trans.Start()
        
        # Créer une ligne de modèle pour chaque arête
        for start_idx, end_idx in lines_indices:
            start_point = corners[start_idx]
            end_point = corners[end_idx]
            line = Line.CreateBound(start_point, end_point)
            ModelCurve.Create(doc, line, view3D.GenLevel.Id)
            
        trans.Commit()

# Exemple d'utilisation
def example_usage():
    """
    Exemple d'utilisation pour dessiner le bounding box d'un mesh
    """
    uidoc = __revit__.ActiveUIDocument  # Accessible dans l'environnement Revit
    doc = uidoc.Document
    
    # Sélectionner un élément
    selection = uidoc.Selection
    selected_element = doc.GetElement(selection.GetElementIds()[0])
    
    # Obtenir le mesh (supposons que c'est le premier élément de géométrie)
    geom_elem = selected_element.get_Geometry(Options())
    mesh = next(geom for geom in geom_elem if isinstance(geom, Mesh))
    
    # Obtenir et dessiner le bounding box
    bbox = get_mesh_bbox(mesh)  # Utilise la fonction précédente
    draw_bbox(doc, bbox)
