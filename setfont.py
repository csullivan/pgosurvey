import pylab

def setfont(font='helvetica',unicode=True): 
    r""" 
    Set Matplotlibs rcParams to use LaTeX for font rendering. 
    Revert all changes by calling rcdefault() from matplotlib. 
    
    Parameters: 
    ----------- 
    font: string 
        "Helvetica" 
        "Times" 
        "Computer Modern" 
    
    usetex: Boolean 
        Use unicode. Default: False.     
    """ 
    
    # Use TeX for all figure text! 
    pylab.rc('text', usetex=True) 

    font = font.lower().replace(" ","") 
    if font == 'times': 
        # Times 
        font = {'family':'serif', 'serif':['Times']} 
        preamble  = r""" 
                       \usepackage{color} 
                       \usepackage{mathptmx} 
                    """ 
    elif font == 'helvetica': 
        # Helvetica 
        # set serif, too. Otherwise setting to times and then 
        # Helvetica causes an error. 
        font = {'family':'sans-serif','sans-serif':['Helvetica'], 
                'serif':['cm10']} 
        preamble  = r""" 
                       \usepackage{color} 
                       \usepackage[tx]{sfmath} 
                       \usepackage{helvet} 
                    """ 
    else: 
        # Computer modern serif 
        font = {'family':'serif', 'serif':['cm10']} 
        preamble  = r""" 
                       \usepackage{color} 
                    """ 
    
    if unicode: 
        # Unicode for Tex 
        #preamble =  r"""\usepackage[utf8]{inputenc}""" + preamble 
        # inputenc should be set automatically 
        pylab.rcParams['text.latex.unicode']=True 
    
    #print font, preamble 
    pylab.rc('font',**font) 
    pylab.rcParams['text.latex.preamble'] = preamble 

