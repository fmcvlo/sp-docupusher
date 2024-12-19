import os
import json
import datetime
import subprocess

# Cargar configuraciones
with open("config.json", "r") as config_file:
    config = json.load(config_file)

BASE_PATH = config["base_path"]
REPO_BASE_PATH = config["repo_base_path"]
DOCUMENTATION_FILE = os.path.join(REPO_BASE_PATH, config["documentation_file"])
SPS_PATH = os.path.join(REPO_BASE_PATH, config["sps_folder"])
SCRIPT_PATH = os.path.join(BASE_PATH, config["sps_folder"])

# Cargar mensajes
with open("messages.json", "r", encoding="utf-8") as messages_file:
    MESSAGES = json.load(messages_file)


def validate_config():
    if not os.path.exists(REPO_BASE_PATH):
        raise FileNotFoundError(f"La ruta del repositorio no existe: {REPO_BASE_PATH}")
    if not os.path.exists(SCRIPT_PATH):
        raise FileNotFoundError(f"La ruta del script no existe: {SCRIPT_PATH}")

def read_file_with_encoding(file_path, encoding="utf-8"):
    try:
        with open(file_path, "r", encoding=encoding) as file:
            return file.read()
    except UnicodeDecodeError:
        with open(file_path, "r", encoding="latin-1") as file:
            return file.read()

def update_sp_log(ejecuciones_path, sp_name, execution_status, notes=""):
    log_file = os.path.join(ejecuciones_path, "SP_Registro.md")
    if not os.path.exists(log_file):
        with open(log_file, "w", encoding="utf-8") as log:
            log.write("# Registro de Stored Procedures Ejecutados\n\n")

    content = read_file_with_encoding(log_file)
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    if f"# Fecha de ejecución: {today}" not in content:
        content += f"\n# Fecha de ejecución: {today}\n\n## Cantidad de SPs Ejecutados: 1\n\n- {sp_name} - {execution_status}\n\n### Notas adicionales:\n{notes}\n"
    else:
        content += f"- {sp_name} - {execution_status}\n"

    with open(log_file, "w", encoding="utf-8") as log:
        log.write(content)
    print(MESSAGES["log_updated"].format(path=log_file))

def update_documentation_v2(sp_list, file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    toc_start_index = next((i for i, line in enumerate(lines) if "## Tabla de Contenidos" in line), None)
    sp_start_index = next((i for i, line in enumerate(lines) if "## Stored Procedures" in line), None)

    if toc_start_index is None or sp_start_index is None:
        print("Error: No se encontraron las secciones requeridas en el archivo.")
        return

    toc_section = lines[toc_start_index + 1:sp_start_index]
    sp_section = lines[sp_start_index + 1:]

    new_toc_entries = []
    new_sp_entries = []

    for sp_name, description, ticket in sp_list:
        toc_entry = f"\t\t- [{sp_name}](#{sp_name.lower().replace('_', '-').replace(' ', '-')})\n"
        sp_entry = f"\n### {sp_name}\n\n**Descripción**: {description}\n**Ticket Asociado**: {ticket if ticket else 'N/A'}\n\n"
        if toc_entry not in toc_section:
            new_toc_entries.append(toc_entry)
        if sp_entry not in sp_section:
            new_sp_entries.append(sp_entry)

    toc_section.extend(new_toc_entries)
    updated_lines = lines[:toc_start_index + 1] + toc_section + ["\n"] + lines[sp_start_index:sp_start_index + 1] + sp_section + new_sp_entries

    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(updated_lines)
    print(MESSAGES["doc_updated"])

def save_or_copy_sp(ejecuciones_path, sp_content=None):
    sp_files = [f for f in os.listdir(SCRIPT_PATH) if os.path.isfile(os.path.join(SCRIPT_PATH, f))]

    if len(sp_files) == 0:
        print(MESSAGES["error_empty_folder"])
        return None
    elif len(sp_files) > 1:
        print(MESSAGES["error_multiple_files"])
        return None

    sp_filename = sp_files[0]
    sp_source_path = os.path.join(SCRIPT_PATH, sp_filename)
    sp_target_path = os.path.join(ejecuciones_path, sp_filename)

    if sp_content is None:
        os.rename(sp_source_path, sp_target_path)
        print(MESSAGES["sp_moved"].format(source=sp_source_path, target=sp_target_path))
    else:
        with open(sp_target_path, "w", encoding="utf-8") as sp_file:
            sp_file.write(sp_content)
        print(MESSAGES["sp_created"].format(path=sp_target_path))

    return sp_target_path, sp_filename

def git_commit_and_push(commit_message):
    subprocess.run(["git", "-C", REPO_BASE_PATH, "add", "."], check=True)
    subprocess.run(["git", "-C", REPO_BASE_PATH, "commit", "-m", commit_message], check=True)
    subprocess.run(["git", "-C", REPO_BASE_PATH, "push"], check=True)
    print("Cambios subidos al repositorio.")

if __name__ == "__main__":
    validate_config()
    version = input("Ingresa la versión de la carpeta de ejecuciones (por ejemplo, 11.1.7): ").strip()
    ejecuciones_path = os.path.join(REPO_BASE_PATH, f"Ejecuciones/{version}")
    os.makedirs(ejecuciones_path, exist_ok=True)

    sp_exists = input(MESSAGES["sp_exists"]).strip().lower()

    if sp_exists == "s":
        result = save_or_copy_sp(ejecuciones_path)
    else:
        sp_name = input(MESSAGES["sp_name"]).strip()
        sp_content = input(MESSAGES["sp_content"])
        result = save_or_copy_sp(ejecuciones_path, sp_content=sp_content)

    if not result:
        exit(1)

    sp_filepath, sp_name = result
    execution_status = input(MESSAGES["execution_status"]).strip().lower()
    execution_status = "éxito" if execution_status == "éxito" else "fallo"
    notes = input("Notas adicionales (opcional): ").strip()

    update_sp_log(ejecuciones_path, sp_name.replace('.sql', ''), execution_status, notes)

    description = input(MESSAGES["description"]).strip()
    ticket = input(MESSAGES["ticket"]).strip()
    update_documentation_v2([(sp_name.replace('.sql', ''), description, ticket)], DOCUMENTATION_FILE)

    git_commit_and_push(f"Registro y documentación del SP {sp_name}")
