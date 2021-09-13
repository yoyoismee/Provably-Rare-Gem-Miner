import logging, colorlog    
class LogColor:
    def __init__(self):
        self.NONCE_COLOR_LEVEL = 101
        self.DIFF_COLOR_LEVEL = 102
        self.SALT_COLOR_LEVEL = 104
        self.RESULT_COLOR_LEVEL = 103

    def get_nonce(self):
        return self.NONCE_COLOR_LEVEL
    
    def get_diff(self):
        print(self.DIFF_COLOR_LEVEL)
        return self.DIFF_COLOR_LEVEL
    
    def get_salt(self):
        return self.SALT_COLOR_LEVEL

    def get_result(self):
        return self.RESULT_COLOR_LEVEL
         
    def setup_logger(self):

        logging.addLevelName(101, 'NONCE')
        logging.addLevelName(102, 'DIFF')
        logging.addLevelName(103, 'RESULT')
        logging.addLevelName(104, 'SALT')

        formatter = colorlog.ColoredFormatter("%(log_color)s%(levelname)-8s%(reset)s %(message_log_color)s%(message)s",
        log_colors={'NONCE': 'red', 'DIFF': 'red', 'RESULT': 'cyan', 'SALT': 'blue'},
        secondary_log_colors={
            'message': {
                'NONCE': 'white,bg_red',
                'DIFF': 'white,bg_red',
                'RESULT': 'cyan',
                'SALT': 'white,bg_blue'
            }
        })
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger = logging.getLogger()
        logger.addHandler(handler)
    
        return logger