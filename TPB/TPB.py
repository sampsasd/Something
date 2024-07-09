import numpy as np
import matplotlib.pyplot as plt
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import AllChem
from scipy.constants import physical_constants


#C28H22

TPB = Chem.MolFromSmiles('C(C=C(C1=CC=CC=C1)C1=CC=CC=C1)=C(C1=CC=CC=C1)C1=CC=CC=C1')
TPB.SetProp('_Name', 'Tetraphenyl Butadiene')

img = Draw.MolToImage(TPB, (1000, 800))
#img.save("./TPB/TPB.png")
#img.show()

AllChem.Compute2DCoords(TPB)

TPB2 = Chem.AddHs(TPB)
params = AllChem.ETKDGv3()
params.randomSeed = 0xf00d
AllChem.EmbedMolecule(TPB2, params)
print(Chem.MolToMolBlock(TPB2))
