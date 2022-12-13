SHELL := /bin/bash

MAIN=report
TEXSRC=$(wildcard *.tex)
DIR_BUILD=build
OPT= --interaction=nonstopmode

all: $(DIR_BUILD)/$(MAIN).pdf

$(DIR_BUILD)/$(MAIN).pdf: $(TEXSRC)
	latexmk -pdf -pdflatex="texfot pdflatex" $(MAIN) -auxdir=$(DIR_BUILD) -outdir=$(DIR_BUILD)

clean:
	rm -f $(DIR_BUILD)/*
.PHONY: clean all