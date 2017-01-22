
class Importer(object):

    def import_binary(self,stream):
        raise NotImplementedError("Please return a shape by reading a proprietry binary format from the stream")
        
    def import_step(self,stream):
        raise NotImplementedError("Please return a shape by reading STEP from the stream")
        
    def import_mesh(self,mesh):
        raise NotImplementedError("Please return a shape by reading the given mesh") 