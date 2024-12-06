import json
import requests
from dotenv import load_dotenv
import os

def download_model(input_model_name, output_model_name, dir_path=None, timeout=30):
    load_dotenv()

    minio_url = os.getenv('MINIO_URL')
    if not minio_url:
        raise ValueError("La variable de entorno MINIO_URL no está definida")

    print("Descargando Modelo")

    url = f'http://{minio_url}/api/minio/download_from_models/'
    try:
        response = requests.post(url,data={'model_name': input_model_name},timeout=timeout)
        if response.status_code == 200:
            file_name = output_model_name
            if dir_path:file_name = f"{dir_path}/{output_model_name}"
            with open(file_name, 'wb') as file:
                file.write(response.content)

            print(f"File downloaded and saved successfully as '{file_name}'")
        else:
            print(f"Error: {response.status_code}")
            print(response.json())
    except Exception as e:
        print(f"Request failed: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")

def fuctions_execute(config_json_path: str):
    # Leer el archivo de configuración
    with open(config_json_path, 'r', encoding='utf-8') as file:
        config = json.load(file)

    #Ruta del proyecto
    ruta = config["proyect"]
    with open(f"{ruta}/{config_json_path}", 'r', encoding='utf-8') as file:
        config = json.load(file)
        
    # Usar los valores del archivo JSON
    model_name = f'{config["model_name"].split("/")[1]}/models/model.pkl'

    # Llamar al modelo y mostrar los resultados
    download_model(model_name, "model.pkl", dir_path=ruta, timeout=30000)


def main():

    config_json_path = "config.json"

    result = fuctions_execute(config_json_path)

if __name__ == "__main__":
    main()
