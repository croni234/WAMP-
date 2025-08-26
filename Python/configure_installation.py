import os
import shutil

def configure_apache(install_path):
    apache_conf_path = os.path.join(install_path, "apache", "conf", "httpd.conf")
    php_module_path = os.path.join(install_path, "php", "php8apache2_4.dll")
    php_ini_path = os.path.join(install_path, "php", "php.ini")

    if not os.path.exists(apache_conf_path):
        raise FileNotFoundError("Arquivo de configuração do Apache não encontrado.")

    # Configura o Apache para usar o PHP
    with open(apache_conf_path, "a") as conf_file:
        conf_file.write(f"""
# Configuração do PHP
LoadModule php_module "{php_module_path.replace("\\", "/")}"
AddHandler application/x-httpd-php .php
PHPIniDir "{os.path.dirname(php_ini_path).replace("\\", "/")}"
""")

def configure_php(install_path):
    php_ini_path = os.path.join(install_path, "php", "php.ini")
    if not os.path.exists(php_ini_path):
        raise FileNotFoundError("Arquivo php.ini não encontrado.")

    # Configura o PHP para se conectar ao MariaDB
    with open(php_ini_path, "a") as ini_file:
        ini_file.write("""
; Configuração do MariaDB
extension=mysqli
extension=pdo_mysql
""")

def configure_mariadb(install_path):
    mariadb_conf_path = os.path.join(install_path, "mariadb", "my.ini")
    data_dir = os.path.join(install_path, "mariadb", "data")

    if not os.path.exists(mariadb_conf_path):
        raise FileNotFoundError("Arquivo de configuração do MariaDB não encontrado.")

    # Configura o MariaDB
    with open(mariadb_conf_path, "a") as conf_file:
        conf_file.write(f"""
# Configuração do MariaDB
[mysqld]
datadir={data_dir.replace("\\", "/")}
""")

def configure_installation():
    install_path = "C:/invent/bin"

    try:
        configure_apache(install_path)
        configure_php(install_path)
        configure_mariadb(install_path)
        print("Configuração concluída com sucesso!")
    except Exception as e:
        print(f"Erro durante a configuração: {e}")

if __name__ == "__main__":
    configure_installation()
