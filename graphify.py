
#--------------------------------------------------------------------##
#		my_print
#--------------------------------------------------------------------##
def my_print(mystring):
	print  mystring 
	print >> outfile, mystring
	
class Box:
        def __init__(self, my_name, my_born, my_died, my_xvalue, my_yvalue):
                self.name = my_name
                self.born = my_born
                self.died = my_died
                self.xvalue = my_xvalue
                self.yvalue = my_yvalue
                self.Items = dict()
        def set(self, variable, value):
                self.Items[variable]=value
        def remove_variable(self, variable):
                del self.Items[variable]
        def boxprint (self) :
                print "{0:<36s} {1:<12s} born: {2:5s} died: {3:5s} coordinates: ({4:4s}, {5:4s}) ".format(self.name,  self.Items['discipline'], self.born, self.died,   self.xvalue,   self.yvalue)
                for item in sorted(self.Items):
                        
                        print "{0:<12s} {1:<15s}".format(item, self.Items[item])
                       
#--------------------------------------------------------------------##
#		Main program 
#--------------------------------------------------------------------##

infolder = ""
#infolder = "..\\..\\books\\battle-images\\poster-new\\"
outfolder = ""
tablelines = []
datalines = []
size = 5
infilename = infolder +  "new-poster-with-sociology2-2-1.tex"
outfilename = outfolder + "python-generated-poster.tex"


infile = open(infilename) 
outfile = open (outfilename,mode='w')
#--------------------------------------------------------------------##
#		input
#--------------------------------------------------------------------##
lines_out_1 = []
lines_out_2 = []
lines_out_3 = []
lines_out_4 = []
lines_out_5 = []
lines_out_6 = []
lines_out_7 = []
lines_out_8 = []

xvalue=dict()
Boxes = dict()
datalines= infile.readlines()
length_of_previous_line = -1
currentDiscipline = ""
name = ""
born = ""
died = ""
 
Values= {       'blur': 'false',
                'discipline' : 'linguist',
                'fillcolor': 'black',
                'fillstyle': 'solid',
                'framearc': '0.5',
                'framesep' : '6pt',
                'gradangle': '135',
                'gradbegin': 'linguist1',
                'gradmidpoint': '0.5',
                'gradend': 'linguist2',
                'linecolor': 'black',
                'linestyle': 'solid',
                'linewidth': '3pt',                
                'shadow': 'false',
                'shadowcolor': 'black',
                'shadowsize': '2pt',
                'slopebegin': 'philpsych1',
                'slopeend': 'philpsych2',
                'slopesteps':'2'
        }
               

for line in datalines:	
	line = line.rstrip()
	if len(line) == 0:
	        continue
        elif line[:13] == "%% discipline":
                #print line
                currentDiscipline = line[13:].strip()
                #print currentDiscipline	        
	elif line[0] != "%":
	        line = line.split("%",1)[0]
	if line[0:11] == "\\newcommand":
	        pieces = line.split("{") 
	        variable1 = pieces[1][1:]  # remove initial 
	        variable1 = variable1[:-1] #remove final 
	        variable2 = pieces[2][:-1]
	        xvalue[variable1] = variable2
	elif line[0:5] == "\\rput": 
                
                line = line[5:]                 # strip rput
                piece1, piece2 = line.split(")",1) 
                if piece1[0:2] == "(\\": 
                        piece1 = piece1[2:]             #pull out symbolic variable
                elif line[0]=="(":                      # or else pull out numeric value
                        piece1 = piece1[1:]
                piece1 = piece1.strip()
                coordinates = piece1.split(",")  
                
               
                my_xvalue = coordinates[0]
                my_yvalue = coordinates[1]
                if my_xvalue in xvalue:
                        my_xvalue = xvalue[my_xvalue]
                  
                piece2 = piece2.strip()
                 
                if piece2[:13] == "{\\psframebox[":
                        piece2 = piece2[13:]
                      
                        items, remainder = piece2.split("]",1)
                        items = items.split(",")
                        
                        
                        
                elif piece2[:13] == "{\\psframebox{":
                        remainder= piece2[12:]
                        #print remainder
                        
                else: 
                        print "error!", line
                        print
                
                if remainder[:19] =="{\\begin{tabular}{c}": 
                        remainder = remainder[19:]
                         
                        
                if remainder[-15:] == "\\end{tabular}}}":
                        remainder = remainder[:-15 ]
                        if "\\\\" in remainder:
                                name, dates = remainder.split("\\\\", 1)
                                name = name.strip()
                                dates = dates.strip()
                                
                                born,died = dates.split("-")
                                 
                                
                        else:
                                name = remainder.strip()
                                
                                
                      
                myBox = Box(name, born,died, my_xvalue, my_yvalue)                
                Boxes[name] = myBox
                                #First take default values from Values, then overwrite by local "items"
                myBox.discipline = currentDiscipline

                for var in Values:
                        myBox.set(var,Values[var])      # these are the current default values.
                for item in items:                      # these are the values set in this particular box/person
                        variable, value = item.split("=")
                        myBox.set(variable, value)
                        #print variable, value, 166
                if myBox.Items["fillstyle"]=="none"  or myBox.Items["fillstyle"]=="solid":
                        myBox.remove_variable("gradbegin")
                        myBox.remove_variable("gradend")
                        myBox.remove_variable("gradangle")
                        myBox.remove_variable("slopesteps")
                        myBox.remove_variable("slopebegin")
                        myBox.remove_variable("slopeend")
                elif myBox.Items["fillstyle"]=="gradient":  
                        myBox.remove_variable("slopesteps")
                        myBox.remove_variable("slopebegin")
                        myBox.remove_variable("slopeend")
                elif myBox.Items["fillstyle"]=="slope" :
                        myBox.remove_variable("slopesteps")
                        myBox.remove_variable("slopebegin")
                        myBox.remove_variable("slopeend")
                if myBox.Items["shadow"]=="false":
                        myBox.remove_variable("shadowcolor")
                        myBox.remove_variable("shadowsize")
   
        

                 
        elif line[0:7] == "\\psset{":
                line = line[7:]
                line = line[:-1]
                
                items = line.split(",")
                for item in items:
                        item = item.strip()
                        if len(item) == 0:
                                continue
                        var, val = item.split("=")
                        if var == "xunit" or var == "yunit":
                                continue
                        if var not in Values:
                                print "Error" , var, val, line
                        else:   
                                Values[var] = val
                        if var == "discipline":
                                print "   ", var, val, 177
                 
        elif line[0:8] == "\\psframe":
                 line = line[8:] 
                
                 if line[0]=="[":
                        line            = line[1:]
                        parts           = line.split("]",1)
                        items           = parts[0]
                        coordinates     = parts[1]
                        #print line
                        items           = items.split(",")
                                                      
                        #print coordinates
                        #print items
                        #print
                 else:
                        coordinates = line
                 
                 #print coordinates, items
                 #print 
        elif line[:10]=="\\psellipse":
                 line = line[10:]
                 if line[0]=="[":
                        line            = line[1:]
                        parts           = line.split("]",1)
                        items           = parts[0]
                        coordinates     = parts[1]
                        #print line
                        items           = items.split(",")
                                                      
                        #print coordinates
                        #print items
                        #print
                 else:
                        coordinates = line
                        #print coordinates       
        elif line[:9]== "\\psbezier":
                line = line[9:].strip()
                #print 1, line   
                if line[0] == "[":
                        line = line[1:]
                        parts   = line.split("]",1)
                        items = parts[0].strip().split(",")
                        line = parts[1].strip()
                        #print 2, line
                if line[0] == "{":
                        parts = line.split("}", 1)
                        arrow = parts[0][1:]
                        #print arrow
                        line = parts[1]
                coordinates = line.split(")(")
                if len(coordinates) == 4:
                        coordinates[0]=coordinates[0][1:]
                        lastcoordinate = coordinates[len(coordinates)-1]
                        coordinates[len(coordinates)-1] = lastcoordinate[:len(lastcoordinate)-1]
                        #for coord in coordinates:
                        for i in range(len(coordinates)):
                                #print coordinates[i]
                                if coordinates[i][0]=="\\":
                                        #print "a"
                                        coordinates[i] = coordinates[i][1:]
                                        #print coordinates[i]
                                        if coordinates[i][0] == "\\":
                                                coordinates[i] = coordinates[i][1:]

                
                #print  arrow , items, coordinates
                #print 
                

 
                 
infile.close()
 
for name, box in sorted(Boxes.items()):
        box.boxprint()


#--------------------------------------------------------------------##
#		output
#--------------------------------------------------------------------##
 
 
 





outfile.close()
