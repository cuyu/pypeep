build: clean
	python setup.py sdist
	twine upload dist/*

clean:
	rm -rf dist

test:
	pytest --cov=pypeep
	coveralls
