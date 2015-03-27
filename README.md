# styleMagic
basic magic function for ipython notebook designed to implement code-mirror styles with css

This file, when loaded as an extension into IPython, implements a `%style` magic, which dynamically modifies the 
[CodeMirror](https://codemirror.net/) implementation of your current IPython instance using IPython's `display` module.
This allows for immediate and flexible adjustment of the code cell theme without defining a profile-specific custom.css
file. This snippet of code was mostly made for the purpose of experimentation with IPython, and is by no means a 
sophisticated implemenation.

###Usage

> `%style <theme>`

Executing this cell will call IPython's display method to update the current notebook instance. It is currently designed to
search for '.css' files in the user's .ipython directory, in a subdirectory labeled "themes/". The magic supports a very simple
tab-completion which precompiles a list of available themes based on the '.css' files found in the "themes" directory.

Because the theme is implemented dynamically, reverting to the original theme can be done by interrupting or removing the original
call cell, or overwriting the theme with `%style default`. 