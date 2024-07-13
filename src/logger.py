# to log all the execution details, useful for tracking everything such as exceptions

import logging
import os
from datetime import datetime

LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
logs_path=os.path.join(os.getcwd(),"logs",LOG_FILE) #current working directory -> cwd
os.makedirs(logs_path,exist_ok=True) #keep on appending files

LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

'testing'
# if __name__=="__main__":
#     logging.info("Logging has started")