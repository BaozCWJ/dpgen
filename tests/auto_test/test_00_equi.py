import numpy as np
import unittest
import json,re,os
from .input_data import *
from .context import setUpModule
from dpgen.auto_test import gen_00_equi,cmpt_00_equi


class TestEqui(unittest.TestCase):

    def test_gen_equi(self):
        conf_dir="confs/Cu/std-fcc"
        global_task_name='00.equi'
        task_path=os.path.abspath(re.sub('confs', global_task_name, conf_dir))
        with open (param_file, 'r') as fp :
            jdata = json.load (fp)

        gen_00_equi.make_vasp(jdata,conf_dir)
        kspacing = jdata['vasp_params']['kspacing']
        vasp_str='vasp-k%.2f' % kspacing
        vasp_path=os.path.join(task_path,vasp_str)
        vasp_check=[os.path.join(vasp_path,ii) for ii in vasp_input]
        for ii in vasp_check:
            if self.assertTrue(os.path.isfile(ii)):
                os.remove(ii)

        gen_00_equi.make_lammps(jdata,conf_dir,"deepmd")
        dp_path = os.path.join(task_path,'deepmd')
        dp_check=[os.path.join(dp_path,ii) for ii in dp_input]
        for ii in dp_check:
            if self.assertTrue(os.path.isfile(ii)):
                os.remove(ii)

    def test_cmpt_equi(self):
        conf_dir="confs/Cu/std-fcc"
        with open (param_file, 'r') as vasp_fp :
            jdata = json.load (vasp_fp)
        n,e,v,s=cmpt_00_equi.comput_vasp_nev(jdata, conf_dir,False)
        sn=str(n)
        se=str('%2.4f'%e)
        sv=str('%2.1f'%v)
        vasp_ref = ['1' ,'-3.7287','12.0']
        self.assertEquals([sn,se,sv],vasp_ref)
        n,e,v,s=cmpt_00_equi.comput_lmp_nev(conf_dir, "deepmd",False)
        sn=str(n)
        se=str('%2.4f'%e)
        sv=str('%2.1f'%v)
        dp_ref = ['1','-3.7271','12.0']
        self.assertEquals([sn,se,sv],dp_ref)




if __name__== '__main__':
    unittest.main()