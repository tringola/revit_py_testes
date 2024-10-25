'''
Python Templates - Revit Basic Imports
'''
__author__ = 'Da Rosa Freire'
__version__ = '0.1.0'

import clr
# import System
import System
from System.Collections.Generic import *
import csv
import json
import os

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

# import Revit API User Interface UI
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI import *
from Autodesk.Revit import Creation

# Imports Ilists module into python
clr.AddReference("System")
from System.Collections.Generic import List as cList
