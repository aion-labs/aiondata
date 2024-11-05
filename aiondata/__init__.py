from .raw.bindingdb import BindingDB
from .raw.protein_structure import (
    FoldswitchProteinsTableS1A,
    FoldswitchProteinsTableS1B,
    FoldswitchProteinsTableS1C,
    CodNas91,
    PDBHandler,
)
from .raw.moleculenet import (
    Tox21,
    ToxCast,
    ESOL,
    FreeSolv,
    Lipophilicity,
    QM7,
    QM8,
    QM9,
    MUV,
    HIV,
    BACE,
    BBBP,
    SIDER,
    ClinTox,
)

from .raw.uniprot import UniProt

from .raw.weizmann_ccca import Weizmann3CA

from .raw.zinc import ZINC

from .processed.bindingaffinity import BindingAffinity
