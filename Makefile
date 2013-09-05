# Keeps a few frequent commands

cleantemp = rm -rf build; rm -f *.c

.PHONY : clean all gitdeps

all: gitdeps

clean: 
	$(cleantmp)
	find . -name '*pyc' -exec rm -f {} \;
	rm -f *.so
	rm -rf __pycache__


gitdeps:
	git submodule init
	git submodule update --recursive
	git submodule foreach git pull origin master
