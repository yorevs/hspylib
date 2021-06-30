from abc import ABC

from PyQt5.QtGui import QColor

PARTITION_EOF = -191  # KafkaError._PARTITION_EOF
POLLING_INTERVAL = 0.5
FLUSH_TIMEOUT = 30

class StatusColor(ABC):
    white = QColor('#FFFFFF')
    red = QColor('#941100')
    green = QColor('#00FF00')
    yellow = QColor('#FFFF00')
    blue = QColor('#2380FA')
    orange = QColor('#FF8C36')
