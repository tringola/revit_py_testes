import clr
import logging
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

def process_geometry(geom):
    """
    Traite un élément de géométrie et retourne les volumes trouvés
    """
    volumes = []
    
    if isinstance(geom, Solid):
        if geom.Volume > 0:
            volumes.append({
                'type': 'solide',
                'solid': geom
            })
            print("Solide trouvé - Volume: {}".format(geom.Volume))
            
    elif isinstance(geom, Mesh):
        volumes.append({
            'type': 'Mesh',
            'solid': geom
        })
        print("Mesh trouvé")
        
    elif isinstance(geom, GeometryInstance):
        print("GeometryInstance trouvée - Extraction de la géométrie symbolique")
        # Obtenir la géométrie symbolique de l'instance
        symbol_geom = geom.GetInstanceGeometry()
        if symbol_geom:
            for sym_geom in symbol_geom:
                volumes.extend(process_geometry(sym_geom))
                
    elif isinstance(geom, GeometryElement):
        print("GeometryElement trouvé - Traitement des sous-éléments")
        for sub_geom in geom:
            volumes.extend(process_geometry(sub_geom))
            
    else:
        print("Autre type trouvé: {}".format(type(geom).__name__))
    
    return volumes

def extract_volumes(geometry_element):
    """
    Extrait tous les volumes (solides) d'un élément de géométrie
    """
    volumes = []
    
    if geometry_element is None:
        print("Geometry element is None")
        return volumes
    
    for geom in geometry_element:
        print("Traitement d'un élément de type: {}".format(type(geom).__name__))
        volumes.extend(process_geometry(geom))
    
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
    print("Element category: {}".format(element.Category.Name if element.Category else "No category"))
    
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
    e = doc.GetElement(id)
    resultado.append(e)

# Traiter le premier élément sélectionné
if len(resultado) > 0:
    result = process_ifc_volumes(doc, resultado[0])
else:
    result = None
    print("Aucun élément sélectionné")
    
def log():
	logging.basicConfig(filename="F:\\document\\23o_desktop\\Marvio_Revit_models\\std.log",format='%(asctime)s %(message)s',filemode='w')
	#Let us Create an object
	logger=logging.getLogger()
	#Now we are going to Set the threshold of logger to DEBUG
	logger.setLevel(logging.DEBUG)
	#some messages to test
	logger.debug("This is just a harmless debug message")
	logger.info("This is just an information for you")
	logger.warning("OOPS!!!Its a Warning")
	logger.error("Have you try to divide a number by zero")
	logger.critical("The Internet is not working....")

log()

OUT = result
