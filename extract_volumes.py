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

# Get selection
selected = uidoc.Selection.GetElementIds()

# Return elements
resultado = []

for id in selected:
	e = doc.GetElement(id).ToDSType(True)
	resultado.append(e)


def extract_volumes(geometry_element):
    """
    Extrait tous les volumes (solides) d'un élément de géométrie
    """
    volumes = []
   
    if geometry_element is None:
        return volumes
     
    teste= 0     
    for geom in geometry_element:       
       
        nature = "neutre"
            # Vérifier que le solide est valide
        if  isinstance(geom, Solid):
        	nature = 'solide'
        	volumes.append({
			'type': nature,
			'solid': geom
             
		})              
   
        elif isinstance(geom, Mesh):
        	nature = 'Mesh'
        	volumes.append({
			'type': nature,
			'solid': geom
		})
		
		volumes.append({
			'type': "nananina",
			'solid': geom
		})
		print("Extracted Volumes: {volumes}")  # Debugging line  
		
    return volumes

def process_ifc_volumes(doc, element):
    """
    Traite les volumes d'un élément IFC
    """
   
    print("Processing: {geom}")  # Debugging line
    
    opt = Options()
    opt.ComputeReferences = True
    opt.DetailLevel = ViewDetailLevel.Fine
    
    geometry = element.Geometry()
    if geometry is None:
        return None
        
    # Extraire tous les volumes
    volumes = extract_volumes(geometry)
    
    # Analyser les relations entre volumes
   # analyzed_volumes = analyze_volume_composition(volumes)
    
    # Construire la hiérarchie des volumes
    #volume_hierarchy = get_volume_hierarchy(analyzed_volumes)
    
    return volumes



result = process_ifc_volumes(doc, resultado[0])
OUT = result
