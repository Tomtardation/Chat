import asyncio
import inspect
import logging
import logging.config
from logging import NullHandler
import yaml


class ConfigurationLoader:
    def __init__(self):
        self.configurations = {}
        self.load('config/config.yaml')
        self.environment = self.configurations['config/config.yaml']['environment']
        logging.config.dictConfig(self.load("config/logging.yaml"))
        print(self.environment)
    
    def load(self, path):
        if path not in self.configurations:
            with open(path, 'r') as stream:
                try:
                    self.configurations[path] = yaml.safe_load(stream)
                except yaml.YAMLError as error:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    log.error(''.join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
        return self.configurations[path]
    
    def get(self, key):
        path = 'config/config.yaml'
        return self.configurations[path][self.environment][key] if self.environment in self.configurations[path] and key in self.configurations[path][self.environment] else None
    
    def getLogger(self):
        _from = inspect.stack()[1]
        _module = inspect.getmodule(_from[0])

        logger = logging.getLogger(_module.__name__)
        logger.propagate = False if 'logging' in self.configurations['config/config.yaml'][self.environment] and not self.configurations['config/config.yaml'][self.environment]['logging'] else True
        print(logger.propagate)
        
        return logger