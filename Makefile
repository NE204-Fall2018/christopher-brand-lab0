manuscript = report
latexopt = -file-line-error -halt-on-error

# Build the PDF of the lab report from the source files
$(manuscript).pdf: $(manuscript).tex text/*.tex references.bib images/*.png
	pdflatex $(latexopt) $(manuscript).tex
	bibtex $(manuscript).aux
	bibtex $(manuscript).aux
	pdflatex $(latexopt) $(manuscript).tex
	pdflatex $(latexopt) $(manuscript).tex

# Get/download necessary data
data :
	curl -L -o lab0_spectral_data.txt https://www.dropbox.com/s/hutmwip3681xlup/lab0_spectral_data.txt?dl=0 

# Validate that downloaded data is not corrupted
validate :
	curl -L -o lab0_spectral_data.md5sum https://www.dropbox.com/s/amumdrm9zp1kn8d/lab0_spectral_data.md5?dl=0 
	md5sum -c lab0_spectral_data.md5sum

# Run tests on analysis code
test :
	pytest
#	nosetests --no-byte-compile test/test_m*

# Automate running the analysis code
analysis :
	cd code/ && python calibration_lab0.py

clean :
	rm -f *.aux *.log *.bbl *.lof *.lot *.blg *.out *.toc *.run.xml *.bcf
	rm -f text/*.aux
	rm $(manuscript).pdf
	rm code/*.pyc

# Make keyword for commands that don't have dependencies
.PHONY : test data validate analysis clean
