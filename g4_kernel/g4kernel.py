# ==================================================================
# Jupyter kernel for Geant4
#
# *** Python3 ***
# ==================================================================
from ipykernel.kernelbase import Kernel
import g4zmq

class Geant4(Kernel):
  implementation = 'Geant4'
  implementation_version = '1.0'
  language = 'g4ui'
  language_version = '1.0'
  language_info = {'name': 'shell', 'mimetype': 'text/plain'}
  banner ="""
 #####   #######     #     #     #  #######  #   #
#     #  #          # #    ##    #     #     #   #
#        #         #   #   # #   #     #     #   #
#  ####  #####    #     #  #  #  #     #     #####
#     #  #        #######  #   # #     #         #
#     #  #        #     #  #    ##     #         #
 #####   #######  #     #  #     #     #         #
"""

  # -----------------------------------------------------------------
  def do_execute(self, code, silent, store_history=True,
                 user_expressions=None, allow_stdin=False) :
    cmd = code.strip()
    if not silent:
      output = ""
      if cmd == "pwd" :
        output = g4zmq.pwd()

      elif cmd == "cwd" :
        output = g4zmq.cwd()

      elif cmd.startswith("cd") :
        arg = cmd.replace('cd', '', 1)
        output = g4zmq.cd(arg)

      elif cmd.startswith("ls") :
        arg = cmd.replace('ls', '', 1)
        output = g4zmq.ls()

      elif cmd.startswith("lc") :
        arg = cmd.replace('lc', '', 1)
        output = g4zmq.lc(arg)

      elif cmd.startswith("#") :
        arg = cmd.replace('#', '', 1)
        output = g4zmq.echo(arg)

      elif cmd.endswith("?") :
        self.do_inspect(code, 0)

      else:
        output = g4zmq.apply(cmd)

      cstr = {'name': 'stdout', 'text': output}
      self.send_response(self.iopub_socket, 'stream', cstr)

    return { 'status': 'ok',
             'execution_count': self.execution_count,
             'payload': [],
             'user_expressions': {}
           }

  # -----------------------------------------------------------------
  def do_complete(self, code, cursor_pos) :
    first_c = code[0]
    typed = code[:cursor_pos]

    if first_c == '/' :
      cmd_list = g4zmq.get_fullcommand_tree()

      return { 'status': 'ok',
               'matches': [c for c in cmd_list if c.startswith(typed)],
               'cursor_start': 0,
               'cursor_end': cursor_pos,
               'metadata': {}
              }

    elif typed.startswith("cd ") or typed.startswith("ls ") :
      cmd_list0 = g4zmq.get_fullcommand_tree()
      cmd_list1 = g4zmq.get_command_tree()
      cwd = g4zmq.cwd().strip()
      cmd_list1_r = [ c.replace(cwd, '', 1) for c in cmd_list1 ]
      cmd_list = cmd_list0 + cmd_list1_r

      return { 'status': 'ok',
               'matches': [c for c in cmd_list
                           if c.startswith(code[3:]) and c.endswith('/')],
               'cursor_start': 3,
               'cursor_end': cursor_pos,
               'metadata': {}
              }

    elif typed.startswith("lc ") or typed.startswith("help ") :
      cmd_list0 = g4zmq.get_fullcommand_tree()
      cmd_list1 = g4zmq.get_command_tree()
      cwd = g4zmq.cwd().strip()
      cmd_list1_r = [ c.replace(cwd, '', 1) for c in cmd_list1 ]
      cmd_list = cmd_list0 + cmd_list1_r

      if typed.startswith("lc ") :
        cs = 3
      elif typed.startswith("help ") :
        cs = 5

      return { 'status': 'ok',
               'matches': [c for c in cmd_list if c.startswith(code[cs:]) ],
               'cursor_start': cs,
               'cursor_end': cursor_pos,
               'metadata': {}
              }

    else :
      cmd_list = g4zmq.get_command_tree()
      cwd = g4zmq.cwd().strip()
      cmd_list_r = [ c.replace(cwd, '', 1) for c in cmd_list ]

      return { 'status': 'ok',
               'matches': [c for c in cmd_list_r if c.startswith(typed)],
               'cursor_start': 0,
               'cursor_end': cursor_pos,
               'metadata': {}
              }

  # -----------------------------------------------------------------
  def do_inspect(self, code, cursor_pos, detail_level=0) :
    print ("AAAAAAAAAAAAAAAAAAAAAaa")
    return { 'status': 'ok',
             'found': True,
             'data': {'hoge':'fuga', 'aa':'123'},
             'metadata': {}
            }

  # -----------------------------------------------------------------
  def do_shutdown(self, restart) :
    #g4zmq.exit()
    return { 'restart': False }

# ==================================================================
if __name__ == '__main__':
  from ipykernel.kernelapp import IPKernelApp
  IPKernelApp.launch_instance(kernel_class=Geant4)
  g4zmq.connect()
