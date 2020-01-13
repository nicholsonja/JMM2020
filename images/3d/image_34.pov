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
    location <0, 0, -44>
    look_at 0
    right x * image_width/image_height
}
background { color Black } 
//light_source { < 30,  30, -100> White }
//light_source { < 30, -30, -100> White }
//light_source { <-30, -30, -100> White }
//light_source { <-30,  30, -100> White }
light_source { <      45,     35,  -100> White }
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
    
        #declare kA = 2;
        #declare kB = 3;
        #declare points = 31;
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
            #declare p_radius = p_radius;
            #declare circle_center = p_center;

            #if (pA.x != pB.x |
                 pA.y != pB.y |
                 pA.z != pB.z)
                    //make_circle( p_radius, p_center, 
                     //            .05 , rgbt <0, 0, 1, 0>  ) 
                    //sphere{ circle_center, .1 texture { pigment { color rgbt <0, 0, 0, 0> } } }
                    #declare center_theta = atan2(circle_center.y, 
                                                  circle_center.x);
                    #declare moveVec = <
                            p_radius * cos(center_theta),
                            p_radius * sin(center_theta),
                            0>;

                    #declare moveVec = moveVec ;
                    //make_circle( p_radius, circle_center + moveVec, .01 , rgbt <1, 0, 0, 0>  ) 
                    difference {
                        sphere{ circle_center + moveVec, p_radius }
                        box { <100, 100, .5>, <-100, -100, -100> }
                        sphere{ circle_center + moveVec, p_radius - .05 }
                        texture { 
                            pigment { color rgbt <j/points * .5 + .5, 0, 0, 0>}
                        }
                        finish {
                            phong .1 
                            phong_size 20
                            }
                    }
            #end

            #declare j = j + 1;
        #end

    } 


#end

union {
      
    make_curve()
    //rotate <0, 0, -90>
    rotate <0, 45*clock, 0>
    
}
