# Charger les bibliothèques DesignScript et Standard Python
import sys
import clr
import os
import glob
import shutil
import json
import csv

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




# Standard areas for Current Document, Active UI and application
doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument

# Input and unwrapping 
input = UnwrapElement(IN[0])
def list_files(dir_path):
    # list to store files
    res = []
    try:
        for file_path in os.listdir(dir_path):
            if os.path.isfile(os.path.join(dir_path, file_path)):
                res.append(dir_path+file_path)
    except FileNotFoundError:
        print("The directory {dir_path} does not exist")
    except PermissionError:
        print("Permission denied to access the directory {dir_path}")
    except OSError as e:
        print("An OS error occurred: {e}")
    return res
    
def getFilesInDir(path,in_sub_dirs):#path is path to dir , in_sub_dir is boolean, true if search in subfolders

    list =[]
    for root, dirs, files in os.walk('C:\\document\\desktop\\Revit_models', topdown=False):
        for file in files:
            list.append("dir: "+os.path.join(root, file))
    return list
# Start Transaction
TransactionManager.Instance.EnsureInTransaction(doc)

# End Transaction
TransactionManager.Instance.TransactionTaskDone()

#OUT = list_files('C:\\document\\desktop\\Revit_models')
OUT = getFilesInDir('C:\\document\\desktop\\Revit_models','false')
