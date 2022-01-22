#Crossword solver project

This software can be used to read crosswords in following format:

"0" - empty_space
"*" - must be filled with digit
any other digit - counts as already known

So, this will be a valid crossword

```markdown
0g00
0o00
**ue
0*00
```

solutions to this crossword can be "blue" and "gold".

##Word sources

Program is tailored to Godville game words.
It can support using default.txt file with manually placed words (this part is limited only by your imagination).

On file parsing tokenization takes place. For this operation help_script.py can be used

After words were read, for each word in puzzle, it searches first in **default.txt** file,
than in **search_cache.txt**
If suitable word was not found, special request to Godville database website fetches 
this word using regular expression with '.' operators (any character) at vacant places.

All search results get tokenized and cached in **search_cache.txt**.