import logging
from logging import handlers
import  os
def get_module_logger(mod_name):
  logger = logging.getLogger(mod_name)
  logger.setLevel(level=logging.DEBUG)
  formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

  time_rotating_file_handler = handlers.TimedRotatingFileHandler(os.getcwd(), when="MIDNIGHT", interval=1,
                                                                 backupCount=30)  # 每天零点存一个文件，最多30个
  time_rotating_file_handler.setLevel(logging.DEBUG)
  time_rotating_file_handler.setFormatter(formatter)

  stream_handler = logging.StreamHandler()
  stream_handler.setLevel(logging.DEBUG)
  stream_handler.setFormatter(formatter)

  logger.addHandler(time_rotating_file_handler)
  logger.addHandler(stream_handler)

  return logger
