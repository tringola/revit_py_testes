"""
Une classe GeometryAnalyzer qui peut :

Stocker plusieurs géométries
Analyser les relations entre deux géométries quelconques
Analyser toutes les relations possibles entre les géométries stockées


Pour chaque analyse, il détecte :

Si une géométrie est complètement contenue dans une autre
S'il y a une intersection partielle (avec le pourcentage d'intersection)
Si les géométries sont disjointes


Les résultats incluent :

Le type de relation
La surface d'intersection (si applicable)
Le pourcentage d'intersection par rapport à la plus petite géométrie
Une description détaillée



Pour l'utiliser avec vos polygones spécifiques, il suffit de :

Créer vos géométries avec Shapely
Les ajouter à l'analyseur
Lancer l'analyse
"""

from shapely.geometry import Polygon, Point
from enum import Enum
from typing import Tuple, List, Dict

class RelationType(Enum):
    DISJOINT = "disjoint"        # Pas de contact
    CONTAINS = "contains"        # Contient complètement
    WITHIN = "within"           # Est complètement contenu
    INTERSECTS = "intersects"   # Intersection partielle

class GeometryAnalyzer:
    def __init__(self):
        self.geometries = {}
        
    def add_geometry(self, name: str, geometry: Polygon):
        """Ajoute une géométrie à analyser"""
        self.geometries[name] = geometry
        
    def analyze_relationship(self, geom1_name: str, geom2_name: str) -> Dict:
        """Analyse la relation entre deux géométries"""
        if geom1_name not in self.geometries or geom2_name not in self.geometries:
            raise ValueError("Géométrie non trouvée")
            
        geom1 = self.geometries[geom1_name]
        geom2 = self.geometries[geom2_name]
        
        result = {
            "geometry1": geom1_name,
            "geometry2": geom2_name,
            "relationship": None,
            "intersection_area": 0,
            "details": ""
        }
        
        # Vérifier les relations
        if geom1.contains(geom2):
            result["relationship"] = RelationType.CONTAINS
            result["details"] = f"{geom1_name} contient complètement {geom2_name}"
        elif geom2.contains(geom1):
            result["relationship"] = RelationType.WITHIN
            result["details"] = f"{geom1_name} est complètement contenu dans {geom2_name}"
        elif geom1.intersects(geom2):
            intersection = geom1.intersection(geom2)
            result["relationship"] = RelationType.INTERSECTS
            result["intersection_area"] = intersection.area
            result["details"] = f"{geom1_name} intersecte partiellement {geom2_name}"
            result["intersection_percentage"] = (intersection.area / min(geom1.area, geom2.area)) * 100
        else:
            result["relationship"] = RelationType.DISJOINT
            result["details"] = f"{geom1_name} et {geom2_name} sont disjoints"
            
        return result

    def analyze_all_relationships(self) -> List[Dict]:
        """Analyse toutes les relations entre les géométries"""
        results = []
        names = list(self.geometries.keys())
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                results.append(self.analyze_relationship(names[i], names[j]))
        return results

# Exemple d'utilisation
def main():
    # Créer les géométries pour l'exemple
    # Polygone en U
    u_shape = Polygon([
        (0, 0), (0, 3), (1, 3), (1, 1), 
        (2, 1), (2, 3), (3, 3), (3, 0), (0, 0)
    ])
    
    # Polygone en L
    l_shape = Polygon([
        (2, 2), (2, 4), (3, 4), 
        (3, 3), (4, 3), (4, 2), (2, 2)
    ])
    
    # Cercle (approximé par un polygone régulier)
    from shapely.geometry import Point
    circle_center = Point(1.5, 2)
    circle = circle_center.buffer(0.4)  # Rayon de 0.4
    
    # Analyser les relations
    analyzer = GeometryAnalyzer()
    analyzer.add_geometry("U_shape", u_shape)
    analyzer.add_geometry("L_shape", l_shape)
    analyzer.add_geometry("Circle", circle)
    
    results = analyzer.analyze_all_relationships()
    
    # Afficher les résultats
    for result in results:
        print("\nAnalyse:", result["details"])
        if result["relationship"] == RelationType.INTERSECTS:
            print(f"Pourcentage d'intersection: {result['intersection_percentage']:.2f}%")

if __name__ == "__main__":
    main()
