# Charger les bibliothèques DesignScript et Standard Python
import sys
import clr
import os
import glob
import shutil
import json


def getFilesInDir(path,in_sub_dirs):#path is path to dir , in_sub_dir is boolean, true if search in subfolders
    list =[]
    for root, dirs, files in os.walk('F:\\document\\23o_desktop\\Marvio_Revit_models', topdown=True):
        for file in files:

        list.append("dir: "+os.path.join(root: {dirs}"+f"Files: {files}")
    return list
    
def list_files(dir_path):
    # list to store files
    res = []
    try:
        for file_path in os.listdir(dir_path):
            if os.path.isfile(os.path.join(dir_path, file_path)):
                res.append(file_path)
    except FileNotFoundError:
        print(f"The directory {dir_path} does not exist")
    except PermissionError:
        print(f"Permission denied to access the directory {dir_path}")
    except OSError as e:
        print(f"An OS error occurred: {e}")
    return res

def searchFilesPathsInDirWithExtension(dir_path,extension,isRecursive):
# search all files inside a specific folder
# *.* means file name with any extension and with yours estensions
    list = []    
    dir_path = r''+dir_path+'\**\*.'+extension
    try:
        for file in glob.glob(dir_path, recursive='true'):
            list.append(file)
    except FileNotFoundError:
        print(f"The directory {dir_path} does not exist")
    except PermissionError:
        print(f"Permission denied to access the directory {dir_path}")
    except OSError as e:
        print(f"An OS error occurred: {e}")
    return list
    
    #creer des dossiers selon l'extention des fichiers et les organiser en consequence
def organizeFileInDirsAccordingToExtention(ext,path):
    image_files = glob.glob("images/*.*")
        for image_file in image_files:
        _, ext = os.path.splitext(image_file)
        ext = ext.lower()
        if ext in ['.jpg', '.png', '.gif']:
            os.makedirs(f"images/{ext[1:]}", exist_ok=True)
            shutil.move(image_file, f"images/{ext[1:]}/{os.path.basename(image_file)}")
            
def readJsonFileToDictionary(path_to_file):
    with open(path_to_file) as file:
        data = json.load(file)
    return data#Dictionnaire

def writeDictionaryOrListToJson(dictionaryOrList,path_to_final_json):
    with open(path_to_final_json, 'w') as json_file:
        json.dump(dictionaryOrList, json_file)

def getTreeDirsFromRoot(root):
    tree = ''
    for root, dirs, files in os.walk('F:\\document\\23o_desktop\\Marvio_Revit_models'):
    indent = ' ' * root.count(os.sep) 
    tree += f'{indent}-{os.path.basename(root)}\n'

def csvToDict(file_path):
	list = []
	with open(file_path) as csvfile:
		reader = csv.DictReader(csvfile,delimiter=';')
		for row in reader:       
			list.append(row)
	return list
