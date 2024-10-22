from colorthief import ColorThief
import json
list_of_names =[]
copy_less_data = list()

with open('suvenil.json', 'r') as file:
    filedata = json.load(file)
    c = 0
    while c < len(filedata['cores']):
        if filedata['cores'][c]['nome'] not in list_of_names:
            copy_less_data.append(filedata['cores'][c])
        c+=1
new_data = copy_less_data

def write_json(new_data, filename='copy_less_suvenil.json'):
    with open(filename,'r+') as file:
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["coressuvinil"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)
write_json(new_data)

