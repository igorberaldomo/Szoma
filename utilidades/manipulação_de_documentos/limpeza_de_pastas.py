import os

def limpeza_de_pastas():
    caminho_do_folder = "image/"
    for filename in os.listdir(caminho_do_folder):
        if filename.endswith('.png'):
            os.remove(os.path.join(caminho_do_folder, filename))
            print(f"Deleted: {filename}")
        if filename.endswith('.jpg'):
            os.remove(os.path.join(caminho_do_folder, filename))
            print(f"Deleted: {filename}")
        if filename.endswith('.jpeg'):
            os.remove(os.path.join(caminho_do_folder, filename))
            print(f"Deleted: {filename}")