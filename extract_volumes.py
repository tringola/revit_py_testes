import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.IFC import *
import System
from System.Collections.Generic import List

# Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

# Import geometry conversion extension methods
clr.ImportExtensions(Revit.GeometryConversion)

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

# Standard areas for Current Document, Active UI and application
doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument

def extract_volumes(geometry_element):
    """
    Extrait tous les volumes (solides) d'un élément de géométrie
    """
    volumes = []
    
    if geometry_element is None:
        print("Geometry element is None")
        return volumes
    
    for geom in geometry_element:
        # Debug: afficher le type de géométrie
        print("Type de géométrie: {}".format(type(geom).__name__))
        
        nature = "neutre"
        
        # Vérifier que le solide est valide
        if isinstance(geom, Solid):
            if geom.Volume > 0:
                nature = 'solide'
                volumes.append({
                    'type': nature,
                    'solid': geom
                })
                print("Solide trouvé - Volume: {}".format(geom.Volume))
                
        elif isinstance(geom, Mesh):
            nature = 'Mesh'
            volumes.append({
                'type': nature,
                'solid': geom
            })
            print("Mesh trouvé")
        
        else:
            print("Autre type trouvé: {}".format(type(geom).__name__))
            volumes.append({
                'type': "autre",
                'solid': geom
            })
    
    print("Nombre total de volumes extraits: {}".format(len(volumes)))
    return volumes

def process_ifc_volumes(doc, element):
    """
    Traite les volumes d'un élément IFC
    """
    if element is None:
        print("Element is None")
        return None
        
    print("Processing element ID: {}".format(element.Id))
    
    # Configuration des options de géométrie
    opt = Options()
    opt.ComputeReferences = True
    opt.DetailLevel = ViewDetailLevel.Fine
    
    try:
        # Obtenir la géométrie
        geometry = element.get_Geometry(opt)
        
        if geometry is None:
            print("No geometry found for element")
            return None
            
        # Extraire tous les volumes
        volumes = extract_volumes(geometry)
        
        return volumes
        
    except Exception as e:
        print("Error processing geometry: {}".format(str(e)))
        return None

# Get selection
selected = uidoc.Selection.GetElementIds()

# Return elements
resultado = []
for id in selected:
    e = doc.GetElement(id)  # Sans conversion Dynamo
    resultado.append(e)

# Traiter le premier élément sélectionné
if len(resultado) > 0:
    result = process_ifc_volumes(doc, resultado[0])
else:
    result = None
    print("Aucun élément sélectionné")

OUT = result
