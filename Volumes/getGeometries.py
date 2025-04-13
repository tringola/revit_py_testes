def getVolumes(doc, element):
    """
    Traite les volumes d'un élément IFC
    """
    if element is None:
        print("Element is None")
        return None
        
    print("Processing element ID: {}".format(element.Id))
    print("Element category: {}".format(element.Category.Name if element.Category else "No category"))
    
    # Configuration des options de géométrie
    opt = Options()
    opt.ComputeReferences = True
    opt.DetailLevel = ViewDetailLevel.Fine
    instance_geom = "null"
    # Extraire tous les volumes
    volumes = []
    try:
       
        # Obtenir la géométrie
        geometry = element.get_Geometry(opt)
        for geom_a in geometry:  # Itère sur les éléments géométriques
            if isinstance(geom_a, GeometryInstance):
                # Là on peut utiliser GetInstanceGeometry()
                volumes.append(geom_a.GetInstanceGeometry())
            elif isinstance(geom_a, Solid):
                # Traiter directement le Solid
                volumes.append(geom_a)
            elif isinstance(geom_a, Mesh):
                # Traiter directement le Mesh
                volumes.append(geom_a)
                
        if geometry is None:
            print("No geometry found for element")
            return None       
        
        return volumes
        
    except Exception as e:
        print("Error processing geometry: {}".format(str(e)))
        return None
