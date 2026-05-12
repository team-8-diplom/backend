import logging

file_handler = logging.FileHandler('my_log.log')
console_handler = logging.StreamHandler()

logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[file_handler, console_handler],
)

logger = logging.getLogger(__name__)