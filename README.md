# Text2Html
------------
To Translate text document to html document, Easy to use no code needed
Just pass given argument into terminal or command prompt
Give input document as text document

## Use
--------

For more information on how to use or additional options, type **'--help'.**

```sh
Usage: python -m texttohtml.convert [FILE PATH] [-OPTIONS] [-OUTPUT FILE PATH]

    -o		On success, instead of writing to stdout, write to a file.
    -t		Adds the <!DOCTYPE html> header to the generated code.
    -d		[DEBUG] Each cycle the processor prints information about
		Html structure and file reader.

```
## Example:

**python -m texttohtml.convert elaa.txt -o elaa.html**

### title:

  **Ex:**
  
	** txt: **
	
	@title Title of your web page;
	
	Where @title indicates to apply style and ; indicates the end of style
	
	** output: **
	<title>Title of your web page</title>

### charset:

	@charset utf-8;
	
### lang:

	@lang en;

		To choose the language which you want to show
	
### description:

	@description

		To Describe the page using this style
	
### keywords:

	@keywords 

		To assign keywords easily top of search engine
	
### author:

	@author

		Author of the page
	
# h1:
	
	@h1 
		Heading Style 1
		
## h2:

	@h2 
		Heading Style 2
			
### h3:

	@h3 
		Heading Style 3
	
#### h4:

	@h4 
		Heading Style 4
	
##### h5:

	@h5 
		Heading Style 5
	
###### h6:

	@h6 
		Heading Style 6
	
### p:

	@p
		Paragraph style
	
### pre:
	@pre
	
### code:
	@code
	
### hr:
	@hr
	
### stylesheet:
	@stylesheet
	
### span:
	@span
	
### strong:
	@strong
### em:
	@em
	
### img:
	@img
	
### a:
	@a
	
### youtube:
	@youtube
	
