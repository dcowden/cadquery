"""
    Backend must implement all of the operations.
    The implemented name must be the same as the 
    base one, but without the 'Base' prefix.
    
    If a backend does not support an operation, it should
    still provide an implementation, but raise an error
    in the perform method.
    
    TODO: there might be a better way to do this.
    Sometimes, backends may not be ab

"""
from cadquery.impl_base.operations import *

class Sphere_Operation(BaseSphere_Operation):
    pass



