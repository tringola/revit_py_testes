"""
Ce code fait plusieurs choses importantes :

Il extrait la géométrie de l'élément en tenant compte de la vue active
Il projette cette géométrie sur le plan de vue
Il récupère le contour extérieur de la projection
Il convertit ce contour en points qui peuvent être utilisés pour créer un polygone Shapely

Points clés à noter :

Il gère à la fois les solides simples et les instances de famille
Il utilise le niveau de détail "Fine" pour obtenir la géométrie la plus précise
Il peut être utilisé avec le code d'analyse géométrique précédent

Pour l'utiliser :

Ouvrez votre projet Revit
Sélectionnez une vue en plan
Sélectionnez l'élément dont vous voulez la projection
Exécutez le script
"""
import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB
from Autodesk.Revit.DB import FilteredElementCollector, ViewPlan
import math

def get_projection_on_level(element, view_plan):
    """
    Obtient la projection 2D d'un élément sur un niveau donné
    
    Args:
        element: L'élément Revit à projeter
        view_plan: La vue en plan (niveau) sur laquelle projeter
    
    Returns:
        Liste de points définissant le contour extérieur de la projection
    """
    # Obtenir la géométrie de l'élément
    opt = Options()
    opt.ComputeReferences = True
    opt.DetailLevel = ViewDetailLevel.Fine
    opt.View = view_plan
    
    geom_elem = element.get_Geometry(opt)
    if geom_elem is None:
        return None
        
    # Obtenir le plan de la vue
    view_plane = Plane.CreateByNormalAndOrigin(
        view_plan.ViewDirection,
        view_plan.Origin
    )
    
    # Liste pour stocker tous les contours
    all_curves = []
    
    def process_solid(solid):
        # Obtenir les faces du solide
        for face in solid.Faces:
            # Projeter la face sur le plan de vue
            projected_face = face.Project(view_plane)
            if projected_face:
                for curve in projected_face.GetEdgesAsCurveLoops():
                    all_curves.extend(curve)
    
    # Parcourir la géométrie
    for geom in geom_elem:
        if isinstance(geom, Solid):
            process_solid(geom)
        elif isinstance(geom, GeometryInstance):
            # Gérer les instances de famille
            geom_instance = geom.GetInstanceGeometry()
            for instance_geom in geom_instance:
                if isinstance(instance_geom, Solid):
                    process_solid(instance_geom)
    
    # Convertir les courbes en points pour créer un polygone
    points = []
    if all_curves:
        # Trouver le contour extérieur
        outer_loop = CurveLoop.Create(all_curves)
        for curve in outer_loop:
            points.append((
                curve.GetEndPoint(0).X,
                curve.GetEndPoint(0).Y
            ))
    
    return points

def export_to_shapely(points):
    """
    Convertit les points en polygone Shapely
    """
    from shapely.geometry import Polygon
    if points and len(points) >= 3:
        return Polygon(points)
    return None

# Exemple d'utilisation dans une macro Revit
def main():
    doc = __revit__.ActiveUIDocument.Document
    uidoc = __revit__.ActiveUIDocument
    
    # Obtenir la vue en plan active
    active_view = doc.ActiveView
    if not isinstance(active_view, ViewPlan):
        print("Veuillez sélectionner une vue en plan")
        return
    
    # Obtenir l'élément sélectionné
    selection = uidoc.Selection
    selected_ids = selection.GetElementIds()
    
    if not selected_ids:
        print("Veuillez sélectionner un élément")
        return
        
    element = doc.GetElement(selected_ids[0])
    
    # Obtenir la projection
    projection_points = get_projection_on_level(element, active_view)
    
    if projection_points:
        # Convertir en polygone Shapely pour analyse ultérieure
        polygon = export_to_shapely(projection_points)
        if polygon:
            print(f"Aire de la projection: {polygon.area}")
            print(f"Périmètre: {polygon.length}")
            # Vous pouvez maintenant utiliser ce polygone avec le code d'analyse 
            # géométrique précédent
    else:
        print("Impossible d'obtenir la projection de cet élément")

if __name__ == '__main__':
    main()
