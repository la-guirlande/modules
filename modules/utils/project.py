"""
Utils functions and classes.
"""
from enum import Enum

class ModuleType(Enum):
  """Module type."""
  LED_STRIP = 0

class Paths(Enum):
  """Paths."""
  API_URL = 'http://localhost'
  WEBSOCKET_URL = 'http://localhost:8000'
