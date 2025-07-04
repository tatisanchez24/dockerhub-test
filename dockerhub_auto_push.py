import os
import subprocess
import requests
import yaml  # Asegúrate de tener PyYAML instalado: pip install pyyaml

# Usa variables de entorno para las credenciales de Docker Hub
docker_username = os.getenv("DOCKER_USERNAME")
docker_password = os.getenv("DOCKER_PASSWORD")

if not docker_username or not docker_password:
    raise EnvironmentError("Debes definir las variables DOCKER_USERNAME y DOCKER_PASSWORD.")

# Endpoint de la API de Docker Hub
DOCKER_API = "https://hub.docker.com/v2"

# Autenticación y obtención del token
auth_response = requests.post(
    f"{DOCKER_API}/users/login/",
    json={"username": docker_username, "password": docker_password}
)

if auth_response.status_code != 200:
    raise Exception("Error al autenticar con Docker Hub.")

token = auth_response.json()["token"]
headers = {"Authorization": f"JWT {token}"}

# Crear carpeta de contexto de construcción
os.makedirs("build_context", exist_ok=True)

# Procesar cada archivo YAML en la carpeta docs/
for filename in os.listdir("docs"):
    if filename.endswith(".yaml"):
        name = os.path.splitext(filename)[0].replace("_", "-").lower()
        repo_name = f"{docker_username}/{name}"

        # Verificar si el repositorio ya existe
        repo_check = requests.get(f"{DOCKER_API}/repositories/{docker_username}/{name}/", headers=headers)
        if repo_check.status_code == 404:
            print(f"Creando repositorio: {repo_name}")
            create_response = requests.post(
                f"{DOCKER_API}/repositories/",
                headers=headers,
                json={"name": name, "namespace": docker_username, "is_private": False}
            )
            if create_response.status_code != 201:
                print(f"❌ Error al crear el repositorio {repo_name}")
                print(f"Status code: {create_response.status_code}")
                print(f"Respuesta de la API: {create_response.text}")
                continue
        else:
            print(f"Repositorio {repo_name} ya existe.")

        # Preparar archivos para la imagen
        yaml_path = os.path.join("docs", filename)
        readme_path = os.path.join("docs_readme", f"{os.path.splitext(filename)[0]}.md")
        dockerfile_path = "Dockerfile.template"

        # Leer la versión desde el archivo YAML
        with open(yaml_path, "r") as f:
            yaml_content = yaml.safe_load(f)
            version = yaml_content.get("version", "latest")

        with open("build_context/documentation.yaml", "w") as f:
            f.write(open(yaml_path).read())

        if os.path.exists(readme_path):
            with open("build_context/README.md", "w") as f:
                f.write(open(readme_path).read())
        else:
            with open("build_context/README.md", "w") as f:
                f.write("# Documentación no disponible\n")

        with open("build_context/Dockerfile", "w") as f:
            f.write(open(dockerfile_path).read())

        # Construir y subir la imagen con la versión y con el tag latest
        version_tag = f"{repo_name}:{version}"
        latest_tag = f"{repo_name}:latest"

        subprocess.run(["docker", "build", "-t", version_tag, "-t", latest_tag, "build_context"], check=True)
        subprocess.run(["docker", "login", "-u", docker_username, "--password-stdin"], input=docker_password.encode(), check=True)
        subprocess.run(["docker", "push", version_tag], check=True)
        subprocess.run(["docker", "push", latest_tag], check=True)

        # Subir README al repositorio en Docker Hub
        with open("build_context/README.md", "r") as f:
            readme_content = f.read()

        readme_update_response = requests.patch(
            f"{DOCKER_API}/repositories/{docker_username}/{name}/",
            headers=headers,
            json={"full_description": readme_content}
        )

        if readme_update_response.status_code == 200:
            print(f"📘 README actualizado correctamente para {repo_name}")
        else:
            print(f"⚠️ No se pudo actualizar el README para {repo_name}")
            print(f"Status code: {readme_update_response.status_code}")
            print(f"Respuesta: {readme_update_response.text}")

        # Limpiar contexto
        for f in os.listdir("build_context"):
            os.remove(os.path.join("build_context", f))

print("✅ Proceso completado.")
