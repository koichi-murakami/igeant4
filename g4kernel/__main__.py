"""
Copyright 2017 Koichi Murakami

Distributed under the OSI-approved BSD License (the "License");
see accompanying file LICENSE for details.

This software is distributed WITHOUT ANY WARRANTY; without even the
implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the License for more information.
"""

if __name__ == '__main__' :
  from ipykernel.kernelapp import IPKernelApp
  from .g4kernel import Geant4
  IPKernelApp.launch_instance(kernel_class=Geant4)
