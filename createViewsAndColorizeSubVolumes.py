"""
Création de vues :

Une vue 3D principale montrant tous les sous-volumes
Une vue individuelle pour chaque sous-volume
Configuration automatique de la boîte de section pour chaque vue
Isolation des éléments dans leurs vues respectives

Coloration des volumes :

Schéma de couleurs prédéfini pour différencier les volumes
Application des couleurs via des surcharges graphiques
Motif de remplissage solide pour une meilleure visualisation
Même couleur maintenue dans toutes les vues pour cohérence



Pour utiliser ce code :

Sélectionnez l'élément IFC dans Revit
Exécutez le script
Vous obtiendrez :

Les sous-volumes créés comme DirectShapes
Une vue principale avec tous les volumes colorés
Des vues individuelles pour chaque volume
La vue principale s'active automatiquement
"""
import random
def create_3d_view(doc, name):
    """
    Crée une vue 3D spécifique pour les sous-volumes
    """
    # Créer un nouveau ViewFamilyType pour vue 3D
    collector = FilteredElementCollector(doc)
    view_family_type = collector.OfClass(ViewFamilyType)\
                               .FirstOrDefault(lambda x: x.ViewFamily == ViewFamily.ThreeDimensional)
    
    # Créer la nouvelle vue 3D
    view_3d = View3D.CreateIsometric(doc, view_family_type.Id)
    view_3d.Name = name
    
    # Configurer la vue
    view_3d.DisplayStyle = DisplayStyle.Shading
    view_3d.DetailLevel = ViewDetailLevel.Fine
    
    return view_3d

def create_color_scheme():
    """
    Crée un schéma de couleurs distinctes
    """
    base_colors = [
        (255, 0, 0),    # Rouge
        (0, 255, 0),    # Vert
        (0, 0, 255),    # Bleu
        (255, 165, 0),  # Orange
        (128, 0, 128),  # Violet
        (0, 255, 255),  # Cyan
        (255, 192, 203),# Rose
        (255, 255, 0),  # Jaune
        (165, 42, 42),  # Marron
        (0, 128, 0)     # Vert foncé
    ]
    
    # Convertir en format Revit Color
    return [Color(r, g, b) for r, g, b in base_colors]

def create_override_graphics(color):
    """
    Crée un surcharge graphique avec une couleur spécifique
    """
    override = OverrideGraphicSettings()
    override.SetSurfaceForegroundPatternColor(color)
    override.SetSurfaceBackgroundPatternColor(color)
    override.SetCutForegroundPatternColor(color)
    override.SetCutBackgroundPatternColor(color)
    
    # Ajouter un motif de remplissage solide
    fill_pattern_id = FillPatternElement.GetFillPatternElementByName(
        doc, 
        FillPatternTarget.Drafting, 
        "<Solid fill>"
    ).Id
    
    override.SetSurfaceBackgroundPatternId(fill_pattern_id)
    override.SetCutBackgroundPatternId(fill_pattern_id)
    
    return override

def setup_views_for_volumes(doc, shapes):
    """
    Crée et configure des vues pour visualiser les sous-volumes
    """
    # Créer une vue 3D principale
    main_3d_view = create_3d_view(doc, "Sous-Volumes - Vue Principale")
    
    # Créer une vue pour chaque sous-volume
    individual_views = []
    for i, shape in enumerate(shapes):
        view = create_3d_view(doc, f"Sous-Volume {i+1}")
        
        # Isoler le sous-volume dans sa vue
        view.IsolateElementTemporary(shape.Id)
        
        # Ajuster la boîte de vue autour du sous-volume
        bbox = shape.get_BoundingBox(view)
        if bbox:
            view.SetSectionBox(bbox)
            
        individual_views.append(view)
    
    return main_3d_view, individual_views

def apply_colors_to_shapes(doc, shapes, views):
    """
    Applique des couleurs différentes aux sous-volumes dans les vues
    """
    colors = create_color_scheme()
    main_view = views[0]
    individual_views = views[1]
    
    # Appliquer les couleurs dans la vue principale
    for i, shape in enumerate(shapes):
        color = colors[i % len(colors)]
        override = create_override_graphics(color)
        
        # Appliquer la surcharge dans la vue principale
        main_view.SetElementOverrides(shape.Id, override)
        
        # Appliquer la même surcharge dans la vue individuelle
        individual_views[i].SetElementOverrides(shape.Id, override)

def create_directshape_from_solid(doc, solid, category_id, name):
    """
    Crée un DirectShape à partir d'un solide
    """
    geom_list = List[GeometryObject]()
    geom_list.Add(solid)
    ds = DirectShape.CreateElement(doc, category_id)
    ds.SetShape(geom_list)
    ds.Name = name
    return ds

def extract_solids(geom_element):
    """
    Extrait tous les solides d'un élément géométrique
    """
    solids = []
    if isinstance(geom_element, GeometryElement):
        for geom in geom_element:
            if isinstance(geom, Solid) and geom.Volume > 0:
                solids.append(geom)
            elif isinstance(geom, GeometryInstance):
                instance_geom = geom.GetInstanceGeometry()
                solids.extend(extract_solids(instance_geom))
    return solids

def create_subshapes_with_views(doc, element):
    """
    Crée les sous-volumes et configure les vues
    """
    # Obtenir la géométrie
    opt = Options()
    opt.ComputeReferences = True
    opt.DetailLevel = ViewDetailLevel.Fine
    geom_element = element.get_Geometry(opt)
    
    # Extraire les solides
    solids = extract_solids(geom_element)
    
    # Créer les DirectShapes
    shapes = []
    for i, solid in enumerate(solids):
        name = f"SubVolume_{i+1}_from_{element.Id}"
        ds = create_directshape_from_solid(doc, solid, element.Category.Id, name)
        shapes.append(ds)
    
    # Créer et configurer les vues
    main_view, individual_views = setup_views_for_volumes(doc, shapes)
    
    # Appliquer les couleurs
    apply_colors_to_shapes(doc, shapes, (main_view, individual_views))
    
    return shapes, main_view, individual_views
