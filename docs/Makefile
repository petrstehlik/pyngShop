NAME=part1

all:
	latex $(NAME).tex
	dvips -t a4 $(NAME).dvi
	ps2pdf -sPAPERSIZE=a4 $(NAME).ps 

clean:
	-rm -f $(NAME).aux $(NAME).ps $(NAME).dvi $(NAME).log