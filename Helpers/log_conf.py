import logging.config
import  logging
import  datetime
def singleton(cls):
    instances = {}
    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return get_instance()

@singleton
class Logger():
    def __init__(self):
        datetimestr = datetime.datetime.now().strftime("%Y-%m-%d")
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler(f"log{datetimestr}.log"),
                logging.StreamHandler()
            ]
        )
        self.logr = logging.getLogger('root')
        
