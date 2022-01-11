"""Color module."""

class Color:
  """Color class.
  
  Represents an RGB color (0 to 255) with useful methods to manipulate it.
  Most of color methods returns the self object.
  """

  def __init__(self, r, g, b):
    self.r = self.__align(r) if r else 0
    self.g = self.__align(g) if g else 0
    self.b = self.__align(b) if b else 0
  
  def set(self, r, g, b):
    """Sets the color with R, G and B parameters."""
    self.r = self.__align(r)
    self.g = self.__align(g)
    self.b = self.__align(b)
    return self

  def set_color(self, color):
    """Sets the color with another color."""
    return self.set(color.r, color.g, color.b)

  def add(self, r, g, b):
    """Adds the color with R, G and B parameters."""
    self.r = self.__align(self.r + r)
    self.g = self.__align(self.g + g)
    self.b = self.__align(self.b + b)
    return self
  
  def add_color(self, color):
    """Adds the color with another color."""
    return self.add(color.r, color.g, color.b)
  
  def substract(self, r, g, b):
    """Substracts the color with R, G and B parameters."""
    self.r = self.__align(self.r - r)
    self.g = self.__align(self.g - g)
    self.b = self.__align(self.b - b)
    return self
  
  def substract_color(self, color):
    """Substracts the color with another color."""
    return self.substract(color.r, color.g, color.b)
  
  def multiply(self, r, g, b):
    """Multiplies the color with R, G and B parameters."""
    self.r = self.__align(self.r * r)
    self.g = self.__align(self.g * g)
    self.b = self.__align(self.b * b)
    return self
  
  def multiply_color(self, color):
    """Multiplies the color with another color."""
    return self.multiply(color.r, color.g, color.b)
  
  def divide(self, r, g, b):
    """Divides the color with R, G and B parameters."""
    self.r = self.__align(self.r / r)
    self.g = self.__align(self.g / g)
    self.b = self.__align(self.b / b)
    return self
  
  def divide_color(self, color):
    """Divides the color with another color."""
    return self.divide(color.r, color.g, color.b)
  
  def equals(self, r, g, b):
    """Checks if the color is equals to R, G and B parameters."""
    return self.r == r and self.g == g and self.b == b
  
  def equals_color(self, color):
    """Checks if the color is equals to another color."""
    return self.equals(color.r, color.g, color.b)

  def distance(self, color):
    """Returns the distance between the color and another color.
    
    This method returns an array like `[r_distance, g_distance, b_distance]`.
    """
    return [abs(self.r - color.r), abs(self.g - color.g), abs(self.b - color.b)]

  def srgb_gamma_compression(self):
    """Applies sRGB gamma compression."""
    # Convert color from 0..255 to 0..1
    r = self.r / 255
    g = self.g / 255
    b = self.b / 255

    # Apply sRGB
    if r > 0.0031308:
      r = 1.055 * (r ** (1/2.4)) - 0.055
    else:
      r = r * 12.92
    if g > 0.0031308:
      g = 1.055 * (g ** (1/2.4)) - 0.055
    else:
      g = g * 12.92
    if b > 0.0031308:
      b = 1.055 * (b ** (1/2.4)) - 0.055
    else:
      b = b * 12.92

    # Convert color from 0..1 to 0..255
    self.r = self.__align(r * 255)
    self.g = self.__align(g * 255)
    self.b = self.__align(b * 255)
    
    return self

  def srgb_inverse_gamma_compression(self):
    """Inverses sRGB gamma compression."""
    # Convert color from 0..255 to 0..1
    r = self.r / 255
    g = self.g / 255
    b = self.b / 255

    # Inverse sRGB
    if r > 0.04045:
      r = ((r + 0.055) / 1.055) ** 2.4
    else:
      r = r / 12.92
    if g > 0.04045:
      g = ((g + 0.055) / 1.055) ** 2.4
    else:
      g = g / 12.92
    if b > 0.04045:
      b = ((b + 0.055) / 1.055) ** 2.4
    else:
      b = b / 12.92

    # Convert color from 0..1 to 0..255
    self.r = self.__align(r * 255)
    self.g = self.__align(g * 255)
    self.b = self.__align(b * 255)
    
    return self
  
  def mix(self, color, mix):
    """Creates a mix color from the color and another color.

    The `mix` parameter can be set between 0.0 and 1.0 :
    - 0.0 : Full self color
    - 0.5 : Mix equals to self and target colors
    - 1.0 : Full target color
    
    This methods returns a new color with mixed values between this color and target color.
    """
    c1 = self.copy().srgb_inverse_gamma_compression()
    c2 = color.copy().srgb_inverse_gamma_compression()
    result = Color(c1.r * (1 - mix) + c2.r * (mix), c1.g * (1 - mix) + c2.g * (mix), c1.b * (1 - mix) + c2.b * (mix))
    return result.srgb_gamma_compression()

  def copy(self):
    """Copies the color.
    
    This method returns a new color instance with same values as self color.
    """
    return Color(self.r, self.g, self.b)
  
  def to_array(self):
    """Returns array representation of self color.
    
    The array will like `[r, g, b]`.
    """
    return [self.r, self.g, self.b]
  
  def __align(self, c):
    """Aligns a color value.
    
    This method can returns :
    - If value < 0 : 0
    - If value > 255 : 255
    - Else value : value
    """
    if c < 0.0:
      return 0
    elif c > 255.0:
      return 255
    return c
