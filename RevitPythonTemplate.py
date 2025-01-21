import sys
import os
"""
ajouter le ou les dossier ou se trouvent vos codes
"""
sys.path.append(os.path.abspath("X:\DIR_A\DIR_B\DIR_C"))


#importez les fichiers et tout ce qui a dedans
from HeadersRevitApi import *

# Start Transaction
TransactionManager.Instance.EnsureInTransaction(doc)
"""
ici du code qui interagi avec la DB de Revit
"""
# End Transaction
TransactionManager.Instance.TransactionTaskDone()

# Geometric converting between revit and dynamo elements
# https://github.com/teocomi/dug-dynamo-unchained/tree/master/dynamo-unchained-1-learn-how-to-develop-zero-touch-nodes-in-csharp#wrapping-unwrapping-and-converting


# Output and Changing element to Dynamo for export
# https://github.com/DynamoDS/Dynamo/wiki/Python-0.6.3-to-0.7.x-Migration#wrapping
# <element>.ToDSType(True), #Not created in script, mark as Revit-owned
# <element>.ToDSType(False) #Created in script, mark as non-Revit-owned
OUT = "default result"
