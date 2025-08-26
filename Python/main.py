import os
import tkinter as tk
from tkinter import messagebox
import shutil
import subprocess
import hashlib
import requests

def check_installation():
    if os.path.exists("C:/invent"):
        if os.path.exists("C:/invent/bin/apache") and os.path.exists("C:/invent/bin/mariadb") and os.path.exists("C:/invent/bin/php"):
            return True
    return False

def install_software():
    try:
        os.makedirs("C:/invent/bin", exist_ok=True)
        # Copia e configura o Apache da pasta local
        configure_local_software("apache", "./wamp/apache.zip", 'E324797985825424AF00CDB9D78B029723F18862DF6C02C2219B341E33E31F04')
        configure_local_software("php", "./wamp/php-8.4.11-Win32-vs17-x64.zip", '1d037fb48dd44c2e434954a0408cc8e0078558bec37dcd98bf85e334e28d57bc')
        configure_local_software("mariadb", "./wamp/mariadb-12.0.2-winx64.zip", '7303f9d0f777ad903dede402ad3061097d216f3e2ab6e8499ad7aa192eb4080e')
        messagebox.showinfo("Sucesso", "Instalação concluída com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro durante a instalação: {e}")

def download_file(url, dest_path):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(dest_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

def verify_checksum(file_path, checksum):
    sha = hashlib.sha256()
    with open(file_path, "rb") as file:
        while chunk := file.read(8192):
            sha.update(chunk)
    return sha.hexdigest().upper() == checksum.upper()

def configure_local_software(software, zip_source_path, checksum):
    software_path = f"C:/invent/bin/{software}"
    os.makedirs(software_path, exist_ok=True)
    zip_dest_path = os.path.join(software_path, f"{software}.zip")

    # Copia o zip original para o destino
    shutil.copyfile(zip_source_path, zip_dest_path)

    # Verifica o checksum
    if not verify_checksum(zip_dest_path, checksum):
        raise ValueError(f"Checksum inválido para {software}.")

    # Extrai o arquivo compactado
    shutil.unpack_archive(zip_dest_path, software_path)
    os.remove(zip_dest_path)

    # Configuração adicional (simulação)
    with open(os.path.join(software_path, "README.txt"), "w") as f:
        f.write(f"{software} configurado com sucesso a partir do ZIP local.")


def download_and_configure(software, url, checksum=None):
    software_path = f"C:/invent/bin/{software}"
    os.makedirs(software_path, exist_ok=True)
    zip_path = os.path.join(software_path, f"{software}.zip")

    # Download do arquivo
    download_file(url, zip_path)

    # Verificação do checksum, se fornecido
    if checksum and not verify_checksum(zip_path, checksum):
        raise ValueError(f"Checksum inválido para {software}.")

    # Extração do arquivo (simulação)
    shutil.unpack_archive(zip_path, software_path)
    os.remove(zip_path)

    # Configuração adicional (simulação)
    with open(os.path.join(software_path, "README.txt"), "w") as f:
        f.write(f"{software} instalado com sucesso.")

def reinstall_software():
    if os.path.exists("C:/invent"):
        shutil.rmtree("C:/invent")
    install_software()

def main():
    root = tk.Tk()
    root.title("Instalador do Sistema")
    root.geometry("400x200")

    label = tk.Label(root, text="Bem-vindo ao Instalador do Sistema", font=("Arial", 14))
    label.pack(pady=10)

    if check_installation():
        messagebox.showinfo("Sistema já instalado", "O sistema já está instalado.")
        reinstall_button = tk.Button(root, text="Reinstalar", command=reinstall_software)
        reinstall_button.pack(pady=10)
    else:
        install_button = tk.Button(root, text="Instalar", command=install_software)
        install_button.pack(pady=10)

    exit_button = tk.Button(root, text="Sair", command=root.quit)
    exit_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
