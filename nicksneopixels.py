import unicornhat as UH
def set_pixel(n, r, g, b):
    x = n//8
    if(x%2==0):
	    y = n%8
    else:
	    y = 7 - n%8
    UH.set_pixel(x, y, r, g, b)
	
def show():
    UH.show()