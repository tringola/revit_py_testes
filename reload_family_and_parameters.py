import clr
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

# 1. Ajoutez un logging pour déboguer
import logging
logging.basicConfig(level=logging.DEBUG)

def reload_family_from_file(family_file_path):
    logging.debug(r"Tentative de chargement de la famille : {family_file_path}")
    
    if not family_file_path.lower().endswith('.rfa'):
        logging.error("Le fichier n'est pas un fichier .rfa")
        return False
        
    t = Transaction(doc, 'Recharger Famille depuis fichier')
    t.Start()
    
    try:
        load_options = FamilyLoadOptions()
        logging.debug("Options de chargement créées")
        
        # Vérifier si le fichier existe
        if not os.path.exists(family_file_path):
            logging.error(r"Le fichier n'existe pas : family_file_path")
            t.RollBack()
            return False
            
        family = doc.LoadFamily(family_file_path, load_options)
        logging.debug(r"Résultat du chargement : {family}")
        
        if family:
            t.Commit()
            logging.debug("Transaction validée avec succès")
            return True
        else:
            t.RollBack()
            logging.error("Échec du chargement de la famille")
            return False
            
    except Exception as e:
        t.RollBack()
        logging.error(r"Erreur lors du chargement : {str(e)}")
        return False

# Implémentation de IFamilyLoadOptions pour gérer les paramètres
class FamilyLoadOptions(IFamilyLoadOptions):
    def OnFamilyFound(self, familyInUse, overwriteParameterValues):
        # Écraser tous les paramètres existants
        overwriteParameterValues.Value = True
        return True
        
    def OnSharedFamilyFound(self, sharedFamily, familyInUse, source, overwriteParameterValues):
        # Écraser tous les paramètres existants pour les familles partagées aussi
        overwriteParameterValues.Value = True
        return True

# Exemple d'utilisation
family_file_path = "F:\\document\\23o_desktop\\sauvegarde_G36\\catalogue_GA\\Equipements\\GA_Separateur_gravitaire.rfa"  # Remplacer par le chemin de votre fichier

# Exécution
result = reload_family_from_file(family_file_path)
OUT = result