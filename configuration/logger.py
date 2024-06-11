import datetime
from logging import getLogger, basicConfig, FileHandler, DEBUG


logger = getLogger()
LOG_FORMAT = '%(asctime)s : %(name)s : %(levelname)s : %(message)s'
file_handler = FileHandler(f'logs/{datetime.date.today()}.log')
file_handler.setLevel(DEBUG)
basicConfig(level=DEBUG, format=LOG_FORMAT, handlers=[file_handler])
