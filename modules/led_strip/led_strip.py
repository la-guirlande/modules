from guirlande_hub_client_package import ghc
from ..utils import utils

module = ghc.Module(utils.ModuleType.LED_STRIP.value)

@module.listening('color')
def color_listener(data):
  print(data['red'], data['green'], data['blue']) # TODO Sends to PWM

try:
  module.connect(utils.Paths.WEBSOCKET_URL.value)
  module.register()
  print('Connected')
except KeyboardInterrupt:
  module.disconnect()
  print('Disconnected')
