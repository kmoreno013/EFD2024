import logging
import os

def configure_logging(log_directory='logs'):
    log_directory = os.environ.get("LOG_DIR", "logs")
    os.makedirs(log_directory, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(f"{log_directory}/api.log")
        ]
    )
    
    modules = ['train', 'evaluate', 'predict', 'api']
    loggers = {}
    
    for module in modules:
        logger = logging.getLogger(f'ml_app.{module}')
        file_handler = logging.FileHandler(f'{log_directory}/{module}.log')
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(file_handler)
        loggers[module] = logger
    
    return loggers
