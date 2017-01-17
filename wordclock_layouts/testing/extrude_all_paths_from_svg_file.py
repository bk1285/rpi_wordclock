# extrude_all_paths_from_svg_file.py
# a generic script that extrudes all paths of a svg file
# created by charlyoleg on 2013/05/08
# license: CC BY SA 3.0

FREECADPATH='/usr/lib/freecad/lib' # adapt this path to your system
input_svg_file="stancil_front.svg" # relative path from the working directory to the svg file

import sys
# choose your favorite test to check if you are running with FreeCAD GUI or traditional Python
freecad_gui = True
#if not(FREECADPATH in sys.path): # test based on PYTHONPATH
if not("FreeCAD" in dir()):       # test based on loaded module
  freecad_gui = False
print("dbg102: freecad_gui:", freecad_gui)

if not(freecad_gui):
  print("dbg101: add FREECADPATH to sys.path")
  sys.path.append(FREECADPATH)
  import FreeCAD

print("FreeCAD.Version:", FreeCAD.Version())
#FreeCAD.Console.PrintMessage("Hello from PrintMessage!\n") # avoid using this method because it is not printed in the FreeCAD GUI

import Part
from FreeCAD import Base

print("dbg111: start building the 3D part")

my_tmp_doc = FreeCAD.newDocument("doc_blabla") # you can create implicitly the document "doc_blabla" by using it!
import importSVG
importSVG.insert(input_svg_file,"doc_blabla")

my_solids = []
for obj in my_tmp_doc.Objects:
  my_svg_shape = obj.Shape
  my_svg_wire = Part.Wire(my_svg_shape.Edges)
  my_svg_face = Part.Face(my_svg_wire)
  # extrusion
  my_solids.append(my_svg_face.extrude(Base.Vector(0,0,2))) # straight linear extrusion

my_compound = Part.makeCompound(my_solids)

## view and export your 3D part
output_stl_file="test_extrude_all_paths_from_svg_file.stl"
Part.show(my_compound) # works only with FreeCAD GUI, ignore otherwise
my_compound.exportStl(output_stl_file)
print("output stl file: %s"%(output_stl_file))
#
print("dbg999: end of script")
#
