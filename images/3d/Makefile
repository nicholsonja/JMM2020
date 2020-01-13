POVRAY=/cygdrive/c/Program\ Files/POV-Ray/v3.7/bin/pvengine 
POVRAY_ARGS=/nr /exit /render 

# can do
# SIZE=
# SIZE=[small]
# SIZE=[huge]
# 
# on command line
#     make SIZE=[huge]
# or other options
SIZE=

povImages := $(patsubst %.pov,%.png,$(wildcard image*.pov))

all : ${povImages}

${povImages}: image%.png : image%.tga
	convert $< -trim $@
	#convert $< $@
	cp $@ ../

image%.tga : image%.pov POVRAY.INI Makefile
	${POVRAY} ${POVRAY_ARGS} $< POVRAY.INI${SIZE}

clean:
	rm -f *.tga  *.png  *.pov-state

