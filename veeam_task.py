import os  # Helps interact with file system
import shutil  # Used to copy files and directories
import schedule  # Allows you to schedule tasks periodically
import time  # Used for delay in the execution
import logging  # Log message to a log file
import argparse  # Analyzes arguments


def main():
    parser = argparse.ArgumentParser(description="Sincronização de Pastas")
    parser.add_argument("origem", help="Caminho da pasta de origem")  # Argumento para o caminho da pasta de origem
    parser.add_argument("destino", help="Caminho da pasta de destino")  # Argumento para o caminho da pasta de destino
    parser.add_argument("--intervalo", type=int, default=86400,
                        help="Intervalo de sincronização em segundos (padrão: 24 horas)")  # Argumento para o intervalo de sincronização

    args = parser.parse_args()

    configurar_logging()  # Configuração do registro de operações
    agendar_sincronizacao(args.origem, args.destino, args.intervalo)  # Agendamento da sincronização
    executar_agendamento()  # Execução do agendamento
