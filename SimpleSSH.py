from tkinter import filedialog
import time
from paramiko import *
from tkinter import *

def ssh():
   global f1, e1, e2
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
   # `remote_client` should now be able to issue commands to the REMOTE box
   # remote_client.exec_command('pwd')
   try:
      import interactive
   except ImportError:
      from . import interactive

   channel = proxy_client.get_transport().open_session()
   channel.get_pty()
   channel.invoke_shell()
   interactive.interactive_shell(channel)
   proxy_client.close()

def browsefunc():
   filename = filedialog.askopenfilename()
   global f1
   f1.config(state=NORMAL)
   f1.delete(0, END)
   f1.insert(END,filename)
   f1.config(state=DISABLED)

master = Tk()
master.title('Simple SSH Client by SpanishMafia')
master.minsize(100,110)
master.geometry("470x100")

Label(master, text="Host IP or URL").grid(row=0)
Label(master, text="Host username").grid(row=1)
Label(master, text="Host Key").grid(row=2)

e1 = Entry(master, width=30)
e2 = Entry(master, width=30)
f1 = Entry(master, width=30)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
f1.grid(row=2, column=2)

Button(master, text='Browse', command=browsefunc).grid(row=2, column=1, sticky=W, pady=4)
Button(master, text='Quit', command=master.quit).grid(row=3, column=0, sticky=W, pady=4)
Button(master, text='Run', command=ssh).grid(row=3, column=1, sticky=W, pady=4)



mainloop( )