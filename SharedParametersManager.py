import clr
# import Revit API
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
# import Revit Services 
clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
doc = DocumentManager.Instance.CurrentDBDocument
app = doc.Application

class SharedParametersManager:
    doc = DocumentManager.Instance.CurrentDBDocument
    app = doc.Application
    def createGroupsInSharedParameters(self,name):       
        originalFile = self.app.SharedParametersFilename
        #app.SharedParametersFilename = tempFile
        sharedParameterFile = self.app.OpenSharedParameterFile()
        #txt group name 
        GroupName = sharedParameterFile.Groups.Create(name)
        return GroupName