import paramiko
import zipfile
import os

# Configurações do SFTP e diretórios
server = '177.67.24.191'
port = 51230
user = 'cdr01'
password = '' 
remote_dir = '/files/CDR/linksfield'
output_dir = r'C:\Users\matheus.weinert\Desktop\ArquivosMVNO_LINKSFIELD'

# Define o intervalo de datas desejado
start_date = '20241101'
end_date = '20241130'

# Cria o cliente SSH
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # Conecta ao servidor
    ssh_client.connect(server, port, user, password)
    print('Connection established successfully')
    
    # Abre a sessão SFTP
    sftp_client = ssh_client.open_sftp()

    # Lista arquivos no diretório remoto
    file_list = sftp_client.listdir(remote_dir)
    print(f'Files in {remote_dir}: {file_list}')

    # Função para descompactar arquivos e salvar apenas os CSVs
    def unzip_and_save_csv(zip_path, output_dir):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for file in zip_ref.namelist():
                # Verifica se é um arquivo CSV
                if file.endswith('.csv'):
                    print(f'Extraindo o arquivo CSV: {file}')
                    zip_ref.extract(file, output_dir)

    # Baixa e processa cada arquivo
    for file in file_list:
        # Filtra os arquivos pelo nome e intervalo de datas
        if file.endswith('.zip') and "cdr_" in file:
            file_date = file.split('_')[1]  # Extraindo a data do nome do arquivo
            if start_date <= file_date <= end_date:
                remote_file_path = f"{remote_dir}/{file}"
                local_file_path = os.path.join(output_dir, file)
                
                # Baixa o arquivo
                print(f'Baixando o arquivo: {file}')
                sftp_client.get(remote_file_path, local_file_path)

                # Descompacta os arquivos CSV
                print(f'Descompactando o arquivo: {file}')
                unzip_and_save_csv(local_file_path, output_dir)

                # Remove o arquivo ZIP baixado (opcional)
                os.remove(local_file_path)
                print(f'Arquivo ZIP removido: {local_file_path}')

    # Fecha a sessão SFTP
    sftp_client.close()

finally:
    # Fecha a conexão SSH
    ssh_client.close()
    print('Connection closed')
