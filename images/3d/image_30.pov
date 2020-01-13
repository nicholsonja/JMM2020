#version 3.7;

#include "colors.inc"
#include "textures.inc"
#include "functions.inc"
#include "strings.inc"

#declare PI = 3.14159265359;

camera {
    location <0, 0, -30>
    look_at 0
    right x * image_width/image_height
}
background { color White } 
light_source { <3000, 3000, -1000> White }


#declare MAIN_RADIUS = 10;

/*
plane {
    <0, 1, 0>, 
    -SPHERE_RADIUS 
    pigment {
      color White
    }
  }
*/

#macro make_circle(circ_radius, center, circ_size, circ_color)
    torus {
        circ_radius,
        circ_size
        texture { pigment { color circ_color } }
        rotate <90, 0, 0>
        translate center
    }
#end


#macro make_circle2(circ_radius, center, circ_size, circ_color)
    object {
        cylinder {
            <center.x, center.y + circ_size, center.z>,
            <center.x, center.y - circ_size, center.z>,
            circ_radius
            texture { pigment { color circ_color } }
            translate <0, -center.y, 0>
        }
        rotate <90, 0, 0>
        translate <0, center.y, 0>
    }
#end

#macro make_line(line_start, line_end, line_radius, line_color) 
    #if (line_start.x != line_end.x |
         line_start.y != line_end.y |
         line_start.z != line_end.z)
        cylinder {
            line_start, line_end
            line_radius
            texture { pigment { color line_color } }
        }
    #end
#end

#macro make_curve()  
    //union {
        //make_circle(MAIN_RADIUS, <0, 0, 0>, .25, rgbt <0, 0, 0, 0>  ) 
    
        #declare kA = 1;
        #declare kB = 2;
        #declare points = 101;
        #declare j = 0;
        #while (j < points) 
            #declare p_theta = 2 * PI / points * j;
    
            #declare pA = < MAIN_RADIUS * cos(kA * p_theta),
                            MAIN_RADIUS * sin(kA * p_theta),
                            0 >;
            #declare pB = < MAIN_RADIUS * cos(kB * p_theta),
                            MAIN_RADIUS * sin(kB * p_theta),
                            0 >;
            #declare p_center = (pA + pB) / 2;
            #declare p_radius = sqrt(
                                    pow(pA.x - p_center.x, 2) +
                                    pow(pA.y - p_center.y, 2) +
                                    pow(pA.z - p_center.z, 2));

            #if (pA.x != pB.x |
                 pA.y != pB.y |
                 pA.z != pB.z)
                    make_line(pA, pB, .02, rgbt <1, 0, 0, 0>  ) 
                    //make_circle(p_radius, p_center, .01, rgbt <0, 0, 0, 0>  ) 
                    //make_circle2(p_radius, p_center, .01, rgbt <0, 0, 1, .9>)
            #end

            #declare j = j + 1;
        #end

    //} 


#end

union {
      
    make_curve()
    //rotate <0, 0, -90>
    rotate <0, 45*clock, 0>
    
}
