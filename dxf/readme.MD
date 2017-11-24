# Starting Point for DXF Importer

This folder has some working, but not integrated with CQ
code that can import/read dxfs.

Reference: https://github.com/dcowden/cadquery/issues/173

## Overview
This code will read a DXF, and clean it up in the process.

DXFs have lots of problems being used for 3d operations, because the default arc format is a centerpoint arc. The result is rounding errors, which cause the endpoints of arc sements not to align perfectly with the end points of line segments.

The right way to render DXF geometry is one long line, using polylines that render each point exactly once.  This can be done in DXFs using the 'bulge format' (LWPOLYLINE), which is desribed here:
https://forums.autodesk.com/t5/visual-lisp-autolisp-and-general/arc-bulge-factor/td-p/888184

This code reads entities, and creates a node map that links points together using a specified tolerance. Then, it chains the entities together so that it can form the largest number of continuous lines, minimizing rounding error.

## Getting started

use pip -r to install cadquery/requirements-dev.txt, and then
also requirements-dxf.txt in this folder.
This will install networkx and ezdxf, the depn

Run python read_dxf.py.It will read two dxfs included.

Two examples are provided-- an 80/20 section and a steel beam. I can provide lots more eamples-- in fact, I have the enter 80/20 collection and american steel shapes series!

## What work is left

This code reads a dxf, and reads it into an entity map that is ready to be used to create a CQ sketch using moveTo and arc commands.  The work left is:

  * move these files into the cq source
  * Add a importDxf function that reads a file. the function should allow specifying these properties:
      * filename
      * recenter=true/false-- this decides whether to shift the sktch to the origin( supported already by entitymap)
      * center point for the import ( default to center of the sketch)
      * layer number ( so user can select which layer to read in the dxf, default=0)
  * convert the entity map into the cq commands to add to the sketch.
  * delete vec2d.py and implmenet in terms of existing cq vector classes ( this is from a separate project where i didnt have vector code available )
  * upgrade to latest networkx ( i think they are at 2.0)
  * add dxf profiles directory to put lots of common profiles
  * add tests to the examples to ensure the new dxfs work right
  * move this code out this folder, into the right places, and delete this folder eventually
