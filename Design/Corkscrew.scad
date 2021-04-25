// units: mm

$fn = 150;

linear_extrude(height = 60, twist = 360) {
    square([8, 60], center = true);
}

difference() {
    translate([-27, 25, -2.5])
        cube([60, 10, 5], center = true);
    translate([-35, 25])
        cylinder(d = 4, h = 15, center = true);
}

difference() {
    translate([-27, -25, -2.5])
        cube([60, 10, 5], center = true);
    translate([-35, -25])
        cylinder(d = 4, h = 15, center = true);
}

difference() {
    translate([-60, 0, -2.5])
        cube([10, 60, 5], center = true);
    translate([-60, 25])
        cylinder(d = 4, h = 15, center = true);
    translate([-60, -25])
        cylinder(d = 4, h = 15, center = true);
    translate([-60, -25])
        cylinder(d = 4, h = 15, center = true);
}

translate([0, 0, -2.5])
    cube([5, 60, 5], center = true);
