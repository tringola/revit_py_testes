import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *

def create_bbox_solid(doc, bbox, material_id=None):
    """
    Crée un solide 3D représentant le bounding box
    
    Args:
        doc: Document Revit actif
        bbox: BoundingBoxXYZ à transformer en solide
        material_id: ElementId du matériau à appliquer (optionnel)
    
    Returns:
        DirectShape: L'élément DirectShape créé
    """
    # Points du bounding box
    min_pt = bbox.Min
    max_pt = bbox.Max
    
    # Créer le profil de base (rectangle)
    profile_points = [
        XYZ(min_pt.X, min_pt.Y, min_pt.Z),
        XYZ(max_pt.X, min_pt.Y, min_pt.Z),
        XYZ(max_pt.X, max_pt.Y, min_pt.Z),
        XYZ(min_pt.X, max_pt.Y, min_pt.Z)
    ]
    
    # Créer une CurveLoop pour le profil
    profile_loop = CurveLoop()
    for i in range(4):
        start_point = profile_points[i]
        end_point = profile_points[(i + 1) % 4]
        line = Line.CreateBound(start_point, end_point)
        profile_loop.Append(line)
    
    # Hauteur du solide
    height = max_pt.Z - min_pt.Z
    
    # Créer le solide par extrusion
    solid_options = SolidOptions(ElementId.InvalidElementId, ElementId.InvalidElementId)
    extrusion = GeometryCreationUtilities.CreateExtrusionGeometry(
        [profile_loop], 
        XYZ(0, 0, 1),  # Direction d'extrusion (vers le haut)
        height,  # Distance d'extrusion
        solid_options
    )
    
    # Créer un DirectShape pour héberger le solide
    category_id = ElementId(BuiltInCategory.OST_GenericModel)
    ds = DirectShape.CreateElement(doc, category_id)
    
    # Définir la géométrie du DirectShape
    ds.SetShape([extrusion])
    
    # Appliquer le matériau si spécifié
    if material_id is not None:
        ds.SetMaterialId(material_id)
    
    return ds

def create_transparent_material(doc, name="Bbox Material", color=(128, 128, 255), transparency=50):
    """
    Crée un nouveau matériau transparent
    
    Args:
        doc: Document Revit actif
        name: Nom du matériau
        color: Tuple RGB (0-255)
        transparency: Transparence (0-100)
    
    Returns:
        ElementId: ID du matériau créé
    """
    with Transaction(doc, "Créer Matériau") as trans:
        trans.Start()
        
        # Créer un nouveau matériau
        material = Material.Create(doc, name)
        
        # Définir la couleur
        color_rgb = Color(color[0], color[1], color[2])
        material.Color = color_rgb
        
        # Définir la transparence
        material.Transparency = transparency
        
        trans.Commit()
        
        return material.Id

# Exemple d'utilisation
def example_usage():
    """
    Exemple d'utilisation pour créer un bounding box solide
    """
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    
    # Sélectionner un élément
    selection = uidoc.Selection
    selected_element = doc.GetElement(selection.GetElementIds()[0])
    
    # Obtenir le mesh et son bounding box
    geom_elem = selected_element.get_Geometry(Options())
    mesh = next(geom for geom in geom_elem if isinstance(geom, Mesh))
    bbox = get_mesh_bbox(mesh)  # Utilise la fonction précédente
    
    # Créer un matériau semi-transparent
    material_id = create_transparent_material(doc)
    
    # Créer le solide
    with Transaction(doc, "Créer Bounding Box Solide") as trans:
        trans.Start()
        bbox_solid = create_bbox_solid(doc, bbox, material_id)
        trans.Commit()
