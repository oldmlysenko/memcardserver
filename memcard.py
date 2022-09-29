import json
import datetime
import os
import threading



class AjaxReqProcessor():

    ERROR_KEY = 'error'
    RESULT_KEY = 'result'
    ID_KEY = 'id'
    ACTION_KEY = 'action'

    def __init__(self):
        pass


    def ProcessLocal(self,indata,outdata):
        return True;

    @property
    def ID(self):
        return self.__class__.__name__;



    def Process(self,indata,outdata):
        if not isinstance(indata, dict):
            return False
        if self.ID_KEY not in indata:
            return False
        if indata[self.ID_KEY]!=self.ID:
            return False
        if self.ACTION_KEY not in indata:
            outdata[self.RESULT_KEY]=None
            outdata[self.ERROR_KEY]='No "'+self.ACTION_KEY+'" key found'
            return True
            
        try:
            if self.ProcessLocal(indata,outdata):
                return True
        except Exception as  e:                    
            outdata[self.RESULT_KEY]=None
            outdata[self.ERROR_KEY]='Exception: '+str(e);
            return True

                
        outdata[self.RESULT_KEY]=None
        outdata[self.ERROR_KEY]='Action "'+indata[self.ACTION_KEY]+'" not supported'
        return True






class MemCard(AjaxReqProcessor):


   
    FILENAME_KEY = 'file'
    NEWFILENAME_KEY = 'newfile'
    TEXT_KEY = 'text'

    REQ_PREFIX = "mcreq"
    ACTION_LIST = "list"
    ACTION_GET = "get"
    ACTION_GETRAW = "getraw"
    ACTION_SETRAW = "setraw"
    
    ACTION_NEW = "new"
    ACTION_DEL = "del"
    ACTION_COPY = "copy"
    
    EXT = ".txt"

    COMMENT_CHAR = '#'

    SEPARATOR_STR = " -"

    def __init__(self,dirname,bakdirname):
        super().__init__()
        self.dir = dirname
        self.bakdir = bakdirname
        self.unique_prefix =  datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        self.unique_index =  1
        self.unique_lock = threading.Lock()
        
     
    
    def GetUniqueId(self):
        value = None
        with self.unique_lock:
            value = self.unique_prefix+"_"+str(self.unique_index)
            self.unique_index+=1
        return value
    
        
    def ProcessLocal(self,indata,outdata):
        
        outdata[self.ERROR_KEY]=None
        if indata[self.ACTION_KEY] == self.ACTION_LIST:
            outdata[self.RESULT_KEY]=self.List()
            return True
        if indata[self.ACTION_KEY] == self.ACTION_GET:
            outdata[self.RESULT_KEY]=self.Get(indata[self.FILENAME_KEY])
            return True
        if indata[self.ACTION_KEY] == self.ACTION_GETRAW:
            outdata[self.RESULT_KEY]=self.GetRAW(indata[self.FILENAME_KEY])
            return True           
        if indata[self.ACTION_KEY] == self.ACTION_SETRAW:
            outdata[self.RESULT_KEY]=self.SetRAW(indata[self.FILENAME_KEY],indata[self.NEWFILENAME_KEY],indata[self.TEXT_KEY],True)
            return True        
        if indata[self.ACTION_KEY] == self.ACTION_NEW:
            outdata[self.RESULT_KEY]=self.CreateNew()
            return True     
        if indata[self.ACTION_KEY] == self.ACTION_DEL:
            outdata[self.RESULT_KEY]=self.Delete(indata[self.FILENAME_KEY])
            return True     
        if indata[self.ACTION_KEY] == self.ACTION_COPY:
            outdata[self.RESULT_KEY]=self.MakeACopy(indata[self.FILENAME_KEY],indata[self.NEWFILENAME_KEY])
            return True        

            
        return False

        
        
    
        
        
        
    def List(self):
        res=[]
        for f in os.listdir(self.dir):
            if f.endswith(self.EXT):
                res.append(f[0:-len(self.EXT)])
        return res;
        
        
        
    def ComposeTransDict(self,wordstr,transstr=""):
        wordstr = wordstr.replace("_", " " ).strip()
        transstr = transstr.strip()
        if (len(wordstr)==0):
            return None
        if (len(transstr)==0):
            transstr = "???"
        return { 'word': wordstr, 'trans': transstr  }
        
    def ParseDictLineDash(self,dashpos,text):   
        w = text[0:dashpos]
        t = text[dashpos+len(self.SEPARATOR_STR):]
        return self.ComposeTransDict(w,t);


    def ParseDictLineSpace(self,text):   
        p = text.split()
        if (len(p)==0):
            return None
        w = p[0]
        if (len(p)==1):
            return self.ComposeTransDict(w);
        t = " ".join(p[1:])
        return self.ComposeTransDict(w,t);

        
    def ParseDictLine(self,text):
        text = text.strip()
        if (text.startswith(self.COMMENT_CHAR)):
            return None
        n = text.find(self.SEPARATOR_STR)
        if (n != -1):
            return self.ParseDictLineDash(n,text)
        return self.ParseDictLineSpace(text)
            
        
        
    def Get(self,filename):

        fn = os.path.join(self.dir, filename+self.EXT)
        res = []
    
        f = open(fn, 'r')
        while True:
            line = f.readline()
            if not line:
                break
            r=self.ParseDictLine(line)
            if (r!=None):
                res.append(r)
        f.close()    
    
        return res
            #{ 'word': 'word1', 'trans':'trans1'  },
            
            
    def GetRAW(self,filename):
        fn = os.path.join(self.dir, filename+self.EXT)
        f = open(fn, 'r')
        text = f.read()
        f.close()
        return text

    


    def SetRAW(self,filename,newfilename,text,isbackup):
        if newfilename==None or len(newfilename)==0:
            newfilename = filename
        
        
        filepath = os.path.join(self.dir, filename+self.EXT)        
        newfilepath = os.path.join(self.dir, newfilename+self.EXT)  
        
        if (os.path.exists(filepath)):
            if (isbackup):
                bakfilepath = os.path.join(self.bakdir, filename+"_"+self.GetUniqueId()+self.EXT)
                os.rename(filepath, bakfilepath)
            else:
                os.remove(filepath, bakfilepath)
            
        f = open(newfilepath, 'w')
        f.write( text )
        f.close()
            
        self.DeleteOldFiles()
            
        return newfilename

            
    def DeleteOldFiles(self):
        #todo: implement
        pass 
            
            
            
            
            
    def CreateNew(self):
        index = 1
        while(True):
            filename = "collection_"+str(index)
            filepath = os.path.join(self.dir, filename+self.EXT) 
            if (not os.path.exists(filepath)):
                break
            index+=1
            
        defaulttext = "# line format: <word> - <translation>\r\nHello - привіт\r\nworld - світ" 
           
        return self.SetRAW(filename,None,defaulttext,False)
            


            
    def Delete(self,filename):
        filepath = os.path.join(self.dir, filename+self.EXT) 
        os.remove(filepath)
        return filename
       
            
            
    def MakeACopy(self,oldfilename,newfilename):
        
        if (newfilename==None):
            newfilename = oldfilename+"_copy"
        index = 1
        while(True):
            newfilepath = os.path.join(self.dir, newfilename+self.EXT) 
            if (not os.path.exists(newfilepath)):
                break
            newfilename = oldfilename+"_copy"+str(index)
            index+=1
            
        text = self.GetRAW(oldfilename)    

        return self.SetRAW(newfilename,None,text,False)
            
            
            
            
            
            
            
        
            
            
            
            
