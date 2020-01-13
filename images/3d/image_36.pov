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
    location <0, 0, -23>
    look_at 0
    right x * image_width/image_height
}
background { color Black } 
//light_source { < 0,  0, -1000> White }
//light_source { < 30, -30, -100> White }
//light_source { <-30, -30, -100> White }
//light_source { <-10,  10, 5> rgb <.5, .5, 1> }
light_source { <      0,    0,  10> rgb <1, 1, 1> }
#declare i = 0;
#declare nL = 4;
#while (i < nL)
    #declare theta = i / nL * 2 * pi;
    light_source { <100 * cos(theta), 100 * sin(theta),  -100> 
                   rgb <.1, .1, .1 >}
    #declare i = i + 1;
#end

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
    
        #declare kA = -1;
        #declare kB = 7;
        #declare points = 301;
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
                   
                    /*
                    cylinder {
                        pA, pB, .01
                        texture { pigment { color rgbt <1, 0, 0, 0> } } 
                    }
                    */
                    

                    #declare Text = text {
                            ttf "Arial.ttf" "JMM"
                            .2, 0
                            scale <1, 1, 5> * p_radius * .3
                            texture { 
                                pigment { color rgbt <.224, 1, .078, .4> }
                            } 
                        };
                    #declare Min = min_extent ( Text );
                    #declare Max = max_extent ( Text );
                    #declare line_theta = atan2(circle_center.y, 
                                                circle_center.x);
                    
                    #declare Text = object { 
                            Text 
                            translate -(Min + Max) / 2
                            //rotate <-90, 0, 0>
                            rotate <0, 0, line_theta * 180/pi>
                        };
                    object { 
                        Text 
                        translate circle_center + <p_radius * cos(line_theta),
                                                   p_radius * sin(line_theta),
                                                   p_radius * 2>
                    }
                    /*
                    sphere{ 
                        circle_center, .1 
                        texture { pigment { color rgbt <0, 0, 0, 0> } } 
                    }
                    */

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
        
    } 


#end

union {
      
    make_curve()
    //rotate <0, 0, -90>
    rotate <0, 45*clock, 0>
    
}
