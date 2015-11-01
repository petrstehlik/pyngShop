NAME=part1

all:
	latex $(NAME).tex
	dvips -t a4 $(NAME).dvi
	ps2pdf -sPAPERSIZE=a4 $(NAME).ps
	rm -f $(NAME).aux $(NAME).ps $(NAME).dvi $(NAME).dvi $(NAME).fls $(NAME).fdb_latexmk $(NAME).synctex.gz $(NAME).log

clean:
	rm -f $(NAME).aux $(NAME).ps $(NAME).dvi $(NAME).dvi $(NAME).fls $(NAME).fdb_latexmk $(NAME).synctex.gz $(NAME).log