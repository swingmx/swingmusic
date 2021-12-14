import os

def fast_scandir(dirname):
    subfolders= [f.path for f in os.scandir(dirname) if f.is_dir()]

    for dirname in list(subfolders):
        subfolders.extend(fast_scandir(dirname))

    return subfolders


list = fast_scandir('/home/cwilvx/Music')

def remove_rejects(folders):
    rejects = []

    for item in folders:
        if item.find(".thumbnails") != -1:
            rejects.append(item)
        
        if len(os.listdir(item)) == 0 and item not in rejects:
            rejects.append(item)

    for item in rejects:
        folders.remove(item)

    print(len(folders))

remove_rejects(list)