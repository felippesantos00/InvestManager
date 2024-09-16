import logging as log
import os

class LoggerConfig():
    def __init__(self, log_dir):
        self.LOG_DIR = log_dir
        self.configurar_logger()

    def configurar_logger(self):
       
        log_file = os.path.join(self.LOG_DIR, 'app.log')
        log.basicConfig(
            level=log.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                log.FileHandler(log_file),
                log.StreamHandler()
            ]
        )
        print("Iniciando Configurações de logging", log_file)
        print("Finalizado Configurações de logging")
