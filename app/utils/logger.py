import logging
import sys

console_handler = logging.StreamHandler(sys.stdout)

logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[console_handler],
)

logger = logging.getLogger(__name__)
