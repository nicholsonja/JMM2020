#version 3.7;

#include "rad_def.inc"
global_settings { 
    assumed_gamma 1.0 
    radiosity {
      //Rad_Settings(Radiosity_IndoorHQ,off,off)
      Rad_Settings(Radiosity_Normal,off,off)
      //Rad_Settings(Radiosity_Fast ,off,off)
   }

}

#include "colors.inc"
#include "textures.inc"    
#include "glass.inc"
#include "functions.inc"
#include "strings.inc"

#declare PI = 3.14159265359;
#declare randomSeed = seed(12345);

camera {
    location <0, 0, -100>
    look_at 0
    right x * image_width/image_height
}
background { color Black } 

//light_source { <0, 0, -300> White }

#macro light(tran)
    light_source { <10, 0, -25> White 
                fade_distance 4 fade_power 2
                area_light x*3, y*3, 40, 40 
                circular orient adaptive 0
                translate tran
               }
#end

#declare lightStep = 10;
#declare lightMax = 10;

#declare lightX = -lightMax;
#while (lightX <= lightMax)
    #declare lightY = -lightMax;
    #while (lightY <= lightMax)
        light(<lightX, lightY, 0>)
        #declare lightY = lightY + lightStep;
    #end
    #declare lightX = lightX + lightStep;
#end


#macro make_petal_T1(freq)
   texture {
        pigment { 
            White
        } 
        //normal {
            //bumps .5
        //}
        finish {
            phong .5
        }
    }
#end

#macro make_petal_T2(rad, pet_color)
    texture {
        pigment {
            pet_color 
            filter .05
            /*
            warp{ 
                spherical
                orientation <0,0,1>
                dist_exp 0
            }
            warp {
                turbulence .1
            }*/
        }
        /*
        scale <rad, 1, rad>
        scale <1.075, 1, 1.075>
        normal {
            bumps .05
        }
        */
        finish {
            //specular .5 
            phong .1
        }
    }
#end

#macro make_circle(circ_radius, circ_size, circ_color)
    torus {
        circ_radius,
        circ_size
        texture { pigment { color circ_color } }
        rotate <90, 0, 0>
    }
#end

#macro make_circle2(main_radius, circ_radius, circ_size, petalColor)
    object {
        cylinder {
             <0, circ_size, 0>,
            -<0, circ_size, 0>,
            circ_radius
            //texture { pigment { circ_pigment } }
            //make_petal_T1(20 * circ_radius/main_radius)
            make_petal_T2(circ_radius, petalColor)
        }
        rotate <90, 0, 0>
    }
#end


#macro make_line(line_start, line_end, line_radius, line_color) 
    #if (line_start.x != line_end.x |
         line_start.y != line_end.y |
         line_start.z != line_end.z)
        union {
            cylinder {
                line_start, line_end
                line_radius
                texture { pigment { color line_color } }
            }
            sphere {
                <(line_start.x + line_end.x) / 2,
                 (line_start.y + line_end.y) / 2,
                 (line_start.z + line_end.z) / 2>
                .5
                texture { pigment { rgb <1, 0, 0> } }
            }
        }
    #end
#end


#macro make_curve(mainRadius, kA, kB, numPoints, circleScale, 
                  petalAngleRange, petalAngleAdjust, centerImage,
                  petalColor)  
    union {
        make_circle(mainRadius, .05, rgbt <0, 0, 0, 0>  ) 
   
        #local j = 0;
        #while (j < numPoints) 
            #local pTheta = 2 * PI / numPoints * j;
    
            #local pA = < mainRadius * cos(kA * pTheta),
                            mainRadius * sin(kA * pTheta),
                            0 >;

            #local pB = < mainRadius * cos(kB * pTheta),
                            mainRadius * sin(kB * pTheta),
                            0 >;

            #local pCenter = (pA + pB) / 2;

            #local pRadius = sqrt(pow(pA.x - pCenter.x, 2) +
                                  pow(pA.y - pCenter.y, 2) +
                                  pow(pA.z - pCenter.z, 2));

            #local colorVar = .2 * (numPoints - 50)/ 160;
            #if (colorVar > .2) 
                #local colorVar = .2;
            #end
            #if (colorVar <  0) 
                #local colorVar = 0;
            #end

            #if (pA.x != pB.x |
                 pA.y != pB.y |
                 pA.z != pB.z) 

                #local petalColor = CRGB2HSV(petalColor);
                #local petalColor = petalColor + 
                                        <0, 0, rand(randomSeed) * (.1 + colorVar)>;
                #local petalColor = CHSV2RGB(petalColor);

                difference {
                    //union {
                    object {
                        //make_line( <pRadius, 0, 0>, 
                                //-<pRadius, 0, 0>, 
                                //.02, rgbt <0, 0, 1, 0>  ) 
                        //make_circle(pRadius,  
                                    //.01, rgbt <0, 0, 0, 0>  ) 
                        make_circle2(mainRadius, pRadius, .001, petalColor )
                        scale circleScale
                        rotate <0, 
                                abs((j - numPoints/2)/(numPoints/2)) * 
                                                  petalAngleRange + petalAngleAdjust
                                0>
                        translate <mainRadius, 0, 0>
                        rotate <0, 0, 180 * kA * pTheta / PI>

                    }
                    cylinder {
                        <0, 0, 100>,
                        <0, 0, -100>
                        mainRadius
                    }

                    /*
                    texture { 
                        pigment{color White}
                        normal {bumps 0.5 scale <0.5,0.15,0.005> } 
                        finish {ambient 0.35 diffuse 0.55 phong .4 
                                reflection 0.2}
                        rotate <90, 0, 0>
                    }
                    */
                    /*
                    texture {
                        pigment { 
                            color petalColor // filter .5
                        }
                        normal { 
                            //bumps .05 
                            granite scale .5
                        }
                        finish {
                            //ambient .1
                            diffuse .8
                            //specular .1 
                            phong 0 
                            //reflection 1
                        }
                    } 
                    */
                }
            #end

            #local j = j + 1;
        #end

        // Lens center
        object {
            intersection {
                sphere { <0, 0, 0>, 1
                    translate -0.5*z
                }
                sphere { <0, 0, 0>, 1
                    translate 0.5*z
                }
            }
            scale <mainRadius + 1.6, mainRadius + 1.6, 8>
            pigment {
                image_map { 
                    png centerImage gamma 2.0
                    once
                    map_type 0
                }
                translate -.5 * x
                translate -.5 * y
                scale <2.1 * (mainRadius), 1, 1>
                scale <1, 2.1 * (mainRadius), 1>
                rotate <1, 1, 180>
            }
            finish { 
                emission  .5
                specular .01 
                phong  0
            }
            normal { bumps .05 }
        }
    } 


#end




object {

    make_curve(
            10,              // main radius
            2, 3,            // kA, kB
            65,              // numPoints
            <3, .5, 1>,       // circleScale
            66,              // petalAngleRange
            0,              // petalAngleAdjust 
            "../image_371.png", // centerImage
            color rgb<0, 1, 1>  // petalColor
        ) 
    rotate <0, 0, -70>
    rotate <15, 0, 0>
 
    rotate <0, 45*clock, 0>
    
}
