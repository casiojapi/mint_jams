# Default target (optional, can be left out if you prefer explicit commands)
all: build

# Clean: Remove all .html files
clean:
	rm -f *.html

# Build: Clean and generate HTML files
build: clean
	python3 script.py
	cp cordoba-mono-21.html index.html

# Publish: Build, then add, commit, and push to Git
publish: build
	git add .
	git commit -m "NEW PICTURE UPDATE"
	git push

# Phony targets (not actual files)
.PHONY: all clean build publish
