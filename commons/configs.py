import os
import logging as log


class LoadConfigs:
    """
    Classe responsável por carregar e organizar os diretórios do projeto.
    """

    def __init__(self):
        self.OS_DIR = os.getcwd()
        self.HOME_DIR = os.path.join(self.OS_DIR, "InvestManager")
        self.CONFIGS_DIR = os.path.join(self.HOME_DIR, "commons")
        self.LOGS_DIR = os.path.join(self.HOME_DIR, "logs")
        self.INPUT_DATAS = os.path.join(self.HOME_DIR, "input_datas")
        self.OUTPUT_DATAS = os.path.join(self.HOME_DIR, "output_datas")

        self._verificar_diretorios()
        # print(self.get_logs_dir())

    def _verificar_diretorios(self):
        """
        Verifica se os diretórios necessários existem. Se não, cria-os.
        """
        for directory in [self.LOGS_DIR, self.CONFIGS_DIR, self.INPUT_DATAS, self.OUTPUT_DATAS]:
            if not os.path.exists(directory):
                os.makedirs(directory)
                log.info(f"Diretório criado: {directory}")
            else:
                log.info(f"Diretório já existe: {directory}")

    def mostrar_diretorios(self):
        """
        Exibe os diretórios configurados.
        """
        log.info(self.OS_DIR)
        log.info(self.HOME_DIR)
        log.info(self.CONFIGS_DIR)
        log.info(self.LOGS_DIR)
        log.info(self.INPUT_DATAS)
        log.info(self.OUTPUT_DATAS)

    def get_logs_dir(self):
        return self.LOGS_DIR

    def get_input_datas_dir(self):
        return self.INPUT_DATAS

    def get_output_datas_dir(self):
        return self.OUTPUT_DATAS
