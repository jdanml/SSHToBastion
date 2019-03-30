from tkinter import filedialog
import time
from paramiko import *
from tkinter import *

def ssh():
   global f1, f2, e1, e2, e3, e4
   # Set up the proxy (forwarding server) credentials
   proxy_port = 22
   # Instantiate a client and connect to the proxy server
   proxy_client = SSHClient()
   proxy_client.set_missing_host_key_policy(AutoAddPolicy())
   proxy_client.connect(
      e1.get(),
      port=proxy_port,
      username=e2.get(),
      pkey=RSAKey.from_private_key_file(f1.get())
)
   # Get the client's transport and open a `direct-tcpip` channel passing
   # the destination hostname:port and the local hostname:port
   transport = proxy_client.get_transport()
   dest_addr = (e3.get(), 22)
   local_addr = ('127.0.0.1', 12345)
   channel = transport.open_channel("direct-tcpip", dest_addr, local_addr)

   # Create a NEW client and pass this channel to it as the `sock` (along with
   # whatever credentials you need to auth into your REMOTE box
   remote_client = SSHClient()
   remote_client.set_missing_host_key_policy(AutoAddPolicy())
   pemkey_path = RSAKey.from_private_key_file(f2.get())
   remote_client.connect('127.0.0.1', port=12345, username=e4.get(), pkey = pemkey_path, sock=channel)

   # `remote_client` should now be able to issue commands to the REMOTE box
   # remote_client.exec_command('pwd')
   try:
      import interactive
   except ImportError:
      from . import interactive

   channel = remote_client.get_transport().open_session()
   channel.get_pty()
   channel.invoke_shell()
   interactive.interactive_shell(channel)
   remote_client.close()

def browsefunc():
   filename = filedialog.askopenfilename()
   global f1
   f1.config(state=NORMAL)
   f1.delete(0, END)
   f1.insert(END,filename)
   f1.config(state=DISABLED)

def browsefunc1():
   filename = filedialog.askopenfilename()
   global f2
   f2.config(state=NORMAL)
   f2.delete(0, END)
   f2.insert(END,filename)
   f2.config(state=DISABLED)

master = Tk()
master.title('SSH To Bastion by SpanishMafia')
master.minsize(100,100)
master.geometry("500x200")

Label(master, text="Bastion IP or URL").grid(row=0)
Label(master, text="Bastion username").grid(row=1)
Label(master, text="Bastion Key").grid(row=2)

Label(master, text="Remote Host IP").grid(row=4)
Label(master, text="Remote Host username").grid(row=5)
Label(master, text="Remote Host Key").grid(row=6)

e1 = Entry(master, width=30)
e2 = Entry(master, width=30)
e3 = Entry(master, width=30)
e4 = Entry(master, width=30)

f1 = Entry(master, width=30)
f2 = Entry(master, width=30)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=4, column=1)
e4.grid(row=5, column=1)
f1.grid(row=2, column=2)
f2.grid(row=6, column=2)

Button(master, text='Browse', command=browsefunc).grid(row=2, column=1, sticky=W, pady=4)
Button(master, text='Browse', command=browsefunc1).grid(row=6, column=1, sticky=W, pady=4)
Button(master, text='Quit', command=master.quit).grid(row=8, column=0, sticky=W, pady=4)
Button(master, text='Run', command=ssh).grid(row=8, column=1, sticky=W, pady=4)



mainloop( )