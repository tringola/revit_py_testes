class IfcManager:
  doc = DocumentManager.Instance.CurrentDBDocument
  app = doc.Application
  def import_ifc(self, doc, ifc_path):
    """
    Importe un fichier IFC dans le document Revit actif
    """
    # Créer les options d'importation IFC
    options = IFCImportOptions()
    options.AutoJoin = False
    options.CreateLevel = False
    
    # Importer le fichier IFC
    try:
        ifc_link = IFCImportFile.Import(ifc_path, options, doc)
        return True
    except Exception as e:
        print(f"Erreur lors de l'importation IFC: {str(e)}")
        return False

  def get_ifc_elements(doc):
    """
    Récupère tous les éléments importés depuis IFC
    """
    # Créer un filtre pour les éléments IFC
    collector = FilteredElementCollector(doc)
    
    # Filtrer pour obtenir uniquement les éléments IFC
    ifc_elements = collector.WhereElementIsNotElementType()\
                          .WherePasses(ElementIsElementTypeFilter(False))\
                          .ToElements()
    
    # Filtrer pour ne garder que les éléments avec des données IFC
    return [elem for elem in ifc_elements if IFCImportFile.HasIFCData(doc, elem.Id)]

def get_ifc_geometry(doc, element):
    """
    Récupère la géométrie d'un élément IFC
    """
    opt = Options()
    opt.ComputeReferences = True
    opt.DetailLevel = ViewDetailLevel.Fine
    
    # Récupérer les données IFC de l'élément
    ifc_info = IFCImportFile.GetIFCData(doc, element.Id)
    if ifc_info is None:
        return None
        
    geometry = element.get_Geometry(opt)
    return geometry

def explode_geometry(geometry_element):
    """
    Décompose un élément de géométrie en ses sous-éléments
    """
    sub_elements = []
    
    if geometry_element is None:
        return sub_elements
        
    for geom in geometry_element:
        if isinstance(geom, Solid):
            # Extraire les faces du solide
            for face in geom.Faces:
                sub_elements.append({
                    'type': 'face',
                    'geometry': face,
                    'area': face.Area,
                    'material': face.MaterialElementId
                })
                
            # Extraire les arêtes du solide
            for edge in geom.Edges:
                sub_elements.append({
                    'type': 'edge',
                    'geometry': edge,
                    'length': edge.Length
                })
                
        elif isinstance(geom, GeometryInstance):
            # Récursion pour les instances de géométrie
            instance_geom = geom.GetInstanceGeometry()
            sub_elements.extend(explode_geometry(instance_geom))
            
    return sub_elements

def process_ifc_file(doc, ifc_path):
    """
    Traite un fichier IFC complet
    """
    # Commencer une transaction
    with Transaction(doc, "Import and Process IFC") as trans:
        trans.Start()
        
        # Importer le fichier IFC
        if not import_ifc(doc, ifc_path):
            print("Échec de l'importation IFC")
            return []
            
        # Récupérer tous les éléments IFC
        ifc_elements = get_ifc_elements(doc)
        
        # Traiter chaque élément
        all_sub_elements = []
        for element in ifc_elements:
            geometry = get_ifc_geometry(doc, element)
            if geometry:
                # Stocker les informations IFC avec la géométrie
                sub_elements = explode_geometry(geometry)
                for sub in sub_elements:
                    sub['ifc_type'] = element.GetType().ToString()
                    sub['ifc_id'] = element.Id.ToString()
                    # Récupérer les propriétés IFC si disponibles
                    ifc_properties = IFCImportFile.GetIFCData(doc, element.Id)
                    if ifc_properties:
                        sub['ifc_properties'] = ifc_properties
                        
                all_sub_elements.extend(sub_elements)
        
        trans.Commit()
        
    return all_sub_elements

# Exemple d'utilisation
def main():
    # Obtenir le document actif
    doc = __revit__.ActiveUIDocument.Document
    
    # Chemin vers le fichier IFC
    ifc_path = r"C:\chemin\vers\votre\fichier.ifc"
    
    # Traiter le fichier IFC
    sub_elements = process_ifc_file(doc, ifc_path)
    
    # Afficher les résultats
    for sub in sub_elements:
        print(f"Type: {sub['type']}")
        print(f"IFC Type: {sub['ifc_type']}")
        print(f"IFC ID: {sub['ifc_id']}")
        if 'area' in sub:
            print(f"Area: {sub['area']}")
        if 'length' in sub:
            print(f"Length: {sub['length']}")
        print("---")
