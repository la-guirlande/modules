from modules.utils import ghc, project

module = ghc.Module(project.ModuleType.TEST, project.Paths.API_URL.value, project.Paths.WEBSOCKET_URL.value)

@module.listening('data')
def data_listener(data):
  print('Received data from the backend :', str(data))
  module.send('data', data)
  print('Resent same data to the backend')

module.connect()
module.wait()
