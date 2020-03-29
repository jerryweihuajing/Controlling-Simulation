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
fault=True
uplift=True
erosion=True
deposit=True

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
for this_factor in list_factor:
    
    if this_factor:
        
        #expand the case name and exp name
        exp_name,case_name=list_name_function[list_factor.index(this_factor)](exp_name,case_name)
 
        #configuration of more factor
        list_spheres_function[list_factor.index(this_factor)]()
        
#final case name
case_name=exp_name+case_name

folder_name='./input//'+case_name

#Generate Fold
O_P.GenerateFold(folder_name)

out_file=open(folder_name+'/A_progress=0.00%.txt','w')

RecordData(out_file,spheres)
