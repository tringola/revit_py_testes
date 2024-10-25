"""
Création d'éléments DirectShape :

Chaque sous-volume devient un élément DirectShape visible et sélectionnable dans Revit
Chaque volume reçoit un identifiant unique
Les volumes sont créés dans la même catégorie que l'élément parent


Stockage des métadonnées :

Création de paramètres partagés pour stocker les informations
Stockage de l'ID de l'élément parent
Stockage des relations entre volumes (intersections, contenances)
Stockage des propriétés géométriques


Traçabilité :

Chaque volume peut être retrouvé par son ID unique
Les relations entre volumes sont documentées dans les paramètres
Les volumes peuvent être sélectionnés et manipulés individuellement

uidoc = __revit__.ActiveUIDocument
volumes = run_on_selected_element(uidoc)
"""

def main(doc, element):
    """
    Fonction principale
    """
    # Créer les paramètres partagés si nécessaire
    app = doc.Application
    if not create_shared_parameters(doc):
        return
    
    # Commencer une transaction
    with Transaction(doc, "Create Volume Elements") as trans:
        trans.Start()
        
        try:
            # Traiter l'élément
            volumes_data = process_ifc_element_volumes(doc, element)
            
            if volumes_data:
                print(f"Créé {len(volumes_data)} volumes pour l'élément {element.Id}")
                for vol in volumes_data:
                    print(f"Volume {vol['id']}: {vol['volume']:.2f} m³")
            
            trans.Commit()
            return volumes_data
            
        except Exception as e:
            print(f"Erreur lors du traitement: {str(e)}")
            trans.RollBack()
            return None

# Exemple d'utilisation
def run_on_selected_element(uidoc):
    doc = uidoc.Document
    selection = uidoc.Selection
    element_id = selection.GetElementIds().First()
    element = doc.GetElement(element_id)
    
    return main(doc, element)
