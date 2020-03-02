from .client import upload_sample
import sys
import logging

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    try:
        if sys.argv[1] == 'upload-sample':
            upload_sample(sys.argv[2:])
    except Exception as error:
        logger.error(f'{error}')
        sys.exit(1)
