# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 23:18:01 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Configuration-Variable
"""

from operation_path import *

from configuration_base import *
from configuration_salt import *
from configuration_fault import *
from configuration_uplift import *
from configuration_erosion import *
from configuration_deposit import *

from configuration_model import *
from operation_record import *

direction='single'

erosion=False
deposit=False
uplift=False
fault=False
base=True
salt=False

exp_name=direction
case_name=''

list_factor=[base,
             salt,
             fault,
             uplift,
             erosion,
             deposit]

list_function=[BaseName,
               SaltName,
               FaultName,
               UpliftName,
               ErosionName,
               DepositName]

for this_factor in list_factor:
    
    if this_factor:
        
        exp_name,case_name=list_function[list_factor.index(this_factor)](exp_name,case_name)
        
case_name=exp_name+case_name

#os.system("python configuration_simulation.py")

folder_name='./input//'+case_name

#Generate Fold
GenerateFold(folder_name)

out_file=open(folder_name+'/A_progress=0.00%.txt','w')

RecordData(out_file,spheres)

Model2Spheres()
Base2Spheres()