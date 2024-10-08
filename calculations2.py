import pyscf
from pyscf import dft, tddft, tdscf
import numpy as np
from time import time

mol_TPB = pyscf.gto.M(
    atom = """
C   0.5303    0.2507   -0.3598
C   -0.5170   -0.3265    0.4514
C   -1.7472   -0.4543    0.0183
C   -2.7456   -1.0861    0.9337
C   -4.0820   -0.9574    0.6699
C   -5.0214   -1.5927    1.4729
C   -4.6005   -2.3518    2.5375
C   -3.2651   -2.5055    2.8375
C   -2.3484   -1.8515    2.0055
C   -2.1917    0.1271   -1.2301
C   -3.1178   -0.5585   -2.0288
C   -3.6442    0.0205   -3.1487
C   -3.3144    1.2915   -3.5719
C   -2.4038    1.9724   -2.7912
C   -1.8604    1.3974   -1.6479
C    1.7631    0.4011    0.0275
C    2.7207    1.0358   -0.9249
C    4.0798    0.9559   -0.7554
C    4.9773    1.6019   -1.5954
C    4.4573    2.3376   -2.6236
C    3.1091    2.4350   -2.8184
C    2.2266    1.7783   -1.9614
C    2.2453   -0.1570    1.2733
C    3.1985    0.5895    1.9735
C    3.7854    0.0929    3.1007
C    3.4403   -1.1525    3.5588
C    2.5095   -1.9368    2.9151
C    1.9267   -1.4059    1.7651
H    0.2894    0.5031   -1.3744
H   -0.3326   -0.6163    1.4920
H   -4.4624   -0.3380   -0.1404
H   -6.0848   -1.4752    1.2401
H   -5.3593   -2.8320    3.1416
H   -2.9655   -3.1029    3.6743
H   -1.3014   -1.9950    2.2483
H   -3.3891   -1.5891   -1.7308
H   -4.3617   -0.5722   -3.7237
H   -3.7491    1.7210   -4.4648
H   -2.1321    2.9723   -3.1080
H   -1.1814    2.0362   -1.0682
H    4.5093    0.3404    0.0411
H    6.0507    1.5065   -1.4154
H    5.1834    2.8380   -3.2732
H    2.7138    3.0169   -3.6320
H    1.1545    1.9145   -2.1716
H    3.4748    1.5941    1.6430
H    4.5259    0.6516    3.6587
H    3.8865   -1.5874    4.4591
H    2.1967   -2.9072    3.2152
H    1.2238   -2.0304    1.2059""", symmetry=True, basis='3-21g')
mol_TPB.symmetry_subgroup = 'c2'

rhf_TPB = pyscf.scf.RHF(mol_TPB)
rhf_TPB = rhf_TPB.newton()
rhf_TPB.verbose=10
rhf_TPB.kernel()


hf_TPB = tdscf.TDHF(rhf_TPB)
x0 = hf_TPB.init_guess(rhf_TPB)
hf_TPB.singlet = True
hf_TPB.max_cycle = 10000
hf_TPB.max_space = 1000
hf_TPB.conv_tol = 1e-6
hf_TPB.verbose = 5
hf_TPB.nstates = 3
hf_TPB.kernel()
hf_TPB.analyze()