#!/bin/env python
import pickle
import datetime


class rcm_session:

    def __init__(self,fromstring='',fromfile='',file='',sessionname='',state='',node='',tunnel='',sessiontype='',nodelogin='',display='',jobid='',sessionid='',username='',walltime='',otp='', vncpassword=''):
        self.hash={'file':'','session name':'', 'state':'', 'node':'','tunnel':'','sessiontype':'', 'nodelogin':'', 'display':'', 'jobid':'', 'sessionid':'', 'username':'', 'walltime':'00:00:00','timeleft':'00:00:00', 'otp':'', 'vncpassword':''}
        if (fromfile != ''):
            self.hash=pickle.load(open(fromfile,"rb"))
        elif (fromstring != ''):
            self.hash=pickle.loads(fromstring)
        else:
            self.hash={'file':file, 'session name':sessionname ,'state':state, 'node':node, 'tunnel':tunnel, 'sessiontype':sessiontype, 'nodelogin':nodelogin,  'display':display, 'jobid':jobid, 'sessionid':sessionid, 'username':username, 'walltime':walltime,'timeleft':walltime, 'otp':otp, 'vncpassword':vncpassword}
            self.hash['created']=datetime.datetime.now().strftime("%Y%m%d-%H:%M:%S")
            
    def serialize(self,file):
        pickle.dump(self.hash, open( file, "wb" ) )

    def write(self,format):
        print "server output->"
        if ( format == 0):
            print pickle.dumps(self.hash)
        elif ( format == 1):
            for k in self.hash.keys():
                print "%s;%s" % ( k , self.hash[k] )
        elif ( format == 2):
            x=[]
            #for k in sorted(self.hash.keys()):
            for k in self.hash.keys():
                x.append(self.hash[k])
            print ";".join(x) 



class rcm_sessions:

    def __init__(self,fromstring='',fromfile='',sessions=[]):
        if (fromfile != ''):
            self.array=pickle.load(fromfile)
        elif (fromstring != ''):
            self.array=pickle.loads(fromstring)
        else:
            self.array=sessions

    def serialize(self,file):
        pickle.dump(self.array, open( file, "wb" ) )

    def get_string(self):
	return pickle.dumps(self.array)
    def write(self,format=0):
        print "server output->"
        if ( format == 0):
            print pickle.dumps(self.array)
        elif ( format == 1):
            for k in self.array:
                print "---------------------"
                k.write(1)
        elif ( format == 2):
            c=rcm_session()
            print ";".join(sorted(c.hash.keys())) 
            for k in self.array:
                k.write(2)

 
class rcm_config:

    def __init__(self,fromstring='',fromfile=''):
        if (fromfile != ''):
            self.config=pickle.load(open(fromfile,"rb"))
        elif (fromstring != ''):
            self.config=pickle.loads(fromstring)
        else:
            self.config={'version':{'checksum':'','url':''},'queues':dict(),'vnc_commands':dict()}
        
    def set_version(self,check,url):
        self.config['version']['checksum']=check
        self.config['version']['url']=url

    def add_queue(self,queue,info=''):
        self.config['queues'][queue]=info
        
    def add_vnc(self,vnc,info=''):
        self.config['vnc_commands'][vnc]=info
        
    def get_string(self):
        return pickle.dumps(self.config)
    def serialize(self,file=''):
        if (file != ''):
            pickle.dump(self.config, open( file, "wb" ) )
        else:
            print pickle.dumps(self.config)
            
    def pretty_print(self):
        print "version: checksum->"+self.config['version']['checksum']+'<--url ->'+self.config['version']['url']
        print
        for queue in self.config['queues']:
            print "queue "+queue+" info-->"+self.config['queues'][queue]+"<--"
        print
        for vnc in sorted(self.config['vnc_commands'].keys()):
            print "vnc command "+vnc+" info-->"+self.config['vnc_commands'][vnc]+"<--"
            
class rcm_protocol:
    def __init__(self,clientfunc=None,server_func=None):
        self.client_sendfunc=clientfunc
        if (server_func):
            self.server_func=server_func
        else:
            self.server_func=dict()

    def config(self,build_platform=''):
        print "get platform configuration"
        if (self.client_sendfunc):
            return self.client_sendfunc("config "+build_platform)

    def version(self,build_platform=''):
        print "get version"
        if (self.client_sendfunc):
            return self.client_sendfunc("version "+build_platform)

    def queue(self):
        print "get queues"
        if (self.client_sendfunc):
            return self.client_sendfunc("queue ")

    def loginlist(self,subnet=''):
        print "get login list "
        if (self.client_sendfunc):
            return self.client_sendfunc("loginlist "+subnet)

    def list(self,subnet=''):
        print "get display session list "
        if (self.client_sendfunc):
            return self.client_sendfunc("list "+subnet)
    def new(self,geometry='',queue='',sessionname='',subnet='',vncpassword='',vncpassword_crypted='',vnc_command=''):
        print "create new vnc display session"
        if (self.client_sendfunc):
            return self.client_sendfunc(
                "new geometry="+geometry+
                " queue="+queue+
                " sessionname=" + '\'' + sessionname + '\'' +
                " subnet="+subnet+
                " vncpassword="+vncpassword+
                " vncpassword_crypted="+'\'' + vncpassword_crypted + '\''+
                " vnc_command="+vnc_command
            )

    def kill(self,session_id=''):
        print "kill vnc display session"
        if (self.client_sendfunc):
            return self.client_sendfunc("kill "+session_id)


if __name__ == '__main__':
    print "start testing.................................."
    void_config=rcm_config()
    print "void......-->"+void_config.get_string()+"<--"
    void_config.pretty_print()

    test_config=rcm_config()
    test_config.set_version('my cheksum','my url')
    test_config.add_queue('coda1','this is queue 1')
    test_config.add_queue('coda2','this is queue 2')
    test_config.add_vnc('vnc1','this is vnc 1')
    test_config.add_vnc('vnc2','this is vnc 2')
    test_config.add_vnc('vnc3')
    print "test......-->"+test_config.get_string()+"<--"
    test_config.pretty_print()
    
    print "test pack_unpack......-->"+test_config.get_string()+"<--"
    test_config.add_vnc('vnc4','added before unpack')
    derived=rcm_config(test_config.get_string())
    derived.add_vnc('vnc5','added after unpack')
    derived.pretty_print()
    
    def prex(command='',commandnode=''):
        print "node "+commandnode+" "+ command
        
    for i in ['uno','due','tre']:
      def myfunc(command):
          prex(command,i)
      r=rcm_protocol(clientfunc=myfunc)
      r.config('mia build platform '+i)
