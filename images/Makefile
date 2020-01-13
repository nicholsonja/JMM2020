pyImages := $(patsubst %.py,%.png,$(wildcard g*.py))
pyImages := $(patsubst genI%,i%,${pyImages})

javaDir=CurveStitching/src
package=cs
javaImages := $(patsubst %.java,%.png,$(wildcard ${javaDir}/${package}/Image*.java))
javaImages := $(patsubst ${javaDir}/${package}/%,%,${javaImages})
javaImages := $(patsubst I%,i%,${javaImages})

all: ${pyImages} ${javaImages} povImages

${pyImages}: image%.png : genImage%.py helper.py
	python3 $<
	convert $@ -trim tmp.png
	mv tmp.png $@

${javaImages}: image%.png : ${javaDir}/${package}/Image%.java ${javaDir}/${package}/CSDP.java
	( cd ${javaDir} ; \
      javac -d ../bin $(patsubst ${javaDir}/%,%,$<) ; \
      cd ../bin ; \
      java ${package}.Image$* ../.. \
    )
	convert $@ -trim tmp.png
	mv tmp.png $@

povImages:
	( cd 3d ; make SIZE=[huge])

clean:
	rm -rf *.png __pycache__ CurveStitching/bin/cs 
	( cd 3d ; make clean )

test: 
	echo ${javaImages}
