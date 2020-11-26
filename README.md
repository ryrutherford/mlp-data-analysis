# My Little Pony Script Analysis Project
## Project Goals
- In this project we are computing statistics based on scripts from the TV show My Little Pony
- We are using the clean_dialog.csv file from: https://www.kaggle.com/liury123/my-little-pony-transcript as our data source
- Our goal is to:
	- Compute the percentage of dialog that each of the 6 Ponies take up
	- Compute the percentage of mentions that each pony makes about the 5 other ponies
	- Compute the percentage of times that each pony has a line that directly follows another pony or non-pony character's line (non-pony characters are treated as one group)
	- Generate a list of the 5 most used non-dictionary words by each pony
	- Determine the highest scoring words for each pony using tfidf

## Tools used
- Python
	- Pandas
	- Regular Expressions
	- Argparse
	- OS.path
- Vim, VSCode
