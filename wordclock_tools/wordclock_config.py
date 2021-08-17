import configparser
import logging
import os


class wordclock_config:

    def __init__(self, basePath):
        self.loadConfig(basePath)

    def loadConfig(self, basePath):
        pathToConfigFile = basePath + '/wordclock_config/wordclock_config.cfg'
        pathToReferenceConfigFile = basePath + '/wordclock_config/wordclock_config.reference.cfg'

        if not os.path.exists(pathToConfigFile):
            if not os.path.exists(pathToReferenceConfigFile):
                logging.error('No config-file available!')
                logging.error('  Expected ' + pathToConfigFile + ' or ' + pathToReferenceConfigFile)
                raise Exception('Missing config-file')
            copyfile(pathToReferenceConfigFile, pathToConfigFile)
            logging.warning('No config-file specified! Was created from reference-config!')

        logging.info('Parsing ' + pathToConfigFile)
        self.config = configparser.ConfigParser()
        self.config.read(pathToConfigFile)

        self.reference_config = configparser.ConfigParser()
        self.reference_config.read(pathToReferenceConfigFile)

        # Add to the loaded configuration the current base path to provide it
        # to other classes/plugins for further usage
        self.config.set('wordclock', 'base_path', basePath)

    def request(self, method, *args):
        try:
            return getattr(self.config, method)(*args)
        except:
            logging.warning("Defaulting to reference value for [" + str(args[0]) + "] " + str(args[1]) )
            return getattr(self.reference_config, method)(*args)

    def getboolean(self, *args):
        return self.request("getboolean", *args)

    def getint(self, *args):
        return self.request("getint", *args)

    def get(self, *args):
        return self.request("get", *args)
