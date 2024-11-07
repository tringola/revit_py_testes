import clr

# Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
#ça a changé
# Import geometry conversion extension methods
clr.ImportExtensions(Revit.GeometryConversion)

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

# Imports Ilists module into python
clr.AddReference("System")
from System.Collections.Generic import List as cList

la_bonne_liste = IN[0]

# Standard areas for Current Document, Active UI and application
doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument

# Start Transaction
TransactionManager.Instance.EnsureInTransaction(doc)

# End Transaction
TransactionManager.Instance.TransactionTaskDone()
# Input and unwrapping 
#input = UnwrapElement(IN[0])
def getRooms():
    FilteredElements = FilteredElementCollector(doc) 
    return FilteredElements.OfCategory(BuiltInCategory.OST_Rooms)


# Geometric converting between revit and dynamo elements
# https://github.com/teocomi/dug-dynamo-unchained/tree/master/dynamo-unchained-1-learn-how-to-develop-zero-touch-nodes-in-csharp#wrapping-unwrapping-and-converting

#t= Transaction(doc, 'title')
# Output and Changing element to Dynamo for export
# https://github.com/DynamoDS/Dynamo/wiki/Python-0.6.3-to-0.7.x-Migration#wrapping
# <element>.ToDSType(True), #Not created in script, mark as Revit-owned
# <element>.ToDSType(False) #Created in script, mark as non-Revit-owned
liste = []
#Pour manipuler les objets trouvés il faut faire un iteration, car les elements de la liste ne sont  acessible par index
def setParameterByName(Element, parameter_name, value):
    Element.LookupParameter(parameter_name).Set(value)
    
def clearParameterByName(Element, parameter_name):
    Element.LookupParameter(parameter_name).ClearValue()
    
def getParameterAsString(Element, parameter_name):
    return Element.LookupParameter(parameter_name).AsString()
    
def search(param,param_value,list):
    return [element for element in list if element[str(param)] == param_value]
    
    
rooms = getRooms()
temp = []
este=""
for el in rooms:
    list_b =[]
    #item_in_vrai_dicto =search('Nom',getParameterAsString(el,'Nom'),la_bonne_liste)
    item_in_vrai_dicto = getParameterAsString(el,'Numéro')
#peut-on prendre les parametres par nom. Le result est un element classe Autodesk.RevitDb.Parameter
    #setParameterByName(el,'__Piece_Safe Area_Fonction', 'ninjaGo')
   # str= area.SetValueString('ratatuille')
    #str= el.AsValueString()
   # liste.append({"item_000":search('Nom',getParameterAsString(el,'Numéro'),la_bonne_liste),"item_1111":getParameterAsString(el,'Numéro')})
    #temp.append(search('Nom',getParameterAsString(el,'Numéro'),la_bonne_liste))
    este = search('Nom',getParameterAsString(el,'Numéro'),la_bonne_liste)
    if len(este) !=0:
        a = {"csv_dict":este[0],"param_revit": getParameterAsString(el,'Numéro')}
        liste.append(a)
        if a['csv_dict']['Nb Cabin Cabinet'] != '' :
            setParameterByName(el, '__Piece_Safe Area_Cabin Cabinet',int(a['csv_dict']['Nb Cabin Cabinet']))
        else:
            setParameterByName(el, '__Piece_Safe Area_Cabin Cabinet',0)
            
        if a['csv_dict']['Safe Area Function'] != '' :
            setParameterByName(el, '__Piece_Safe Area_Fonction', a['csv_dict']['Safe Area Function'])
        else:
            setParameterByName(el, '__Piece_Safe Area_Fonction','')
            
       	if a['csv_dict']['Nb Public Cabinet'] != '' :
        	setParameterByName(el, '__Piece_Safe Area_Public Cabinet',int(a['csv_dict']['Nb Public Cabinet']))
        else:
            setParameterByName(el, '__Piece_Safe Area_Public Cabinet',0)
            
        if a['csv_dict']['Safe Area Table'] != '' :
            setParameterByName(el, '__Piece_Safe Area_Tableau',int(a['csv_dict']['Safe Area Table']))
        else:
            setParameterByName(el, '__Piece_Safe Area_Tableau',0)
            
for item in liste:
     if len(item['csv_dict'])!=0:    
        temp.append(item['csv_dict'])



	
OUT = liste
