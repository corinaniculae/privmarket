 #!/usr/bin/python

class TFLError(Exception):
    """Error class for handling TFL HTTPS request errors or warnings."""

    """ Initiates a TFL error instance. """
    def __init__(self, value):
        self.value = value
 
    """ Gives the string representation of the error. """   
    def __str__(self):
       return repr(self.value)