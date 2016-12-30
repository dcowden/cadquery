from cadquery import BaseOperation

#Primitive Operations
class BaseSphere_Operation(BaseOperation):pass
class BaseCone_Operation(BaseOperation):pass
class BaseWedge_Operation(BaseOperation):pass
class BaseBox_Operation(BaseOperation):pass
class BaseTorus_Operation(BaseOperation):pass
class BaseCylinder_Operation(BaseOperation):pass

#Solid Operations
class BaseExtrude_Operation(BaseOperation): pass
class BaseRevolve_Operation(BaseOperation): pass
class BaseSweep_Operation(BaseOperation): pass
class BaseLoft_Operation(BaseOperation): pass
class BaseDraft_Operation(BaseOperation): pass
class BaseUnion_Operation(BaseOperation): pass
class BaseIntersect_Operation(BaseOperation): pass
class BaseCut_Operation(BaseOperation): pass
class BaseChamfer_Operation(BaseOperation): pass
class BaseSplitOperation(BaseOperation):pass
class BaseFillet_Operation(BaseOperation): pass
class BaseClean_Operation(BaseOperation): pass
class BaseHole_Operation(BaseOperation): pass
class BaseCbore_Operation(BaseOperation): pass
class BaseCountersink_Operation(BaseOperation): pass

#Transformations
class BaseRotate_Operation(BaseOperation): pass
class BaseTranslate_Operation(BaseOperation): pass
class BaseTranform_Operation(BaseOperation):pass

#Face Operations
class BaseFaceCut_Operation(BaseOperation):pass
class BaseFaceIntersect_Operation(BaseOperation):pass
class BaseFaceFromPlane_Operation(BaseOperation):pass
class BaseFuseFace_Operation(BaseOperation):pass
class BaseRuledSurface_Operation(BaseOperation):pass
class BaseFaceFromWires_Operation(BaseOperation):pass

#Edge Operations
class BaseCircleEdge_Operation(BaseOperation): pass
class BaseSplineEdge_Operation(BaseOperation): pass
class BaseEdge_Operation(BaseOperation): pass
class BasePolyLineEdge_Operation(BaseOperation):pass
class BaseThreePointArc_Edge_Operation(BaseOperation):pass
class BaseCenterPointArc_Edge_Operation(BaseOperation):pass

#Wire Operations
class BaseCircleWire_Operation(BaseOperation): pass
class BaseRegularPolygonWire_Operation(BaseOperation):pass
class BaseHelix_Operation(BaseOperation):pass
class BaseCombineWires_Operation(BaseOperation):pass
class BaseCombineEdges_Operation(BaseOperation):pass
class BaseRectangleWire_Operation(BaseOperation):pass

#Shell Operations
class BaseShellFromFaces_Operation(BaseOperation): pass
class BaseShellSolid_Operation(BaseOperation): pass

#Projection Operations
class BaseProjectOntoPlane_Operation(BaseOperation): pass

#Other Stuff
class BaseCombine_Operation(BaseOperation): pass
