import os  # Helps interact with file system
import shutil  # Used to copy files and directories
import schedule  # Allows you to schedule tasks periodically
import time  # Used for delay in the execution
import logging  # Log message to a log file
import argparse  # Analyzes arguments


def main():
    parser = argparse.ArgumentParser(description="Sincronização de Pastas")
    # Argumento da pasta origem
    parser.add_argument("origem", help="Caminho da pasta origem")
    # Argumento da pasta destino
    parser.add_argument("destino", help="Caminho da pasta destino")
    # Argumento do intervalo de sincronização
    parser.add_argument("--intervalo", type=int, default=3600,
                        help="Intervalo de sincronização em segundos (padrão: 1 hora)")

    args = parser.parse_args()

    # Para DEBUG :)
    # print("Argumentos de linha de comando:")
    # print(f"Origem: {args.origem}")
    # print(f"Destino: {args.destino}")
    # print(f"Intervalo: {args.intervalo} segundos")

    configurar_logging()  # Configuração do registro de operações
    agendar_sincronizacao(args.origem, args.destino, args.intervalo)  # Agendamento da sincronização
    executar_agendamento()  # Execução do agendamento


def configurar_logging():
    log_filename = "registro_sync.txt"
    # Configuração do registro em arquivo
    logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(message)s')


def sincronizar_pastas(pasta_origem, pasta_destino):
    try:
        verificar_existencia_pasta(pasta_origem)  # Verifica se pasta original existe
        criar_pasta_se_nao_existe(pasta_destino)  # Cria a pasta de destino se não existir

        # Para DEBUG
        # print(f"Sincronizando: {pasta_origem} -> {pasta_destino}")

        for item in os.listdir(pasta_origem):
            origem_item = os.path.join(pasta_origem, item)
            destino_item = os.path.join(pasta_destino, item)

            if os.path.isfile(origem_item):
                copiar_arquivo(origem_item, destino_item)  # Cópia de arquivo
                # Para DEBUG
                # print(f"Arquivo copiado: {origem_item} -> {destino_item}")
                registrar_operacao("Cópia de arquivo", origem_item, destino_item)  # Registra a operção
            elif os.path.isdir(origem_item):
                sincronizar_pastas(origem_item, destino_item)  # Sincroniza as pasta
                # Para DEBUG
                # print(f"Pasta sincronizada: {origem_item} -> {destino_item}")
                registrar_operacao("Sincronização de pasta", origem_item, destino_item)  # Registra a operação

        remover_arquivos_excedentes(pasta_origem, pasta_destino)  # Remove arquivos a mais

        print("Sincronização concluída com sucesso!")

    except Exception as e:
        print(f"Ocorreu um erro durante a sincronização: {str(e)}")
        registrar_operacao("Erro durante sincronização", str(e))  # Registro de erro


def verificar_existencia_pasta(pasta):
    if not os.path.exists(pasta):
        print(f"A pasta '{pasta}' não existe.")
        raise FileNotFoundError(f"A pasta '{pasta}' não existe.")  # Tratamento de erro se pasta não existe


def criar_pasta_se_nao_existe(pasta):
    if not os.path.exists(pasta):
        os.makedirs(pasta)  # Criação da pasta se não existir


def copiar_arquivo(origem, destino):
    shutil.copy2(origem, destino)  # Cópia de arquivo


def registrar_operacao(acao, origem=None, destino=None):
    mensagem = acao
    if origem:
        mensagem += f": {origem} -> {destino}" if destino else f": {origem}"
    logging.info(mensagem)  # Registro da operação no arquivo
    print(mensagem)  # Mostra no console


def remover_arquivos_excedentes(pasta_origem, pasta_destino):
    for item in os.listdir(pasta_destino):
        destino_item = os.path.join(pasta_destino, item)
        if not os.path.exists(os.path.join(pasta_origem, item)):
            os.remove(destino_item)
            registrar_operacao("Remoção de arquivo", destino_item)  # Registra a remoção


def agendar_sincronizacao(pasta_origem, pasta_destino, intervalo):
    schedule.every(intervalo).seconds.do(sincronizar_pastas, pasta_origem, pasta_destino)  # Fazendo agendamento


def executar_agendamento():
    while True:
        schedule.run_pending()
        time.sleep(1)  # Executa agendamento
