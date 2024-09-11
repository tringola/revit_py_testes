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

def getParameterAsString(Element, parameter_name):
    return Element.LookupParameter(parameter_name).AsString()
    
def search(param,param_value,list):
    return [element for element in list if element[str(param)] == param_value]
    
    
rooms = getRooms()
for el in rooms:
    list_b =[]
    #item_in_vrai_dicto =search('Nom',getParameterAsString(el,'Nom'),la_bonne_liste)
    item_in_vrai_dicto = getParameterAsString(el,'Nom')
#peut-on prendre les parametres par nom. Le result est un element classe Autodesk.RevitDb.Parameter
    #setParameterByName(el,'__Piece_Safe Area_Fonction', 'ninjaGo')
   # str= area.SetValueString('ratatuille')
    #str= el.AsValueString()
    liste.append(search('Nom',getParameterAsString(el,'Numéro'),la_bonne_liste))
   

OUT = liste