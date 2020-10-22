import logging as logger

logger.basicConfig(
    filename='server.log'
    , filemode='a'
    , format='%(asctime)s, %(levelname)s, %(message)s'
    , datefmt='%A | %Y-%m-%d %H:%M:%S | %z'
    , level=logger.INFO
)

def log(level, message):
    '''ghi lai hoat dong cua thu vien
    '''
    if level.lower() in ['debug']:
        logger.debug(message)
    elif level.lower() in ['info']:
        logger.info(message)
    elif level.lower() in ['warning']:
        logger.warning(message)
    elif level.lower() in ['error']:
        logger.error(message)
    elif level.lower() in ['critical']:
        logger.critical(message)
