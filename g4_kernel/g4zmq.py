# ==================================================================
# ZeroMQ interface with Geant4
#
# *** Python3 ***
# ==================================================================
import zmq

# global vars
charset = 'utf-8'
context = zmq.Context(1)
socket = context.socket(zmq.REQ)

# ===============================================================
def connect(endpoint="tcp://127.0.0.1:5555") :
  socket.setsockopt(zmq.LINGER, 0)
  socket.connect(endpoint)
  ping()

def ping() :
  socket.send(b"@@ping")
  poller = zmq.Poller()
  poller.register(socket, zmq.POLLIN)
  if poller.poll(1*1000) :
    output = socket.recv()
    print ("@@ G4ZMQ server connected.\n")
  else :
    raise ConnectionError("*** connection timeout")

def get_command_tree() :
  socket.send(b"@@get_command_tree")
  output = socket.recv()
  cmdlist_str_buf = output.decode(charset)
  cmdlist_str = cmdlist_str_buf.strip()
  cmdlist = cmdlist_str.split(' ')
  return cmdlist

def get_fullcommand_tree() :
  socket.send(b"@@get_fullcommand_tree")
  output = socket.recv()
  cmdlist_str_buf = output.decode(charset)
  cmdlist_str = cmdlist_str_buf.strip()
  cmdlist = cmdlist_str.split(' ')
  return cmdlist

def apply(command) :
  cmd_str= command.encode(charset)
  socket.send(cmd_str)
  output = socket.recv()
  return output.decode(charset)

def execute(command) :
  return apply(command)

def pwd() :
  socket.send(b"pwd")
  output = socket.recv()
  return output.decode(charset).strip()

def cwd() :
  socket.send(b"cwd")
  output = socket.recv()
  return output.decode(charset).strip()

def cd(dir="") :
  cmd = "cd " + dir
  socket.send(cmd.encode(charset))
  output = socket.recv()
  return output.decode(charset).strip()

def lc(target="") :
  cmd = "lc " + target
  socket.send(cmd.encode(charset))
  output = socket.recv()
  return output.decode(charset).strip()

def ls(target="") :
  cmd = "ls " + target
  socket.send(cmd.encode(charset))
  output = socket.recv()
  return output.decode(charset).strip()

def help(target="") :
  if ( target == "" ) :
    raise SyntaxWarning("*** no command specified.")
  else :
    cmd = "help " + target
    socket.send(cmd.encode(charset))
    output = socket.recv()
    return output.decode(charset)

def beamOn(nevent) :
  cmd = "/run/beamOn " + str(nevent)
  return apply(cmd)

def getvalue(target="") :
  cmd = "?" + target
  socket.send(cmd.encode(charset))
  output = socket.recv()
  return output.decode(charset).strip()

def echo(message="") :
  return message.strip()

def exit() :
  socket.send(b"exit")
  output = socket.recv()
  print( output.decode(charset))

# ===============================================================
if __name__ == '__main__' :
  pass
