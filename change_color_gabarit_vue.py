import json
import clr


# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
# import Revit API
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
clr.AddReference("System")
# Exemple d'un document actif
doc = DocumentManager.Instance.CurrentDBDocument

# Supposons que vous avez déjà le nom du gabarit de vue
view_template_name = "ratatuille"

# Rechercher le gabarit de vue dans le document
view_template = "none"
view_templates = FilteredElementCollector(doc).OfClass(View).ToElements()

for vt in view_templates:
	if vt.Name == view_template_name and vt.ViewTemplateId != ElementId.InvalidElementId:
		view_template = vt
        break

if view_template == "none":
	print("Gabarit de vue non trouvé.")
else:
	print(f"Gabarit de vue trouvé : {view_template.Name}")

# Commencer une transaction pour modifier le gabarit
TransactionManager.Instance.EnsureInTransaction(doc)

    # Modifier la couleur de remplissage pour une catégorie spécifique
walls_category = doc.Settings.Categories.get_Item(BuiltInCategory.OST_Walls)
    
if walls_category:
	# Récupérer les paramètres de visibilité pour le gabarit de vue
	view_template.SetCategoryHidden(walls_category.Id, False)  # S'assurer que la catégorie est visible# Définir une couleur de remplissage pour le gabarit de vue
	fill_color = Color(255, 0, 0)  # Rouge, par exemple
	# Appliquer la couleur de remplissage à cette vue uniquement
	override = OverrideGraphicSettings()
	override.SetProjectionFillColor(fill_color)
	override.SetProjectionFillPatternId(ElementId.InvalidElementId)  # Utilisez un motif de remplissage valide si nécessaire
	view_template.SetOverrides(walls_category.Id, override)

# Terminer la transaction
TransactionManager.Instance.TransactionTaskDone()
OUT = "Modifications des couleurs de remplissage effectuées avec succès."
