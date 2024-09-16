import logging.handlers
from scripts.yahoo_finances import YahooFinances as yf
from commons.logger_config import LoggerConfig
from commons.configs import LoadConfigs
import logging as log
import os


def setup_logging():
    # Configura o caminho para o arquivo de log
    log_file = os.path.join(os.path.dirname(__file__),
                            'logs', 'application.log')

    print(log_file)
    # Cria o diretório de logs se não existir
    if not os.path.exists(os.path.dirname(log_file)):
        os.makedirs(os.path.dirname(log_file))

    # Configura o logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Configura o RotatingFileHandler
    handler = logging.handlers.RotatingFileHandler(
        # 5 MB por arquivo de log, mantendo 5 arquivos antigos
        log_file, maxBytes=5*1024*1024, backupCount=5
    )
    handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    logger.addHandler(handler)


def main():
    setup_logging()
    output_data_dir = LoadConfigs().get_output_datas_dir()
    output_data_file = os.path.join(output_data_dir,"rendimentos.csv")
    # Instancia a classe YahooFinances
    yf_instance = yf()

    # Processa as linhas do arquivo de entrada
    for linha in yf_instance.INPUT_BUY_STOCKS:
        TICKER, DATA_COMPRA, QTD_COTAS = linha.strip().split(";")
        QTD_COTAS = int(QTD_COTAS)
        yf_instance.calcular_rendimento(TICKER, DATA_COMPRA, QTD_COTAS)
        yf_instance.salvar_rendimentos_csv(output_data_file)
   
    # Salvar os rendimentos em um CSV
    log.info("Processamento concluído!")


if __name__ == "__main__":
    main()
