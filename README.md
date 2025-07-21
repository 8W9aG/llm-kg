# llm-kg

<a href="https://pypi.org/project/llmkg/">
    <img alt="PyPi" src="https://img.shields.io/pypi/v/llmkg">
</a>

A knowledge graph generator using LLMs.

## Dependencies :globe_with_meridians:

Python 3.11.6:

- [timefhuman](https://github.com/alvinwan/timefhuman)
- [nltk](https://www.nltk.org/)
- [instructor](https://python.useinstructor.com/)
- [groq](https://github.com/groq/groq-python)
- [pydantic](https://docs.pydantic.dev/latest/)
- [textblob](https://textblob.readthedocs.io/en/dev/)

## Raison D'être :thought_balloon:

`llm-kg` is a package that uses LLMs to extract knowledge graphs from freeform text.

## Architecture :triangular_ruler:

`llm-kg` calls an LLM using Groq to turn text into a series of triples.

## Installation :inbox_tray:

This is a python package hosted on pypi, so to install simply run the following command:

`pip install llmkgext`

or install using this local repository:

`python setup.py install --old-and-unmanageable`

## Usage example :eyes:

The use of `llmkgext` is entirely through code due to it being a library. It has exactly the same semantics as a requests session:

```python
from llmkgext import extract


triples = extract("Rodrigo Martins Vaz, known as Rodrigo (born 24 May 1971), is a retired Brazilian footballer.")
print(triples)
```

## License :memo:

The project is available under the [MIT License](LICENSE).
