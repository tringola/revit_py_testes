'''
Python Templates - Revit Based Python Imports
'''
__author__ = 'Brendan cassidy'
__twitter__ = '@brencass86'
__version__ = '1.0.0'

import clr
import System
import json
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

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

# Imports Ilists module into python
clr.AddReference("System")
from System.Collections.Generic import List as cList


# Standard areas for Current Document, Active UI and application
doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument


catname = IN[0]
bic = System.Enum.GetValues(BuiltInCategory) 
cats, bics = [], []
ost = ""
cat = []
arr_name = []
for i in bic:
    try:
        categorie = {}
        cat = Revit.Elements.Category.ById(ElementId(i).IntegerValue)
        arr_name = cat.Name.Split("-")
        if len(arr_name) > 1 :
            #remove dernier space vide (avant tiret)
        	categorie["main_category"] = arr_name[0][:-1]
        	#remove premier space vide (après tiret)
        	categorie["name"] = arr_name[1][1:]
        else :
        	categorie["name"] = cat.Name
        	
        categorie["OST"] = i.ToString()
        categorie['en_name']=ElementId(i).ToString()
        categorie['dwg_correspondance']=""
        categorie['ifc_correspondance']=""
        categorie['dgn_correspondance']=""
        categorie['type_categorie']=""

        cats.append(cat)
        bics.append(categorie)
    except:
        pass
 
for i, b in zip(cats, bics):
    if catname == str(i): 
        ost = b 
r = json.dumps(bics, indent=2, ensure_ascii=False)
OUT =  r

