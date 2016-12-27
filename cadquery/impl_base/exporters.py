class BaseExporter(object):    
    
    def export_svg(self,shape, stream, output_options=None):
        raise NotImplementedError("Please write SVG for the given shape to the stream")
        
    def export_binary(self,shape, stream, output_options=None):
        raise NotImplementedError("Please write binary data for the given shape to the stream, suitable for import")

    def export_step(self,shape, stream, output_options=None):
        raise NotImplementedError("Please write step format for the given shape to the stream, suitable for import")

    def export_mesh(self,shape, stream, output_options=None):
        #output options will typically be thigns like tolerance/deflection, etc
        raise NotImplementedError("Please return a Mesh object, which can be used to create other outputs") 