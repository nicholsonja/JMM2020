#version 3.7;

global_settings { 
    assumed_gamma 1.0 
}

#include "colors.inc"
#include "textures.inc"    
#include "glass.inc"
#include "functions.inc"
#include "strings.inc"

#declare PI = 3.14159265359;

camera {
    location <0, 0, -21>
    look_at 0
    right x * image_width/image_height
}
background { color Black } 
//light_source { < 0,  0, -1000> White }
//light_source { < 30, -30, -100> White }
//light_source { <-30, -30, -100> White }
light_source { <-10,  10, -5> rgb <.5, .5, 1> }
light_source { <      45,     35,  -25> White }
light_source { <      30,    -30,  -50> White }

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


#macro make_curve() 
    union {
        //make_circle(MAIN_RADIUS, <0, 0, 0>, .25, rgbt <0, 0, 0, 0>  ) 
    
        #declare kA = 4;
        #declare kB = 5;
        #declare points = 5001;
        #declare j = 0;
        #while (j < points) 
            #declare p_theta = 2 * PI / points * j;
    
            #declare pA = < MAIN_RADIUS * cos(2 * kA * p_theta) * cos(kA * p_theta),
                            MAIN_RADIUS * cos(2 * kA * p_theta) * sin(kA * p_theta),
                            0 >;
            #declare pB = < MAIN_RADIUS * cos(2 * kB * p_theta) * cos(kB * p_theta),
                            MAIN_RADIUS * cos(2 * kB * p_theta) * sin(kB * p_theta),
                            0 >;
            #declare p_center = (pA + pB) / 2;
            #declare p_radius = sqrt(
                                    pow(pA.x - p_center.x, 2) +
                                    pow(pA.y - p_center.y, 2) +
                                    pow(pA.z - p_center.z, 2));
            #declare p_radius = p_radius;
            #declare circle_center = p_center;

            #if (pA.x != pB.x |
                 pA.y != pB.y |
                 pA.z != pB.z)
                    /*
                    cylinder {
                        pA, pB, .01
                        texture { pigment { color rgbt <0, 0, 0, 0> } } 
                    }
                    */

                    cylinder {
                        circle_center + <0, 0,  p_radius * .5>,
                        circle_center + <0, 0, -p_radius * .5>,
                        p_radius * .01
                    }
                    
                    /*
                    sphere{ 
                        pA, .1 
                        texture { pigment { color rgbt <0, 0, 0, 0> } } 
                    }
                    sphere{ 
                        pB, .1 
                        texture { pigment { color rgbt <1, 0, 0, 0> } } 
                    }
                    */
            #end

            #declare j = j + 1;
        #end 
        
        texture { 
            Polished_Brass
        } 
        texture { 
            pigment { color rgbt <.5, .5, 1, .95> } 
        } 
        finish { 
            phong .8 
            metallic
            reflection { 0.03, 1 }
            }
    } 


#end

union {
      
    make_curve()
    //rotate <0, 0, -90>
    rotate <0, 45*clock, 0>
    
}
