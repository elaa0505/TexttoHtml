'''
@author: elango
'''
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="texttohtml",
    version="1.0",
    author="Elango SK",
    author_email="elango111000@gmail.com",
    description="Easy to convert text document to html document",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/elaa0505/TexttoHtml",
    packages=setuptools.find_packages(),
    keywords = "text2html, Text to html, Text document to html, convert text to html, Convert html using text, Texttohtml",
    
)
