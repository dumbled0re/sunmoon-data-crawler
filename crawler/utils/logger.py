import datetime
from logging import DEBUG, CRITICAL, Formatter, StreamHandler, FileHandler, getLogger, disable

"""ロギング関係
"""

current_time = datetime.datetime.today().strftime("%Y-%m-%d_%H:%M:%S")
log_file_path = f"./log/logfile_{current_time}.txt"

logger = getLogger(__name__)
# disable(CRITICAL)
formatter = Formatter(
    "[%(levelname)s] [%(asctime)s] [%(filename)s:%(lineno)d] %(message)s"
)

filehandler = FileHandler(log_file_path)
filehandler.setFormatter(formatter)

streamhandler = StreamHandler()
streamhandler.setLevel(DEBUG)
streamhandler.setFormatter(formatter)

logger.addHandler(filehandler)
logger.addHandler(streamhandler)
logger.setLevel(DEBUG)
logger.propagate = False
