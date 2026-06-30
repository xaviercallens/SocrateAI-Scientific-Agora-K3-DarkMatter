/*
  Projet Caméléon: Optical Mounts for Citizen Science Interferometer
  Designed by Xavier Callens & Agora Swarm Architecture
  License: Strong Copyleft (GPL v3)
  
  Parametric OpenSCAD design for Laser holder, Beam Splitter holder, and Mirror holders.
*/

$fn = 100; // Render resolution

// Choose which part you want to render: "laser", "splitter", "mirror_base", "mirror_plate"
PART_TO_RENDER = "mirror_base"; 

// --- 1. PARAMETERS ---
laser_diameter = 12.1; // 12mm laser diode module + clearance
cube_size = 20.2;      // 20mm beam splitter + clearance
mirror_size = 25.4;    // 25.4mm (1-inch) first-surface mirror + clearance
base_thickness = 5.0;  // Mounting base thickness

// --- 2. RENDER SWITCHBOARD ---
if (PART_TO_RENDER == "laser") {
    render_laser_holder();
} else if (PART_TO_RENDER == "splitter") {
    render_splitter_holder();
} else if (PART_TO_RENDER == "mirror_base") {
    render_mirror_mount_base();
} else if (PART_TO_RENDER == "mirror_plate") {
    render_mirror_mount_plate();
}

// --- 3. MODULES ---

module render_laser_holder() {
    difference() {
        // Main block
        cube([25, 30, 25], center=true);
        
        // Horizontal laser diode tunnel
        rotate([0, 90, 0])
            cylinder(d=laser_diameter, h=40, center=true);
        
        // Vertical tightening screw slot
        cube([3, 40, 15], center=true);
        
        // Tightening screw cross-bore (M3)
        translate([0, 8, 8])
            rotate([90, 0, 0])
                cylinder(d=3.3, h=40, center=true);
                
        // Base plate screw holes for securing to wood board
        translate([0, -10, -12.5])
            cylinder(d=3.5, h=10, center=true);
    }
}

module render_splitter_holder() {
    difference() {
        // Base block
        cube([cube_size + 8, cube_size + 8, base_thickness + 10], center=true);
        
        // Deep square pocket to press-fit the 50/50 glass cube
        translate([0, 0, base_thickness/2 + 1])
            cube([cube_size, cube_size, 12], center=true);
            
        // Clean optical passage tunnels in X and Y directions
        rotate([0, 90, 0])
            cylinder(d=15, h=40, center=true);
        rotate([90, 0, 0])
            cylinder(d=15, h=40, center=true);
            
        // Base board mounting holes
        translate([-(cube_size/2 + 2), -(cube_size/2 + 2), -5])
            cylinder(d=3.2, h=15, center=true);
        translate([cube_size/2 + 2, cube_size/2 + 2, -5])
            cylinder(d=3.2, h=15, center=true);
    }
}

module render_mirror_mount_base() {
    difference() {
        // Vertical backplate base block
        cube([35, 10, 35], center=true);
        
        // Central hole for light passage and mirror baseboard screw
        rotate([90, 0, 0])
            cylinder(d=16, h=20, center=true);
            
        // 3x Pivoting adjustment screw holes (M3) arranged in an L-shape
        // Hole 1: Top left
        translate([-12, 0, 12])
            rotate([90, 0, 0])
                cylinder(d=3.2, h=20, center=true);
        // Hexagonal M3 nut trap on the back-facing surface
        translate([-12, 3, 12])
            rotate([90, 0, 0])
                cylinder(d=6.2, h=5, $fn=6, center=true);
                
        // Hole 2: Top right
        translate([12, 0, 12])
            rotate([90, 0, 0])
                cylinder(d=3.2, h=20, center=true);
        translate([12, 3, 12])
            rotate([90, 0, 0])
                cylinder(d=6.2, h=5, $fn=6, center=true);
                
        // Hole 3: Bottom center
        translate([0, 0, -12])
            rotate([90, 0, 0])
                cylinder(d=3.2, h=20, center=true);
        translate([0, 3, -12])
            rotate([90, 0, 0])
                cylinder(d=6.2, h=5, $fn=6, center=true);
                
        // Bottom feet baseboard wood screw holes
        translate([-12, -5, -12])
            rotate([0, 90, 90])
                cylinder(d=3.5, h=10, center=true);
    }
}

module render_mirror_mount_plate() {
    difference() {
        // Vertical pivoting plate
        cube([35, 6, 35], center=true);
        
        // Shallow circular pocket to glue the 25.4mm first-surface glass mirror
        translate([0, -2, 0])
            rotate([90, 0, 0])
                cylinder(d=mirror_size, h=4, center=true);
                
        // 3x Screw insertion pockets matching the baseplate L-shape adjustment holes
        // Hole 1: Top left
        translate([-12, 0, 12])
            rotate([90, 0, 0])
                cylinder(d=3.0, h=10, center=true);
                
        // Hole 2: Top right
        translate([12, 0, 12])
            rotate([90, 0, 0])
                cylinder(d=3.0, h=10, center=true);
                
        // Hole 3: Bottom center
        translate([0, 0, -12])
            rotate([90, 0, 0])
                cylinder(d=3.0, h=10, center=true);
    }
}
