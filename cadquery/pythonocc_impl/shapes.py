"""
    Copyright (C) 2011-2015  Parametric Products Intellectual Holdings, LLC

    This file is part of CadQuery.

    CadQuery is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.

    CadQuery is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public
    License along with this library; If not, see <http://www.gnu.org/licenses/>

    Wrapper Classes for PythonOCC
    These classes provide a stable interface for 3d objects,
    independent of the PythonOCC interface.

    Future work might include use of OCC, or even another CAD kernel directly,
    so this interface layer is quite important.

    This interface layer provides three distinct values:

        1. It allows us to avoid changing key api points if we change underlying implementations.
           It would be a disaster if script and plugin authors had to change models because we
           changed implementations

        2. Allow better documentation.  One of the reasons FreeCAD is no more popular is because
           its docs are terrible.  This allows us to provide good documentation via docstrings
           for each wrapper

        3. Work around bugs. There are a quite a few bugs in FreeCAD, and this layer allows fixing them

        4. Allows for enhanced functionality.  Many objects are missing features we need. For example
           we need a 'forConstruction' flag on the Wire object. This allows adding those kinds of things

        5. Allow changing interfaces when we'd like.  There are many cases where the PythonOCC API is not
           very user friendly: we like to change those when necessary.
"""
from cadquery import Vector, BoundBox