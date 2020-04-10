# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 23:18:01 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Configuration-Variable
"""

from operation_path import*
from operation_record import *

from configuration_model import *

from configuration_base import *
from configuration_salt import *
from configuration_fault import *
from configuration_uplift import *
from configuration_erosion import *
from configuration_deposit import *

direction='single'

base=True
salt=True
fault=False
uplift=False
erosion=False
deposit=False

exp_name=direction
case_name=''

list_factor=[base,
             salt,
             fault,
             uplift,
             erosion,
             deposit]

list_name_function=[BaseName,
                    SaltName,
                    FaultName,
                    UpliftName,
                    ErosionName,
                    DepositName]

list_spheres_function=[Base2Spheres,
                       Salt2Spheres,
                       Fault2Spheres,
                       Uplift2Spheres,
                       Erosion2Spheres,
                       Deposit2Spheres]

#init the model
Model2Spheres()

#combine the output case name
for k in range(len(list_factor)):
    
    if list_factor[k]:
        
        #expand the case name and exp name
        exp_name,case_name=list_name_function[k](exp_name,case_name)
 
        #configuration of more factor
        list_spheres_function[k]()
        
#final case name
case_name=exp_name+case_name

folder_name='./Data/input/'+case_name

#Generate Fold
GenerateFolder(folder_name)

RecordData(open(folder_name+'/A_progress=0.00%.txt','w'))
