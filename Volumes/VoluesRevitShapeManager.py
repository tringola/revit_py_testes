def create_direct_shape(doc, solid, category_id, name):
    """
    Crée un élément DirectShape à partir d'un solide
    """
    # Créer une liste de géométrie pour DirectShape
    geometry_list = List[GeometryObject]()
    geometry_list.Add(solid)
    
    # Créer le DirectShape
    ds = DirectShape.CreateElement(doc, category_id)
    
    # Définir la forme
    ds.SetShape(geometry_list)
    
    # Définir le nom
    ds.Name = name
    
    return ds

def extract_and_create_volumes(doc, geometry_element, parent_element_id, category_id):
    """
    Extrait les volumes et crée des DirectShape pour chacun
    """
    volumes_data = []
    
    if geometry_element is None:
        return volumes_data
        
    for geom in geometry_element:
        if isinstance(geom, Solid):
            if geom.Volume > 0:
                # Générer un identifiant unique
                volume_id = str(uuid.uuid4())[:8]
                
                # Créer un nom descriptif
                volume_name = f"Volume_{volume_id}_from_{parent_element_id}"
                
                # Créer le DirectShape
                direct_shape = create_direct_shape(doc, geom, category_id, volume_name)
                
                # Stocker les informations du volume
                volume_data = {
                    'id': volume_id,
                    'revit_id': direct_shape.Id,
                    'name': volume_name,
                    'volume': geom.Volume,
                    'solid': geom,
                    'direct_shape': direct_shape,
                    'centroid': geom.ComputeCentroid(),
                    'bbox': geom.GetBoundingBox()
                }
                
                # Créer des paramètres pour stocker les métadonnées
                try:
                    # Créer un paramètre pour l'ID du volume parent
                    param = direct_shape.LookupParameter("ParentElementId")
                    if param:
                        param.Set(str(parent_element_id))
                        
                    # Créer un paramètre pour le volume
                    param = direct_shape.LookupParameter("Volume")
                    if param:
                        param.Set(geom.Volume)
                except Exception as e:
                    print(f"Erreur lors de la création des paramètres: {str(e)}")
                
                volumes_data.append(volume_data)
                
        elif isinstance(geom, GeometryInstance):
            instance_geom = geom.GetInstanceGeometry()
            volumes_data.extend(extract_and_create_volumes(doc, instance_geom, 
                                                         parent_element_id, category_id))
            
    return volumes_data

def analyze_volume_relationships(doc, volumes_data):
    """
    Analyse et stocke les relations entre les volumes dans les paramètres Revit
    """
    for i, vol in enumerate(volumes_data):
        intersecting_volumes = []
        containing_volumes = []
        contained_volumes = []
        
        for j, other_vol in enumerate(volumes_data):
            if i != j:
                try:
                    intersection = BooleanOperationsUtils.ExecuteBooleanOperation(
                        vol['solid'],
                        other_vol['solid'],
                        BooleanOperationsType.Intersect
                    )
                    
                    if intersection and intersection.Volume > 0:
                        intersecting_volumes.append(other_vol['id'])
                        
                        if abs(intersection.Volume - other_vol['solid'].Volume) < 0.0001:
                            containing_volumes.append(other_vol['id'])
                        elif abs(intersection.Volume - vol['solid'].Volume) < 0.0001:
                            contained_volumes.append(other_vol['id'])
                except:
                    continue
        
        # Stocker les relations dans les paramètres de l'élément DirectShape
        direct_shape = vol['direct_shape']
        try:
            # Stocker les IDs des volumes intersectants
            param = direct_shape.LookupParameter("IntersectingVolumes")
            if param:
                param.Set(','.join(intersecting_volumes))
                
            # Stocker les IDs des volumes contenants
            param = direct_shape.LookupParameter("ContainingVolumes")
            if param:
                param.Set(','.join(containing_volumes))
                
            # Stocker les IDs des volumes contenus
            param = direct_shape.LookupParameter("ContainedVolumes")
            if param:
                param.Set(','.join(contained_volumes))
        except Exception as e:
            print(f"Erreur lors du stockage des relations: {str(e)}")

def process_ifc_element_volumes(doc, element):
    """
    Traite un élément IFC et crée des DirectShape pour ses volumes
    """
    # Obtenir la catégorie appropriée pour les DirectShape
    category_id = element.Category.Id
    
    # Obtenir la géométrie
    opt = Options()
    opt.ComputeReferences = True
    opt.DetailLevel = ViewDetailLevel.Fine
    geometry = element.get_Geometry(opt)
    
    if geometry is None:
        return None
    
    # Créer les volumes
    volumes_data = extract_and_create_volumes(doc, geometry, element.Id, category_id)
    
    # Analyser et stocker les relations
    analyze_volume_relationships(doc, volumes_data)
    
    return volumes_data

def create_shared_parameters(doc, app):
    """
    Crée les paramètres partagés nécessaires
    """
    # Créer ou obtenir le fichier de paramètres partagés
    try:
        app.SharedParametersFilename = "VolumeParameters.txt"
        file = app.OpenSharedParameterFile()
    except:
        print("Erreur lors de la création du fichier de paramètres partagés")
        return False
    
    # Définir les paramètres à créer
    params_to_create = [
        ("ParentElementId", ParameterType.Text),
        ("VolumeId", ParameterType.Text),
        ("IntersectingVolumes", ParameterType.Text),
        ("ContainingVolumes", ParameterType.Text),
        ("ContainedVolumes", ParameterType.Text),
        ("Volume", ParameterType.Number)
    ]
    
    # Créer un groupe de définitions
    group = file.Groups.Create("VolumeParameters")
    
    # Créer les paramètres
    for param_name, param_type in params_to_create:
        if not group.Definitions.Contains(param_name):
            group.Definitions.Create(param_name, param_type)
    
    return True
