import logging
import sys
class GrpcLog:
    def grpc_log(self):
        logger = logging.getLogger(__name__)
        # logger setting
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter("[PID %(process)d] %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger


grpc_logging = GrpcLog()
