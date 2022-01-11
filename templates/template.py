def compile(path, data):
  """Compiles the target template with data to inject.
  
  Templates are located in the `./templates` folder.

  To create variable into the template, simply add `<% var_name %>` to the template content and run this method with `data={ 'var_name': value }`
  """
  compiled = ''
  with open(path) as template:
    for line in template.readlines():
      compiled_line = line
      for key, value in data.items():
        compiled_line = compiled_line.replace('<% ' + key + ' %>', value)
      compiled += compiled_line
  return compiled
