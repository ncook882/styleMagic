#/.ipython/extensions/styleCells.py

'''
This file implements the %style magic using the 'styleCellMagics class. The
%style magic is currently designed to only theme the cell magics, but could
be extended. The ultimate execution of the magic is to simply apply the 
IPython HTML display call on a .css file enclosed by <style> brackets,
which IPython then dynamically applies to the current notebook.

This is an attempt at a more sophisticated implementation of a magic, and
by virtue an extension of IPython using the Magics class in conjunction with
argument parsing and other fancy things to make a robust and self-consistent
style magic.

The magic uses a basic autocompleter, created upon loading, which references
the available .css style files within the themes folder for quick loading.

Usage:
    
    %style theme
    
Positional arguments:
    theme - theme name from standard directory '.ipython/themes'



'''



#-------------------------------------------------------
# imports
#-------------------------------------------------------

#stdlib
import os
import glob

#ipython
from IPython.core.magic import Magics, magics_class, line_magic
from IPython.core.magic_arguments import (argument, magic_arguments, parse_argstring)
from IPython.utils.path import get_ipython_dir
from IPython.core.display import HTML
from IPython.core.completerlib import quick_completer

@magics_class
class StyleMagics(Magics):
    
    #this initializion is used to allow for the possibility of additional arguments!
    def __init__(self,shell): 
        super(StyleMagics,self).__init__(shell)
        self.stylepath = os.path.join(get_ipython_dir(),"themes")

    def __dir__(self):
        return self.getThemes().keys()
    
    def getThemes(self):
        '''Return dictionary of .css themes in path'''
        return dict([(str(os.path.split(f)[-1].split('.')[0]), f) for f in glob.glob(self.stylepath+"\*.css")])  
        
        
    @line_magic
    @magic_arguments()
    @argument('theme', nargs='?', default=None, help='your theme')
    #@argument('shade', nargs='?', default=None, help='shade')
    #@argument('file', )
    def style(self,args):
        #parse the magick arguments
        args = parse_argstring(self.style,args)
        theme = args.theme
        
        #location of theme .css files
        #csspath = os.path.join(get_ipython_dir(),"themes")
        
        #Note: os.path.split(f)[-1].split('.')[0]  splits the file path, takes
        # last part (-1) which contains the file name 'theme.css', then splits
        #the 'theme' string
        #themes = dict([(os.path.split(f)[-1].split('.')[0], f) for f in glob.glob(csspath+"\*.css")])  

        themes = self.getThemes()
        
        if not theme in themes.keys():
            print("theme must be present in .ipython/themes dir, defaulting to 'default'")
            print("Available themes:")
            for t in themes.keys():
                print("\t{}".format(t))
            theme = 'default'
            
        #edit .css
        with open(themes[theme], 'r') as f:
            text = f.read()

        #parse text to add proper ipython monikers
        #add <style> brackets to text
        newtext = "<style> \n \n" + text.replace(theme, 'ipython') + "\n <\style>"

        return HTML(newtext)        
        
        
#now need to define function for registering the magic upon %load_ext
def load_ipython_extension(ipython):
    styleMagic = StyleMagics(ipython)
    #quick and dirty completer definition
    quick_completer('%style', styleMagic.getThemes().keys())
    ipython.register_magics(styleMagic)