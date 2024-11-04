import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *

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

def create_transparent_material(doc, name="BBox Material", color=(100, 150, 255), transparency=70):
    """
    Crée un matériau semi-transparent
    """
    material = Material.Create(doc, name)
    material.Color = Color(color[0], color[1], color[2])
    material.Transparency = transparency
    return material.Id

def process_geometry_element(geom_elem):
    """
    Traite un élément de géométrie et retourne tous les solides trouvés
    
    Args:
        geom_elem: GeometryElement
    Returns:
        list: Liste de solides trouvés
    """
    solids = []
    
    if geom_elem is None:
        return solids
        
    # Parcourir tous les éléments de géométrie
    for geom in geom_elem:
        if isinstance(geom, Solid):
            # Vérifier que le solide est valide (a un volume)
            if geom.Volume > 0:
                solids.append(geom)
        elif isinstance(geom, GeometryInstance):
            # Traiter les instances de géométrie
            instance_geom = geom.GetInstanceGeometry()
            solids.extend(process_geometry_element(instance_geom))
            
    return solids

def main():
    uidoc = __revit__.ActiveUIDocument
    doc = uidoc.Document
    
    try:
        # Obtenir les éléments sélectionnés
        selection = uidoc.Selection
        element_ids = selection.GetElementIds()
        
        if not element_ids:
            raise Exception("Veuillez sélectionner au moins un élément.")
            
        # Créer un matériau semi-transparent une seule fois
        with Transaction(doc, "Créer Matériau BBox") as trans:
            trans.Start()
            material_id = create_transparent_material(doc)
            trans.Commit()
        
        # Créer les bounding boxes
        with Transaction(doc, "Créer Bounding Box Solides") as trans:
            trans.Start()
            
            bbox_count = 0
            for element_id in element_ids:
                element = doc.GetElement(element_id)
                
                # Obtenir la géométrie avec les options appropriées
                geom_options = Options()
                geom_options.ComputeReferences = True
                geom_options.IncludeNonVisibleObjects = True
                
                geom_elem = element.get_Geometry(geom_options)
                solids = process_geometry_element(geom_elem)
                
                # Créer un bounding box pour chaque solide
                for solid in solids:
                    bbox = get_solid_bbox(solid)
                    if bbox is not None:
                        create_bbox_solid(doc, bbox, material_id)
                        bbox_count += 1
            
            trans.Commit()
            
            print(f"{bbox_count} bounding box solides créés avec succès!")
            
    except Exception as e:
        print(f"Erreur: {str(e)}")
        # S'assurer que la transaction est annulée en cas d'erreur
        if trans.HasStarted():
            trans.RollBack()

if __name__ == '__main__':
    main()
