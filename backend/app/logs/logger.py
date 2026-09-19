import logging

import os





LOG_DIR = "logs"



os.makedirs(
    LOG_DIR,
    exist_ok=True
)





logging.basicConfig(

    filename=f"{LOG_DIR}/app.log",

    level=logging.INFO,

    format=
    "%(asctime)s | %(levelname)s | %(message)s"

)





logger = logging.getLogger(
    "hobbyfi"
)





def log_info(
    message: str
):


    logger.info(
        message
    )





def log_error(
    message: str
):


    logger.error(
        message
    )





def log_warning(
    message: str
):


    logger.warning(
        message
    )