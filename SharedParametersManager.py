import clr
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
        #app.SharedParametersFilename = tempFile
        sharedParameterFile = self.app.OpenSharedParameterFile()
        #txt group name 
        GroupName = sharedParameterFile.Groups.Create(name)
        return GroupName
        
    def createSharedParameterInGroup(self,name):
        originalFile = self.app.SharedParametersFilename
        #app.SharedParametersFilename = tempFile
        sharedParameterFile = self.app.OpenSharedParameterFile()
        #txt parametres name 
        return 
    
    def addParameterToPoject(self,name,file,groupe):
    def createFileSharedParameters(self,path,):
