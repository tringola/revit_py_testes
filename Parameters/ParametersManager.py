import clr
import sys
import os

import pyrevit

# import Revit API

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
# import Revit Services 
clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager

class SharedParametersManager:

    doc = DocumentManager.Instance.CurrentDBDocument
    app = doc.Application
    #si chemin du fichier est donné il ouvre le fichier et change, sinon il change le fichier ouvert
    def createGroupsInSharedParameters(self,name,path='null'):       
        originalFile = self.app.SharedParametersFilename
        #si le path (complet) du fichier est donné, donc prendre ce fichier comme base
        if path != 'null':
            app.SharedParametersFilename = path
        sharedParameterFile = self.app.OpenSharedParameterFile()
        #txt group name 
        GroupName = sharedParameterFile.Groups.Create(name)
        return GroupName
        
    def createType :
        
    def createParameterFromShared(self,parameterName,group,typeOfFamily,IsInstance):
        
        originalFile = self.app.SharedParametersFilename
        #app.SharedParametersFilename = tempFile
        sharedParameterFile = self.app.OpenSharedParameterFile()
        #txt parametres name 
        doc.FamilyManager.AddParameter()
        return 
    
    def addParameterToProject(self,name,file,groupe):
    
    #path is the path of dir and name of file .txt
    def createFileSharedParameters(self,path):
        f = open(path, "r")
        f.close()
        
    
    def getAllElementsOfCategory(self,Category):#il faut etre dans la forme BuiltInCategory.OST_Rooms par exemple
    FilteredElements = FilteredElementCollector(doc) 
    return FilteredElements.OfCategory(Category)


    #Pour manipuler les objets trouvés il faut faire un iteration, car les elements de la liste ne sont  acessible par index
    def setParameterByName(self,Element, parameter_name, value):
        Element.LookupParameter(parameter_name).Set(value)
        
    def clearParameterByName(self,Element, parameter_name):
        Element.LookupParameter(parameter_name).ClearValue()
        
    def getParameterAsString(self,Element, parameter_name):
        return Element.LookupParameter(parameter_name).AsString()
        
    def search(self,param,param_value,list):
        return [element for element in list if element[str(param)] == param_value]
    
