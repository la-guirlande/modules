from modules.utils import ghc, project

module = ghc.Module(project.ModuleType.MAGASIN, project.Paths.API_URL.value, project.Paths.WEBSOCKET_URL.value)

@module.listening('up')
def up_listener():
  print('Je monte sur ta grosse daronne')

@module.listening('down')
def down_listener():
  print('Je déscends sur ta grosse daronne')

@module.listening('stop')
def up_listener():
  print('J\'ai pété')

module.connect()
module.wait()
