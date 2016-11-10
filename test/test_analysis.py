import unittest
import utils
import os
import sys
import re
import shutil
import subprocess

TOPDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(TOPDIR, 'lib'))
import cryptosite.analysis

def touch(fname):
    with open(fname, 'w') as fh:
        pass

class Tests(unittest.TestCase):

    def test_get_energy(self):
        """Test get_energy() function"""
        inputs = os.path.join(TOPDIR, 'test', 'input')
        with utils.temporary_directory() as tmpdir:
            subdir = os.path.join(tmpdir, 'XXX.pdb_14')
            os.mkdir(subdir)
            touch(os.path.join(subdir, 'pm.pdb.B10010001.pdb'))
            touch(os.path.join(subdir, 'pm.pdb.B10020001.pdb'))
            touch(os.path.join(subdir, 'pm.pdb.B99990001.pdb'))
            shutil.copy(os.path.join(inputs, 'pm.pdb.D00000001'), subdir)

            e = cryptosite.analysis.get_energy(tmpdir)
            with open(os.path.join(subdir, 'energy.dat')) as fh:
                e = fh.readlines()
            self.assertEqual(e,
                    ['   1000      13478.55371   0.0280   0.0836       '
                     '3374.72437        499.52283\n',
                     '   1000      13580.25098   0.0279   0.0794       '
                     '3332.75293        493.31027\n'])

    def test_get_qioft(self):
        """Test get_qioft() function"""
        inputs = os.path.join(TOPDIR, 'test', 'input')
        with utils.temporary_directory() as tmpdir:
            subdir = os.path.join(tmpdir, 'XXX.pdb_14')
            os.mkdir(subdir)
            for f in ('list', 'pm.pdb.B10010001.pdb', 'pm_XXX.pdb'):
                shutil.copy(os.path.join(inputs, f), subdir)

            cryptosite.analysis.get_qioft(tmpdir)
            with open(os.path.join(subdir, 'qioft_pm_XXX.pdb_11sc.dat')) as fh:
                e = fh.readlines()
            self.assertEqual(e, ['0.2205 0.3422 0.5290 0.3791 0.2468 '
                         '0.4816 0.3841 0.5149 0.4896 0.0971 0.3187 0.0189 \n'])

if __name__ == '__main__':
    unittest.main()