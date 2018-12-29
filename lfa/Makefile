JFLAGS = -g
JC = javac
JVM = java
JFLEX = ./lib/jflex-1.6.1.jar

all: build

Flexer.java: flexer.flex
	$(JVM) -jar $(JFLEX) $<

sources = $(wildcard *.java)
classes = $(sources:.java=.class)

build: Flexer.java $(classes)

run:
	$(JVM) Main

.PHOONY: clean
clean :
	rm -f *.class Flexer.java *~
%.class : %.java
	$(JC) $(JFLAGS) $<
