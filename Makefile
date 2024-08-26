docs:
	python -m sphinx -T -b html -d docs/_build/doctrees -D language=en docs docs/_build/html

clean:
	rm -rf docs/_build