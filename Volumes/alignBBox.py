def align_bbox_with_geometry(element, doc):
    """
    Aligne la bounding box avec le volume exact d'un élément Revit.
    
    Args:
        element: L'élément Revit à traiter
        doc: Le document Revit actif
    Returns:
        BoundingBoxXYZ: La bounding box alignée
    """
    # Obtenir la géométrie de l'élément
    opts = Options()
    opts.ComputeReferences = True
    opts.DetailLevel = ViewDetailLevel.Fine
    
    geom_elem = element.get_Geometry(opts)
    
    # Initialiser les coordonnées min/max
    min_x = float('inf')
    min_y = float('inf')
    min_z = float('inf')
    max_x = float('-inf')
    max_y = float('-inf')
    max_z = float('-inf')
    
    # Parcourir tous les solides de la géométrie
    for geom in geom_elem:
        if isinstance(geom, Solid):
            # Obtenir les faces du solide
            for face in geom.Faces:
                # Obtenir les points de la face
                mesh = face.Triangulate()
                for vertex in mesh.Vertices:
                    # Mettre à jour les coordonnées min/max
                    min_x = min(min_x, vertex.X)
                    min_y = min(min_y, vertex.Y)
                    min_z = min(min_z, vertex.Z)
                    max_x = max(max_x, vertex.X)
                    max_y = max(max_y, vertex.Y)
                    max_z = max(max_z, vertex.Z)
    
    # Créer la nouvelle bounding box alignée
    bbox = BoundingBoxXYZ()
    bbox.Min = XYZ(min_x, min_y, min_z)
    bbox.Max = XYZ(max_x, max_y, max_z)
    
    return bbox

# Exemple d'utilisation
def align_selected_element_bbox(doc):
    selection = doc.Selection.GetElementIds()
    if selection.Count == 1:
        element_id = list(selection)[0]
        element = doc.GetElement(element_id)
        aligned_bbox = align_bbox_with_geometry(element, doc)
        return aligned_bbox
    return None
