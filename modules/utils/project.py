"""
Utils functions and classes.
"""
from enum import Enum

class ModuleType(Enum):
  """Module type."""
  TEST = 0
  LED_STRIP = 1,
  MAGASIN = 2

class Paths(Enum):
  """Paths."""
  API_URL = 'http://localhost'
  WEBSOCKET_URL = 'http://localhost:8000'
