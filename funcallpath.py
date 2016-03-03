from idaapi import *
f = 0
#Edit bt Christine , 2
#input sensitive API names and find their function calls paths
haohao = {} #function calls lists
path = [] #single path to targrt function
allPath = [] #all path to target function
# ________________________________________________

#callback list
def traverse(func,path): #callback list
    path.append(func)
    isCircle = 0 #flag as a function call circle
    for key in haohao.keys():#find all funcs call 'func'
        if func in haohao.get(key):
            if(key not in path):
                traverse(key,path)
            else:
                isCircle = 1 #circle
    
    if(isCircle == 0 and (path not in allPath)):
        currentPath = []
        for Point in path:
            currentPath.insert(0,Point)
        allPath.append(currentPath)
    path.pop()
#________________________________________________

#main call
if __name__=='__main__':
    Wait()
    file = AskFile(1,".txt","Select txt save file") #choose dir path and file name
    print(file)
    if not file:
        print("Cancel storing path information!\n")
    else:
        funcname = askstr(1,"_string","input function name:") #input function name
        print("Function name:%s" % funcname)
        for f in Functions():
            haohaolist = []
            if not f is None:
                fname = Name(f) #get function name
                fend = GetFunctionAttr(f,FUNCATTR_START)
                items = FuncItems(f)
                #Message("Function:%s,starts at %x, ends at %x\n" % (fname,f,fend))
                for i in items:
                    for xref in XrefsFrom(i,0):
                        if xref.type == fl_CN or xref.type == fl_CF:
                            #Message("\t%s -> %s\n" % (fname,Name(xref.to)))
                            haohaolist.append(Name(xref.to))
                haohao[fname] = haohaolist
        with open(file,'w') as fd:
            fd.write("Function %s calls as following list:\n" % funcname)
            traverse(funcname,path)
            for paths in allPath:
                if(len(paths)==1 and len(allPath)==1):
                    print("No function calls %s\n" % funcname)
                    fd.write("No function calls "+funcname+"\n")
                    break
                for functioncall in paths:
                    if(len(paths)!=1):
                        if(functioncall!=funcname):
                            fd.write(functioncall+" -> ")
                            print(functioncall+" -> ")
                        else:
                            fd.write(functioncall+"\n")
                            print(functioncall+"\n")
        fd.close()
#Exit(0)




