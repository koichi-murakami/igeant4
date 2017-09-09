"""
Copyright 2017 Koichi Murakami

Distributed under the OSI-approved BSD License (the "License");
see accompanying file LICENSE for details.

This software is distributed WITHOUT ANY WARRANTY; without even the
implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the License for more information.
"""
# ==================================================================
# Jupyter kernel for Geant4
#
# *** Python3 ***
# ==================================================================
from ipykernel.kernelbase import Kernel
import g4zmq
import subprocess

class Geant4(Kernel):
  implementation = 'Geant4'
  implementation_version = '1.0'
  language = 'geant4'
  language_version = '1.0'
  language_info = {'name': 'shell', 'mimetype': 'application/x-shell-session'}
  banner ="""
 #####   #######     #     #     #  #######  #   #
#     #  #          # #    ##    #     #     #   #
#        #         #   #   # #   #     #     #   #
#  ####  #####    #     #  #  #  #     #     #####
#     #  #        #######  #   # #     #         #
#     #  #        #     #  #    ##     #         #
 #####   #######  #     #  #     #     #         #

Geant4 Jupyter kernel 1.0 -- Jupyter frontend for Geant4 UI
Geant4 UI commands  -> Execute UI commands
pwd/cwd/cd/ls/lc    -> move/show UI command tree
?command            -> Show a current value if possible
#message            -> Echo message
help command        -> Details about commands
command?            -> Same as help
%shell              -> Shell command
%connect            -> Connet to G4ZMQ server
"""
  __connected = False
  __magic = [ "%shell", "%connect"]

  # -----------------------------------------------------------------
  def do_execute(self, code, silent, store_history=True,
                 user_expressions=None, allow_stdin=False) :
    cmd = code.strip()
    output = ""

    if not silent:
      if cmd.startswith("%shell") :
        arg = cmd.replace('%shell', '', 1)
        try :
          subprocess.Popen(arg.strip())
        except :
          print ("@@ shell command error")

      elif cmd.startswith("%connect") :
        try :
          g4zmq.connect()
          self.__connected = True
        except :
          print ("@@ g4zmq connection error")

      elif not self.__connected :
        print ("@@ invalid input")

      elif cmd == "pwd" :
        output = g4zmq.pwd()

      elif cmd == "cwd" :
        output = g4zmq.cwd()

      elif cmd.startswith("cd") :
        arg = cmd.replace('cd', '', 1)
        output = g4zmq.cd(arg)

      elif cmd.startswith("ls") :
        arg = cmd.replace('ls', '', 1)
        output = g4zmq.ls(arg)

      elif cmd.startswith("lc") :
        arg = cmd.replace('lc', '', 1)
        output = g4zmq.lc(arg)

      elif cmd.startswith("#") :
        output = g4zmq.echo(cmd[1:])

      elif cmd.endswith("?") :
        output = g4zmq.help(cmd[:-1])

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

    if not self.__connected :
      return { 'status': 'ok',
                'matches': [c for c in self.__magic if c.startswith(typed)],
                'cursor_start' : 0,
                'cursor_end' : cursor_pos,
                'metadata':{}
              }

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
  def do_shutdown(self, restart) :
    if self.__connected :
      g4zmq.exit()
    return { 'restart': False }
