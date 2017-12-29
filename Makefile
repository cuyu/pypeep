build: clean
	python setup.py sdist
	twine upload dist/*

clean:
	rm -rf dist

test:
	python setup.py test
	coveralls
