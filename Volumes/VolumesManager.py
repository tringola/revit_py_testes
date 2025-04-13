def extract_volumes(geometry_element):
    """
    Extrait tous les volumes (solides) d'un élément de géométrie
    """
    volumes = []
    
    if geometry_element is None:
        return volumes
        
    for geom in geometry_element:
        if isinstance(geom, Solid):
            # Vérifier que le solide est valide
            if geom.Volume > 0:
                volumes.append({
                    'type': 'volume',
                    'solid': geom,
                    'volume': geom.Volume,
                    'faces': [f for f in geom.Faces],
                    'centroid': geom.ComputeCentroid(),
                    'bbox': geom.GetBoundingBox(),
                    'is_closed': all(face.Area > 0 for face in geom.Faces)
                })
                
        elif isinstance(geom, GeometryInstance):
            # Récursion pour les instances de géométrie
            instance_geom = geom.GetInstanceGeometry()
            volumes.extend(extract_volumes(instance_geom))
            
    return volumes

def analyze_volume_composition(volumes):
    """
    Analyse la composition des volumes pour identifier les relations spatiales
    """
    analyzed_volumes = []
    
    for i, vol in enumerate(volumes):
        intersecting_volumes = []
        containing_volumes = []
        contained_volumes = []
        
        # Comparer avec tous les autres volumes
        for j, other_vol in enumerate(volumes):
            if i != j:
                # Vérifier l'intersection
                try:
                    intersection = BooleanOperationsUtils.ExecuteBooleanOperation(
                        vol['solid'],
                        other_vol['solid'],
                        BooleanOperationsType.Intersect
                    )
                    
                    if intersection and intersection.Volume > 0:
                        intersecting_volumes.append(j)
                        
                        # Vérifier si un volume contient l'autre
                        if abs(intersection.Volume - other_vol['solid'].Volume) < 0.0001:
                            containing_volumes.append(j)
                        elif abs(intersection.Volume - vol['solid'].Volume) < 0.0001:
                            contained_volumes.append(j)
                except:
                    continue
        
        analyzed_vol = vol.copy()
        analyzed_vol.update({
            'intersecting_indices': intersecting_volumes,
            'containing_indices': containing_volumes,
            'contained_indices': contained_volumes,
            'is_primitive': len(intersecting_volumes) == 0
        })
        analyzed_volumes.append(analyzed_vol)
    
    return analyzed_volumes

def get_volume_hierarchy(analyzed_volumes):
    """
    Construit une hiérarchie des volumes basée sur les relations de contenance
    """
    hierarchy = []
    processed = set()
    
    def add_to_hierarchy(vol_index, level=0):
        if vol_index in processed:
            return None
            
        processed.add(vol_index)
        vol = analyzed_volumes[vol_index]
        
        node = {
            'index': vol_index,
            'volume': vol['volume'],
            'level': level,
            'contained_volumes': []
        }
        
        # Ajouter les volumes contenus
        for contained_idx in vol['containing_indices']:
            if contained_idx not in processed:
                contained_node = add_to_hierarchy(contained_idx, level + 1)
                if contained_node:
                    node['contained_volumes'].append(contained_node)
        
        return node
    
    # Commencer par les volumes qui ne sont contenus dans aucun autre
    for i, vol in enumerate(analyzed_volumes):
        if len(vol['contained_indices']) == 0 and i not in processed:
            hierarchy.append(add_to_hierarchy(i))
    
    return hierarchy

def process_ifc_volumes(doc, element):
    """
    Traite les volumes d'un élément IFC
    """
    opt = Options()
    opt.ComputeReferences = True
    opt.DetailLevel = ViewDetailLevel.Fine
    
    geometry = element.get_Geometry(opt)
    if geometry is None:
        return None
        
    # Extraire tous les volumes
    volumes = extract_volumes(geometry)
    
    # Analyser les relations entre volumes
    analyzed_volumes = analyze_volume_composition(volumes)
    
    # Construire la hiérarchie des volumes
    volume_hierarchy = get_volume_hierarchy(analyzed_volumes)
    
    return {
        'element_id': element.Id,
        'volumes': analyzed_volumes,
        'hierarchy': volume_hierarchy
    }
