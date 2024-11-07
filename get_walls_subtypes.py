def get_wall_subtypes(doc, family_name=None):
    """
    Récupère tous les sous-types de mur d'une famille spécifique
    
    Args:
        doc: Document Revit actif
        family_name: Nom de la famille (ex: "Mur de base"). Si None, affiche tous les types
    Returns:
        Dictionary avec les familles et leurs sous-types
    """
    # Collecter tous les types de murs
    wall_types = FilteredElementCollector(doc).OfClass(WallType)
    
    # Organiser par famille
    wall_families = {}
    
    for wall_type in wall_types:
        # Obtenir le nom de la famille
        fam_name = wall_type.FamilyName
        # Obtenir le nom du sous-type
        type_name = wall_type.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
        
        # Si un nom de famille spécifique est donné, filtrer
        if family_name and family_name.lower() != fam_name.lower():
            continue
            
        # Ajouter à notre dictionnaire
        if fam_name not in wall_families:
            wall_families[fam_name] = []
            
        wall_families[fam_name].append({
            'name': type_name,
            'id': wall_type.Id,
            'width': wall_type.Width,
            'function': wall_type.Function,
            'wall_type': wall_type  # L'objet WallType complet
        })
    
    return wall_families
