"""
    Tests basic workplane functionality
"""
#core modules
import io

#my modules
from cadquery import *
from cadquery import exporters
from tests import BaseTest


class TestStringIO(io.StringIO):
    def write(self, content):
        # force unicode encoding
        #
        # Justification:
        #   StringIO is being used in place of file descriptors,
        #   however file descriptors automatically encode for the
        #   output encoding... demonstrated below:
        #
        #       >>> # file type is flexible
        #       >>> with open('foo.txt', 'w') as s:
        #       ...     s.write(str('abc'))
        #       ...     s.write(unicode('xyz'))
        #       >>> with open('foo.txt', 'r') as s:
        #       ...     print(s.read())
        #       abcxyz
        #
        #       >>> # StringIO is not flexible with encoding
        #       >>> with io.StringIO() as s:
        #       ...     s.write(str('abc'))
        #       TypeError: unicode argument expected, got 'str'
        return super(TestStringIO, self).write(unicode(content))


class TestExporters(BaseTest):

    def _exportBox(self,eType,stringsToFind):
        """
            Exports a test object, and then looks for
            all of the supplied strings to be in the result
            returns the result in case the case wants to do more checks also
        """
        p = Workplane("XY").box(1,2,3)
        s = TestStringIO()
        exporters.exportShape(p,eType,s,0.1)

        result = s.getvalue()
        #print result
        for q in stringsToFind:
            self.assertTrue(result.find(q) > -1 )
        return result

    def testSTL(self):
        self._exportBox(exporters.ExportTypes.STL,['facet normal'])

    def testSVG(self):
        self._exportBox(exporters.ExportTypes.SVG,['<svg','<g transform'])

    def testAMF(self):
        self._exportBox(exporters.ExportTypes.AMF,['<amf units','</object>'])

    def testSTEP(self):
        self._exportBox(exporters.ExportTypes.STEP,['FILE_SCHEMA'])

    def testTJS(self):
        self._exportBox(exporters.ExportTypes.TJS,['vertices','formatVersion','faces'])
