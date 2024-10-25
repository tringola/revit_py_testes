"""
Extraire tous les volumes (solides) composant l'élément avec leurs propriétés :

Volume en m³
Position du centre de gravité
Faces composantes
Boîte englobante


Analyser les relations entre les volumes :

Intersections entre volumes
Relations de contenance (un volume qui en contient un autre)
Identification des volumes primitifs (ceux qui n'intersectent avec aucun autre)


Construire une hiérarchie des volumes basée sur les relations de contenance, ce qui permet de comprendre comment les volumes sont imbriqués les uns dans les autres.

Voici un exemple de ce que vous pourriez voir comme résultat :
Volume 0: 100.50 m³
  Volume 1: 20.30 m³
    Volume 3: 5.20 m³
  Volume 2: 15.70 m³
  Cela signifie que le Volume 0 contient les Volumes 1 et 2, et le Volume 1 contient le Volume 3.
"""
# Exemple d'utilisation
def print_volume_hierarchy(hierarchy, indent=0):
    """
    Affiche la hiérarchie des volumes de manière lisible
    """
    for node in hierarchy:
        print('  ' * indent + f"Volume {node['index']}: {node['volume']:.2f} m³")
        if node['contained_volumes']:
            print_volume_hierarchy(node['contained_volumes'], indent + 1)

def main(doc, element):
    result = process_ifc_volumes(doc, element)
    if result:
        print(f"Analyse des volumes pour l'élément {result['element_id']}:")
        print("\nHiérarchie des volumes:")
        print_volume_hierarchy(result['hierarchy'])
        
        print("\nDétails des volumes:")
        for i, vol in enumerate(result['volumes']):
            print(f"\nVolume {i}:")
            print(f"  Volume: {vol['volume']:.2f} m³")
            print(f"  Est primitif: {vol['is_primitive']}")
            print(f"  Intersecte avec: {vol['intersecting_indices']}")
            print(f"  Contient les volumes: {vol['containing_indices']}")
            print(f"  Est contenu dans: {vol['contained_indices']}")
