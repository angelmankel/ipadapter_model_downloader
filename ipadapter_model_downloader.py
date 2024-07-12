import os
import json
import requests

def load_model_list():
    with open(os.path.join(downloader_path, 'models.json'), 'r') as f:
        return json.load(f)
    
def verify_paths_exist():
    if not os.path.isdir(models_path):
        os.makedirs(models_path)
    
    if not os.path.isdir(os.path.join(models_path, 'ipadapter')):
        os.makedirs(os.path.join(models_path, 'ipadapter'))

    if not os.path.isdir(os.path.join(models_path, 'clip_vision')):
        os.makedirs(os.path.join(models_path, 'clip_vision'))
    
    if not os.path.isdir(os.path.join(models_path, 'loras')):
        os.makedirs(os.path.join(models_path, 'loras'))

    print('Model paths verified!')
        
def check_if_file_exists(path):
    return os.path.isfile(path)

def download_file(url, path):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024

    with open(path, 'wb') as file:
        for data in response.iter_content(block_size):
            file.write(data)

            # Progress bar
            progress = int(file.tell() / total_size * 50)
            print('\r[{}{}] {:.2f}%'.format('#' * progress, '.' * (50 - progress), file.tell() / total_size * 100), end='')

    print()

if __name__ == '__main__':

    # Set this to True to skip downloading models that already exist
    skip_existing = False

    # This can be hardcoded manually if needed
    comfyUI_path = os.path.dirname(os.getcwd())

    # Get the current working directory of the downloader script
    downloader_path = os.getcwd()

    # Define the paths to the custom nodes folder
    custom_nodes_path = os.path.join(comfyUI_path, 'custom_nodes')

    # Define the path to the models folder
    models_path = os.path.join(comfyUI_path, 'models')

    # Load model list
    models_to_download = load_model_list()

    # For testing purposes, only download the first model
    # models_to_download = [models_to_download[0]]

    # Get the number of models to download to display progress
    num_models = len(models_to_download)

    # Verify that the paths exist before downloading
    verify_paths_exist()

    # Display the number of models to download
    print('Downloading', num_models, 'models')

    # Start downloading models
    for i, model in enumerate(models_to_download):
        print('\nDownloading model', i+1, 'of', num_models, ':', model['filename'])

        if (skip_existing):
            exists = check_if_file_exists(os.path.join(comfyUI_path, model['path'], model['filename']))
            if exists:
                print('Model', i+1, 'of', num_models, 'already exists, skipping')
            else:
                download_file(model['url'], os.path.join(comfyUI_path, model['path'], model['filename']))                
        else:
            download_file(model['url'], os.path.join(comfyUI_path, model['path'], model['filename']))

    print('All models downloaded!')


