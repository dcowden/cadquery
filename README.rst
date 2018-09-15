.. image:: http://dcowden.github.io/cadquery/_static/cadquery_logo_dark.svg

What is a CadQuery?
========================================

|TRAVIS| |APPVEYOR| |COVERALLS| |VERSION| |LICENSE|

.. |TRAVIS| image:: https://travis-ci.org/dcowden/cadquery.svg?branch=master
    :alt: Travis Build Status
    :target: https://travis-ci.org/dcowden/cadquery?branch=master

.. |APPVEYOR| image:: https://ci.appveyor.com/api/projects/status/c7u4yjl8xxlokrw0/branch/master?svg=true
    :alt: Build status
    :target: https://ci.appveyor.com/project/jmwright/cadquery/branch/master

.. |COVERALLS| image:: https://coveralls.io/repos/github/dcowden/cadquery/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://coveralls.io/github/dcowden/cadquery?branch=master

.. |VERSION| image:: https://d25lcipzij17d.cloudfront.net/badge.svg?id=gh&type=6&v=1.2.0&x2=0
    :alt: GitHub version
    :target: https://github.com/dcowden/cadquery/releases/tag/v1.2.0

.. |LICENSE| image:: https://img.shields.io/badge/license-Apache2-blue.svg
    :alt: License
    :target: https://github.com/dcowden/cadquery/blob/master/LICENSE

CadQuery is an intuitive, easy-to-use python based language for building parametric 3D CAD models.  CadQuery is for 3D CAD what jQuery is for javascript.  Imagine selecting Faces of a 3d object the same way you select DOM objects with JQuery!

CadQuery has several goals:

* Build lD models with scripts that are as close as possible to how you'd describe the object to a human.
* Create parametric models that can be very easily customized by end users
* Output high quality (loss-less) CAD formats like STEP and AMF in addition to traditional STL
* Provide a non-proprietary, plain text model format that can be edited and executed with only a web browser

Using CadQuery, you can write short, simple scripts that produce high quality CAD models.  It is easy to make many different objects using a single script that can be customized.


Full Documentation and a Welcoming Community
===============================================
You can find the full cadquery documentation at `http://dcowden.github.io/cadquery <http://dcowden.github.io/cadquery>`_

We also have a Google Group to make it easy to get help from other CadQuery users. We want you to feel welcome and encourage you to join the group and introduce yourself. We would also love to hear what you are doing with CadQuery. https://groups.google.com/forum/#!forum/cadquery

Getting Started With CadQuery
========================================

Installation instructions for all following use cases can be found `here <http://dcowden.github.io/cadquery/installation.html>`_.

It is currently possible to use CadQuery for your own projects in 4 different ways:
  * as a plugin for FreeCAD
  * using the Docker Image to operate CadQuery as a CLI
  * as a plugin running on a Jupyter Notebook server
  * a standalone installation

I just want to try things out!
--------------------------------------------------

If you are interested in trying CadQuery without installing anything, your best option is to experiment with CadQuery scripts running on a Jupyter server.

|BINDER|

.. |BINDER| image:: https://mybinder.org/badge.svg
    :alt: Binder
    :target: https://mybinder.org/v2/gh/RustyVermeer/tryCQ/master

That button will launch a Jupyter Server pre-configured with CadQuery and its dependencies. It contains a folder with many useful examples to showcase CadQuery's features.

I'd like to use CadQuery on my own setup
--------------------------------------------------

The easiest way to get started with CadQuery is to Install FreeCAD (version 16+)  (`http://www.freecadweb.org/ <http://www.freecadweb.org/>`_), and then to use our great CadQuery-FreeCAD plugin here: `https://github.com/jmwright/cadquery-freecad-module <https://github.com/jmwright/cadquery-freecad-module>`_

It includes the latest version of cadquery already bundled, and has super-easy installation on Mac, Windows, and Unix.

It has tons of awesome features like integration with FreeCAD so you can see your objects, code-autocompletion, an examples bundle, and script saving/loading. Its definitely the best way to kick the tires!

I have other ideas and want to run things my own way
-----------------------------------------------------------

Awesome! CadQuery is built with this attitude in mind. If none of the existing usage methods work for you, you are more than welcome to forge your own path. You'll probably find the most success using the Docker image. You can alternatively install CadQuery as a standalone package.


Getting Started with the docker image
=======================================

The CadQuery docker image (`https://hub.docker.com/r/dcowden/cadquery/ <https://hub.docker.com/r/dcowden/cadquery/>`_)  includes cadquery and all of its dependencies. It can be used to run cadquery scripts without any installation required ( other than docker, of course)

Examples:

Display the Documentation:

.. code-block:: bash

     docker run dcowden/cadquery:latest

Build a local model using stdin/stdout:

.. code-block:: bash

    cat Ex001_Simple_Block.py | docker run -i dcowden/cadquery:latest build --in_spec stdin --format STEP --out_spec stdout

    ... STEP output on the console

Build local models and output to the same directory::

     docker run -v $PWD:/home/cq -i dcowden/cadquery:latest build --in_spec Ex001_Simple_Block.py --format STEP
     INFO: Reading from file 'Ex001_Simple_Block.py'
     INFO: Parsed Script 'Ex001_Simple_Block.py'.
     INFO: This script provides parameters length,thickness,height, which can be customized at build time.
     INFO: The script will run with default variable values
     INFO: use --param_file to provide a json file that contains values to override the defaults
     INFO: Output Format is 'STEP'. Use --output-format to change it.
     INFO: Output Path is './cqobject-%(counter)d.%(format)s'. Use --out_spec to change it.
     INFO: Script Generated 1 result Objects
     INFO: Writing STEP Output to './cqobject-1.STEP'


Projects Using CadQuery
=========================

This resin mold was modeled using cadquery and then created on a CNC machine:

|HY0ZD_CABLEFIX| |HY0ZD_FINISHED|

.. |HY0ZD_CABLEFIX| image:: http://dcowden.github.io/cadquery/_static/hyOzd-cablefix.png
   :alt: Cable-fix resin mold: Rendered

.. |HY0ZD_FINISHED| image:: http://dcowden.github.io/cadquery/_static/hyOzd-finished_thumb.jpg
   :alt: Cable-fix resin mold: Finised
   :target: http://dcowden.github.io/cadquery/_static/hyOzd-finished_thumb.jpg


The cadquery script is surprisingly short, and allows easily customizing any of the variables:

.. code-block:: python

    import cadquery as cq
    from Helpers import show
    BS = cq.selectors.BoxSelector

    # PARAMETERS
    mount_holes = True

    # mold size
    mw = 40
    mh = 13
    ml = 120

    # wire and fix size
    wd = 6  # wire diameter
    rt = 7  # resin thickness
    rl = 50  # resin length
    rwpl = 10  # resin to wire pass length

    # pocket fillet
    pf = 18

    # mount holes
    mhd = 7  # hole diameter
    mht = 3  # hole distance from edge

    # filling hole
    fhd = 6

    # DRAWING

    # draw base
    base = cq.Workplane("XY").box(ml, mw, mh, (True, True, False))

    # draw wire
    pocket = cq.Workplane("XY", (0, 0, mh)).moveTo(-ml/2., 0).line(0, wd/2.)\
        .line((ml-rl)/2.-rwpl, 0).line(rwpl, rt).line(rl, 0)\
        .line(rwpl, -rt).line((ml-rl)/2.-rwpl, 0)\
        .line(0, -(wd/2.)).close().revolve(axisEnd=(1, 0))\
        .edges(BS((-rl/2.-rwpl-.1, -100, -100), (rl/2.+rwpl+.1, 100, 100)))\
        .fillet(pf)

    r = base.cut(pocket)

    # mount holes
    if mount_holes:
        px = ml/2.-mht-mhd/2.
        py = mw/2.-mht-mhd/2
        r = r.faces("<Z").workplane().pushPoints([
    	(px, py),
    	(-px, py),
    	(-px, -py),
    	(px, -py)
    	]).hole(mhd)

    # fill holes
    r = r.faces("<Y").workplane().center(0, mh/2.).pushPoints([
        (-rl/2., 0),
        (0, 0),
        (rl/2., 0)
        ]).hole(fhd, mw/2.)

    show(r)


Thanks go to cadquery contributor hyOzd ( Altu Technology ) for the example!


KiCad uses cadquery to build high quality models of electrictronic components. (`https://github.com/KiCad/packages3D <https://github.com/KiCad/packages3D>`_)

.. image:: http://dcowden.github.io/cadquery/_static/KiCad_Capacitors_SMD_thumb.jpg
   :target: http://dcowden.github.io/cadquery/_static/KiCad_Capacitors_SMD.jpg
   :alt: Surface mount capacitors rendered in KiCad

This Prusa i3 extruder support uses cadquery to build the model (`https://github.com/adam-urbanczyk/cadquery-models <https://github.com/adam-urbanczyk/cadquery-models>`_):

.. image:: http://dcowden.github.io/cadquery/_static/extruder_support.png
   :alt: Prusa i3 extruder support - FreeCAD model render

The mach30 project used cadquery to develop a tool that will create a rocket thruster directly from the appropriate equations (`https://opendesignengine.net/projects/yavin-thruster/wiki <https://opendesignengine.net/projects/yavin-thruster/wiki>`_):

.. image:: http://dcowden.github.io/cadquery/_static/march30_landing_page.png
   :target: https://opendesignengine.net/projects/yavin-thruster/wiki
   :alt: mach30 project landing page

This example uses Jupyter notebook to produce a really cool web-based scripting environment (`https://github.com/RustyVermeer/avnb/blob/master/readme.md <https://github.com/RustyVermeer/avnb/blob/master/readme.md>`_):

.. image:: http://dcowden.github.io/cadquery/_static/jupyter_showcase_thumb.gif
   :alt: Jupyter notebook showcased as animation
   :target: https://github.com/RustyVermeer/cqnb/raw/master/showcase.gif

We would love to link to your cadquery based project. Just let us know and we'll add it here.


Where does the name CadQuery come from?
========================================

CadQuery is inspired by jQuery, a popular framework that
revolutionized web development involving javascript.

If you are familiar with jQuery, you will probably recognize several jQuery features that CadQuery uses:

* A fluent api to create clean, easy to read code
* Language features that make selection and iteration incredibly easy
* Ability to use the library along side other python libraries
* Clear and complete documentation, with plenty of samples.


Why CadQuery instead of OpenSCAD?
========================================

CadQuery is based on OpenCasCade.  CadQuery shares many features with OpenSCAD, another open source, script based, parametric model generator.

The primary advantage of OpenSCAD is the large number of already existing model libraries  that exist already. So why not simply use OpenSCAD?

CadQuery scripts have several key advantages over OpenSCAD:

#. **The scripts use a standard programming language**, python, and thus can benefit from the associated infrastructure.
   This includes many standard libraries and IDEs
#. **More powerful CAD kernel** OpenCascade is much more powerful than CGAL. Features supported natively
   by OCC include NURBS, splines, surface sewing, STL repair, STEP import/export,  and other complex operations,
   in addition to the standard CSG operations supported by CGAL
#. **Ability to import/export STEP** We think the ability to begin with a STEP model, created in a CAD package,
   and then add parametric features is key.  This is possible in OpenSCAD using STL, but STL is a lossy format
#. **Less Code and easier scripting**  CadQuery scripts require less code to create most objects, because it is possible to locate
   features based on the position of other features, workplanes, vertices, etc.
#. **Better Performance**  CadQuery scripts can build STL, STEP, and AMF faster than OpenSCAD.


License
====================

CadQuery is licensed under the terms of the `Apache Public License, version 2.0 <http://www.apache.org/licenses/LICENSE-2.0>`_.

Ongoing and Future Work
=============================

CadQuery GUI (under development)
-------------------------------------------

Work is underway on a stand-alone gui here: `https://github.com/jmwright/cadquery-gui <https://github.com/jmwright/cadquery-gui>`_

CadQuery Parts / Assembly Handling
-------------------------------------------

Work by Fragmuffin is ongoing with the `cqparts <https://github.com/fragmuffin/cqparts>`_ repo.

Moving to Python3 and away from FreeCAD as a dependency
-------------------------------------------

Adam Urbańczyk has been working hard on his own `CQ fork <https://github.com/adam-urbanczyk/cadquery>`_ which uses only PythonOCC instead of FreeCAD.

Work has begun on Cadquery 2.0, which will feature:

#. Feature trees, for more powerful selection
#. Direct use of OpenCascade Community Edition (OCE), so that it is no longer required to install FreeCAD

The project page can be found here: `https://github.com/dcowden/cadquery/projects/1 <https://github.com/dcowden/cadquery/projects/1>`_

A more detailed description of the plan for CQ 2.0 is `here <https://docs.google.com/document/d/1cXuxBkVeYmGOo34MGRdG7E3ILypQqkrJ26oVf3CUSPQ>`_
