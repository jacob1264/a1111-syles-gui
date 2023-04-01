# a1111-syles-gui
A basic GUI styles.csv editor based in tkinter for Stable Diffusion Automatic1111 release.
I made this quickly to deal with my frustrations in dealing with A1111's styles dropdown and it's lack of basic features.

## How to use

Copy styles.py to the root of your Stable Diffusion Web UI folder.
```
python styles.py
```

## Features

* Rename Styles
* Delete Styles
* Create New Styles
* Copy Styles
* Edit Prompts and Negative Prompt
* Organize Styles, Move them Up or Down in the List

## Dependencies

* This tool relies on the pandas library for parsing csv data
```
pip install pandas
```
There were issues with the formatting of styles.csv that prevented me from utilizing python's built in csv library

## Future

* This would be better as an A1111 extension
* I am not planning on updating this unless I personally want more features 

![styles.py UI screenshot](/styles.py-screenshot1.png "GUI")

![A1111 organized styles](/styles.py-screenshot2.png "Organize your styles")
