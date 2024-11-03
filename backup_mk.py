import paramiko  # type: ignore
import datetime
import os
import time
import sys

# Configura    es do equipamento MikroTik
host = sys.argv[1]  # Endereço  do IP do MikroTik
hostname = sys.argv[2]  # Nome do Host Mikrotik dentro do Zabbix
username = sys.argv[3]  # Usuario do Mikrotik
password = sys.argv[4]  # Senha do Mikrotik
base_backup_dir = sys.argv[5]  # Caminho para salvar o backup

# Fun    o para realizar o backup


def realizar_export():
    timestamp = datetime.datetime.now().strftime("%d-%m-%Y")
    # Remove pontos do hostname para o nome do arquivo, mantendo a extens  o .rsc
    export_filename = f"backup_{hostname}_{timestamp}.rsc"

    # Criar uma pasta espec  fica para o hostname, se n  o existir
    hostname_dir = os.path.join(base_backup_dir, hostname.replace(
        ".", "_"))  # Troca pontos por underlines
    os.makedirs(hostname_dir, exist_ok=True)  # Cria a pasta se n  o existir

    try:
        # Conecta ao MikroTik via SSH
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username, password=password)

        # Comando para exportar a configura    o no MikroTik
        export_command = f"/export file={export_filename}"
        stdin, stdout,        stderr = client.exec_command(export_command)
        stdout.channel.recv_exit_status()  # Aguarda o comando terminar

        # Configura o SFTP para baixar o arquivo de exporta    o
        sftp = client.open_sftp()
        remote_export_path = f"/{export_filename}"
        local_export_path = os.path.join(
            hostname_dir, export_filename)  # Salva na pasta do hostname

        # Verifica se o arquivo foi realmente criado no MikroTik
        try:
            sftp.stat(remote_export_path)  # Confirma que o arquivo existe
        except FileNotFoundError:
            print(
                f"Erro: o arquivo {remote_export_path} n  o foi encontrado no MikroTik.")
            return

        # Baixa o arquivo de exporta    o
        sftp.get(remote_export_path, local_export_path)
        print(f"Backup realizado com sucesso e salvo em {local_export_path}")

        # Remove o arquivo de exporta    o do MikroTik ap  s o download
        remove_command = f'/file remove "{export_filename}"'
        client.exec_command(remove_command)

        # Verifica se o arquivo foi removido
        attempts = 5  # N  mero de tentativas para remover o arquivo
        for attempt in range(attempts):
            try:
                # Tenta verificar se o arquivo ainda existe
                sftp.stat(remote_export_path)
                print(
                    f"Tentativa {attempt + 1}: o arquivo {export_filename} ainda existe. Tentando remover novamente.")
                time.sleep(1)  # Espera 1 segundo antes de tentar novamente
                client.exec_command(remove_command)  # Tenta remover novamente
            except FileNotFoundError:
                print(
                    f"Arquivo remoto {export_filename} removido com sucesso ap  s {attempt + 1} tentativas.")
                break
        else:
            print(
                f"Erro: o arquivo {export_filename} n  o foi removido ap  s {attempts} tentativas.")

        # Fecha a conex  o SFTP e SSH
        sftp.close()
        client.close()
    except Exception as e:
        print(f"Erro ao exportar configura    o: {e}")


if __name__ == "__main__":
    realizar_export()
