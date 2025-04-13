import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *

def create_bbox_solid(bbox):
    """
    Crée un Solid à partir d'une BoundingBoxXYZ
    
    Args:
        bbox: BoundingBoxXYZ à convertir en Solid
    Returns:
        Solid: Le solid créé
    """
    min_pt = bbox.Min
    max_pt = bbox.Max
    
    # Créer les points des coins
    pts = [
        XYZ(min_pt.X, min_pt.Y, min_pt.Z),  # 0
        XYZ(max_pt.X, min_pt.Y, min_pt.Z),  # 1
        XYZ(max_pt.X, max_pt.Y, min_pt.Z),  # 2
        XYZ(min_pt.X, max_pt.Y, min_pt.Z),  # 3
        XYZ(min_pt.X, min_pt.Y, max_pt.Z),  # 4
        XYZ(max_pt.X, min_pt.Y, max_pt.Z),  # 5
        XYZ(max_pt.X, max_pt.Y, max_pt.Z),  # 6
        XYZ(min_pt.X, max_pt.Y, max_pt.Z)   # 7
    ]
    
    # Créer les faces du cube
    edges = []
    faces = []
    
    # Face inférieure (0,1,2,3)
    profile = [pts[0], pts[1], pts[2], pts[3]]
    face = CreateFace(profile)
    faces.append(face)
    
    # Face supérieure (4,5,6,7)
    profile = [pts[4], pts[5], pts[6], pts[7]]
    face = CreateFace(profile)
    faces.append(face)
    
    # Face avant (0,1,5,4)
    profile = [pts[0], pts[1], pts[5], pts[4]]
    face = CreateFace(profile)
    faces.append(face)
    
    # Face droite (1,2,6,5)
    profile = [pts[1], pts[2], pts[6], pts[5]]
    face = CreateFace(profile)
    faces.append(face)
    
    # Face arrière (2,3,7,6)
    profile = [pts[2], pts[3], pts[7], pts[6]]
    face = CreateFace(profile)
    faces.append(face)
    
    # Face gauche (3,0,4,7)
    profile = [pts[3], pts[0], pts[4], pts[7]]
    face = CreateFace(profile)
    faces.append(face)
    
    # Créer le Solid à partir des faces
    try:
        shell = Shell.CreateShell(faces)
        solid = Solid.CreateShell(shell)
        return solid
    except:
        return None

def CreateFace(profile):
    """Crée une face à partir d'un profil de points"""
    loop = CurveLoop()
    for i in range(len(profile)):
        start = profile[i]
        end = profile[(i + 1) % len(profile)]
        line = Line.CreateBound(start, end)
        loop.Append(line)
    return Face.CreateFromCurveLoop(loop, True)

def create_bbox_directshape(doc, bbox, category_id=None, name=None, material_id=None):
    """
    Crée un DirectShape représentant la bounding box
    
    Args:
        doc: Document Revit actif
        bbox: BoundingBoxXYZ à visualiser
        category_id: ID de catégorie pour le DirectShape (optionnel)
        name: Nom du DirectShape (optionnel)
        material_id: ID du matériau à appliquer (optionnel)
    Returns:
        DirectShape: L'élément DirectShape créé
    """
    if not category_id:
        category_id = ElementId(BuiltInCategory.OST_GenericModel)
        
    # Créer le Solid
    solid = create_bbox_solid(bbox)
    if not solid:
        return None
        
    # Créer le DirectShape
    ds = DirectShape.CreateElement(doc, category_id)
    
    # Définir la géométrie
    geometry_options = DirectShapeOptions()
    geometry_options.ReferencingOption = DirectShapeReferencingOption.Independent
    
    ds.SetShape([solid], geometry_options)
    
    # Définir le nom si fourni
    if name:
        ds.Name = name
        
    # Appliquer le matériau si fourni
    if material_id:
        ds.SetMaterialId(material_id)
        
    return ds

def create_transparent_material(doc, name="BBox Material", color=None, transparency=50):
    """
    Crée un matériau semi-transparent
    """
    with Transaction(doc, "Créer matériau") as trans:
        trans.Start()
        
        # Créer un nouveau matériau
        material = Material.Create(doc, name)
        
        # Définir la couleur
        if not color:
            color = Color(100, 150, 255)  # Bleu clair par défaut
        material.Color = color
        
        # Définir la transparence (0-100)
        material.Transparency = transparency
        
        trans.Commit()
        
    return material.Id

def visualize_bboxes_as_solids(doc, bboxes):
    """
    Visualise les bounding boxes comme des DirectShapes semi-transparents
    
    Args:
        doc: Document Revit actif
        bboxes: Dictionnaire des bounding boxes à visualiser
    """
    # Créer un matériau semi-transparent
    material_id = create_transparent_material(doc)
    
    # Créer les DirectShapes
    created_shapes = []
    
    with Transaction(doc, "Créer BBox Solids") as trans:
        trans.Start()
        
        for idx, bbox in bboxes.items():
            name = "BoundingBox_{0}".format(idx)
            ds = create_bbox_directshape(doc, bbox, name=name, material_id=material_id)
            if ds:
                created_shapes.append(ds)
                
        trans.Commit()
        
    return created_shapes

# Exemple d'utilisation
def run_example(doc):
    # Récupérer les éléments sélectionnés
    selection = [doc.GetElement(id) for id in doc.Selection.GetElementIds()]
    geometries = []
    
    # Extraire les géométries
    for elem in selection:
        opts = Options()
        opts.ComputeReferences = True
        opts.DetailLevel = ViewDetailLevel.Fine
        
        geom_elem = elem.get_Geometry(opts)
        for geom in geom_elem:
            if isinstance(geom, Solid) or isinstance(geom, Mesh):
                geometries.append(geom)
    
    if geometries:
        # Créer les bounding boxes ajustées
        bboxes = align_geometry_list_bbox(geometries)
        
        # Créer les représentations solides
        shapes = visualize_bboxes_as_solids(doc, bboxes)
        
        print("Création de {0} DirectShapes pour visualiser les bounding boxes".format(len(shapes)))
        return shapes
    else:
        print("Aucune géométrie valide sélectionnée")
        return []
