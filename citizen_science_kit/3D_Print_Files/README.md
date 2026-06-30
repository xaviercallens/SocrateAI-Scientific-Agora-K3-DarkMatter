# Projet Caméléon : 3D Printable Optical Mounts 🕶️

This folder contains the CAD specifications and open-source **OpenSCAD** code to 3D print the custom mounts for the People's Interferometer.

All mounts are designed to be printed with standard **PLA, PETG, or ABS** filament, with standard 0.2mm layer height and a minimum of 20% infill for mechanical stability.

---

## 📂 Files Included

*   `mounts.scad`: A unified, parametric CAD file in OpenSCAD that allows you to render the three critical mechanical mounts:
    1.  **Laser Diode Mount**: Holds a 12mm cylindrical laser diode module securely.
    2.  **50/50 Beam Splitter Cube Base**: A snug nest for a 20x20mm optical glass cube.
    3.  **Kinematic Mirror Mount (2-Part)**: Includes a stable base and an adjustable front plate that pivots on three M3 screws and small compression springs to allow sub-micrometer angle tuning of the mirrors.

---

## 🖥️ How to Use OpenSCAD to Export STL Files

OpenSCAD is 100% free, open-source, and runs on Windows, macOS, and Linux.

1.  Download and install **[OpenSCAD](https://openscad.org/)**.
2.  Open the file `mounts.scad` in OpenSCAD.
3.  In the editor panel, locate the variable `PART_TO_RENDER` on line 11:
    *   Set `PART_TO_RENDER = "laser"` to view the Laser holder.
    *   Set `PART_TO_RENDER = "splitter"` to view the Beam Splitter base.
    *   Set `PART_TO_RENDER = "mirror_base"` to view the Mirror holder base.
    *   Set `PART_TO_RENDER = "mirror_plate"` to view the Mirror adjustable pivoting plate.
4.  Press **F6** to render the geometry.
5.  Click the **STL** button in the toolbar (or select *File -> Export as STL*) to save the printable `.stl` file.
6.  Slice the `.stl` file using your favorite slicer (Cura, PrusaSlicer, Bambu Studio) and print!

---

## ⚙️ Slicer & Hardware Recommendations

*   **Infill**: 20-30% Gyroid or Grid infill for excellent torsional rigidity.
*   **Perimeters / Walls**: 3 perimeters minimum.
*   **Additional Hardware Required**:
    *   6x **M3x20mm screws** (for the two kinematic mirror mounts, 3 per mount).
    *   6x **Small compression springs** (diameter 4-5mm, length 10-15mm - can be salvaged from cheap ballpoint pens).
    *   6x **M3 nuts** (pressed into the back-facing slots of the mirror mount base).
