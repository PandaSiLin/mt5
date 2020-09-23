import socket, numpy as np
from sklearn.linear_model import LinearRegression

class socketserver:
    def __init__(self, address = '', port = 9090):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = address
        self.port = port
        self.sock.bind((self.address, self.port))
        self.cummdata = ''
        
    def recvmsg(self):
        self.sock.listen(1)
        self.conn, self.addr = self.sock.accept()
        print('connected to', self.addr)
        self.cummdata = ''

        while True:
            data = self.conn.recv(10000)
            self.cummdata+=data.decode("utf-8")
            if not data:
                break    
            self.conn.send(bytes(calcregr(self.cummdata), "utf-8"))
            return self.cummdata
            
    def __del__(self):
        self.sock.close()


def calcregr(msg = ''):
    chartdata = np.fromstring(msg, dtype=float, sep= ' ') 
    Y = np.array(chartdata).reshape(-1,1)
    X = np.array(np.arange(len(chartdata))).reshape(-1,1)
        
    lr = LinearRegression()
    lr.fit(X, Y)
    Y_pred = lr.predict(X)
    type(Y_pred)
    P = Y_pred.astype(str).item(-1) + ' ' + Y_pred.astype(str).item(0)
    print(P)
    return str(P)

serv = socketserver('127.0.0.1', 9090)

while True:  
    msg = serv.recvmsg()

bool socksend(int sock,string request) 
  {
   char req[];
   int  len=StringToCharArray(request,req)-1;
   if(len<0) return(false);
   return(SocketSend(sock,req,len)==len); 
  }

string socketreceive(int sock,int timeout)
  {
   char rsp[];
   string result="";
   uint len;
   uint timeout_check=GetTickCount()+timeout;
   do
     {
      len=SocketIsReadable(sock);
      if(len)
        {
         int rsp_len;
         rsp_len=SocketRead(sock,rsp,len,timeout);
         if(rsp_len>0) 
           {
            result+=CharArrayToString(rsp,0,rsp_len); 
           }
        }
     }
   while((GetTickCount()<timeout_check) && !IsStopped());
   return result;
  }

void drawlr(string points) 
  {
   string res[];
   StringSplit(points,' ',res);

   if(ArraySize(res)==2) 
     {
      Print(StringToDouble(res[0]));
      Print(StringToDouble(res[1]));
      datetime temp[];
      CopyTime(Symbol(),Period(),TimeCurrent(),lrlenght,temp);
      ObjectCreate(0,"regrline",OBJ_TREND,0,TimeCurrent(),NormalizeDouble(StringToDouble(res[0]),_Digits),temp[0],NormalizeDouble(StringToDouble(res[1]),_Digits)); 
     }

void OnTick() {
 socket=SocketCreate();
 if(socket!=INVALID_HANDLE) {
  if(SocketConnect(socket,"localhost",9090,1000)) {
   Print("Connected to "," localhost",":",9090);
         
   double clpr[];
   int copyed = CopyClose(_Symbol,PERIOD_CURRENT,0,lrlenght,clpr);
         
   string tosend;
   for(int i=0;i<ArraySize(clpr);i++) tosend+=(string)clpr[i]+" ";       
   string received = socksend(socket, tosend) ? socketreceive(socket, 10) : ""; 
   drawlr(recieved); }
   
  else Print("Connection ","localhost",":",9090," error ",GetLastError());
  SocketClose(socket); }
 else Print("Socket creation error ",GetLastError()); }