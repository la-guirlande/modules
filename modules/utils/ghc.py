"""Guirlande Hub client library.

This library is used to communicate with the backend.
"""
import time
import requests
import socketio

class Module:
  """Module class used to instantiate the module and communicate with the backend."""

  def __init__(self, type, api_url, websocket_url):
    config = self.__read_config()
    self.type = type
    self.__api_url = api_url
    self.__websocket_url = websocket_url
    self.connected = False
    self.__token = config['token']
    self.socket = socketio.Client()

    # When connected, update module connection status
    @self.socket.on('module.connect')
    def __connect_listener(data):
      if data['status']:
        self.connected = True
        print('Module connected')
    
    # When disconnected, update module connection status
    @self.socket.on('disconnect')
    def __disconnect_listener():
        self.disconnect()
    
    @self.socket.on('module.error')
    def __error_listener(data):
      print('Error from the backend :', data['error'])
  
  def connect(self, max_attempt = 50):
    """Connects the module websocket to the backend.
    
    This method will blocks the current thread while the module is not connected. The thread is free when successful connection.
    
    If the module token is not set in the configuration file, this method will registers the module by calling API to `POST /modules/register` to gets a new token.
    This call will store this module in the backend but it will be set as not validated.
    That means an user must validate this module to allow access to it websocket events.

    If the token is stored on the configuration file, this method will periodically check if the module is validated
    by a websocket event emission (`module.connect`) while the module receives a `MODULE_IS_PENDING` error.

    After a positive response on the same event, the module is officially connected (and obviously validated) to the backend and can communicate to the dedicated events.
    """
    self.socket.connect(self.__websocket_url)
    print('Connecting')

    if self.__token == '':
      print('No token, registering')
      self.__register()
      print('Registered with token', self.__token)

    attempt = 0
    while not self.connected and attempt < max_attempt:
      attempt += 1
      print('Checking connection (attempt ' + str(attempt) + ')')
      self.socket.emit('module.connect', { 'token': self.__token })
      time.sleep(5)
    
    if not self.connected:
      print('Could not connect the module, maximum attempts reached')
  
  def run_task(self, fc, *args):
    """Runs a task in another thread."""
    return self.socket.start_background_task(fc, *args)
  
  def wait(self):
    """Waits until the connection between the module and the backend ends.
    
    This method will block the current thread. When the connection is lost, the thread is free.
    """
    self.socket.wait()
    self.disconnect()

  def disconnect(self):
    """Disconnects the module websocket from the backend."""
    self.socket.disconnect()
    self.connected = False
    print('Disconnected')
  
  def __register(self):
    """Registers the module to the backend.
    
    This method will send a `POST /modules/register` to register the module.
    The returned token is stored in the configuration file.
    """
    res = requests.post(self.__api_url + '/modules/register', { 'type': self.type })
    self.__token = res.json()['token']
    self.__write_config('token', self.__token)
  
  def listening(self, event_name):
    """Listening on a websocket event.
    
    This method is a decorator. Usage example :
    ```Python
    module = ghc.Module(0)

    @module.listening('color')
    def color_listener(data):
      print(data)
    ```
    """
    def inner(fc):
      self.socket.on('module.' + str(self.type) + '.' + event_name, fc)
      return fc
    return inner

  def send(self, event_name, data):
    """Sends data to a websocket event"""
    event_name = 'module.' + str(self.type) + '.' + event_name
    self.socket.emit(event_name, data)
    print('Sended event %s', event_name)
  
  def __read_config(self):
    """Reads the configuration file."""
    try:
      config = {}
      with open('config') as f:
        for line in f.readlines():
          items = line.split('=')
          config[items[0]] = items[1]
      return config
    except FileNotFoundError:
      print('Creating configuration file')
      self.__create_config({ 'token': '' })
      return self.__read_config() # Recursive if file not created
  
  def __create_config(self, config):
    """Creates the configuration file.
    
    This method will erase current configuration file if exists.
    """
    with open('config', 'w') as f:
      for key, value in config.items():
        f.write(key + '=' + value)
  
  def __write_config(self, key, value):
    """Writes a key value pair into the configuration file.
    
    This method will read and recreate the configuration file.
    """
    config = self.__read_config()
    config[key] = value
    self.__create_config(config)
