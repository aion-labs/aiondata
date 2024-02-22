import os
from pathlib import Path
import polars as pl

from .datasets import CsvDataset,ExcelDataset

class FoldswitchProteins:
    """
    Papaer:AlphaFold2 fails to predict protein fold switching
    https://doi.org/10.1002/pro.4353
    """

    class Table_S1A(ExcelDataset):
        '''(A) List of pairs (PDBIDs), lengths and the sequence of the fold-switching region.
        (For those pairs not having the second fold solved in PDB, only the first PDB is reported).
        '''
        SOURCE = "https://raw.githubusercontent.com/tomshani/aiondata/tom-branch/data/pro4353-sup-0002-tables1%20/Table_S1A_final.xlsx"

    class Table_S1B(ExcelDataset):
        '''(B) RMSD, TM-scores for the whole protein and only fold-switching fragment,
        as well as sequence identities between the fold-switching pairs.
        wTM-score/wRMSD indicate TM-scores/RMSDs considering whole protein chains.
        fsTM-score/fsRMSD indicate TM-scores/RMSDs considering fold-switching regions only.
        '''
        SOURCE = "https://raw.githubusercontent.com/tomshani/aiondata/tom-branch/data/pro4353-sup-0002-tables1%20/Table_S1B_final.xlsx"

    class Table_S1C(ExcelDataset):
        '''(C) List of fold-switching protein pairs (PDBID and chain) used for the analysis,
        first column corresponds to Fold1 and second to Fold2, followed by TM-scores of the predictions.
        Tables attached separately.
        '''
        SOURCE = "https://raw.githubusercontent.com/tomshani/aiondata/tom-branch/data/pro4353-sup-0002-tables1%20/Table_S1C_final.xlsx"


class CodNas91(CsvDataset):
    """
    Paper: Impact of protein conformational diversity on AlphaFold predictions
    https://doi.org/10.1093/bioinformatics/btac202
    We selected 91 proteins (Supplementary Table S1) with different degrees of conformational diversity expressed as the range of pairwise global Cα-RMSD between their conformers in the PDB (Fig. 1).
    All the pairs of conformers for each protein are apo–holo pairs selected from the CoDNaS database (Monzon et al., 2016) and bibliography. Manual curation for each protein confirmed that structural deformations were associated with a given biological process based on experimental evidence.
    This step is essential to ensure that conformational diversity is not associated with artifacts, misalignments, missing regions, or the presence of flexible ends. When more than two conformers were known, we selected the apo–holo pair showing the maximum Cα-RMSD (maxRMSD).
    Other considerations were absence of disorder, PDB resolution, absence of mutations and sequence differences. We previously observed that when conformational diversity is derived from experimentally based conformers, different ranges of RMSD are obtained between them depending on the structure determination method (Monzon et al., 2017a).
    Here we considered a continuum of protein flexibility measured as the RMSD between apo and holo forms as shown in Figure 1.
    """
    SOURCE= "https://raw.githubusercontent.com/tomshani/aiondata/tom-branch/data/Supplementary_Table_1_91_apo_holo_pairs.csv" 


class Tox21(CsvDataset):
    """Tox21 is a dataset consisting of qualitative toxicity measurements for 12,000 compounds on 12 different targets."""

    SOURCE = "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/tox21.csv.gz"


class ESOL(CsvDataset):
    """
    ESOL is a dataset consisting of water solubility data for 1,128 compounds. The dataset is widely used for developing models that predict solubility directly from chemical structures.
    """

    SOURCE = (
        "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/delaney-processed.csv"
    )


class FreeSolv(CsvDataset):
    """
    FreeSolv provides experimental and calculated hydration free energy of small molecules in water. It includes 642 molecules and is used for benchmarking hydration free energy predictions.
    """

    SOURCE = "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/SAMPL.csv"


class Lipophilicity(CsvDataset):
    """
    Lipophilicity contains experimental measurements of octanol/water distribution coefficient (logD at pH 7.4) for 4,200 compounds. It is useful for modeling compound partitioning between lipids and water.
    """

    SOURCE = (
        "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/Lipophilicity.csv"
    )


class QM7(CsvDataset):
    """
    QM7 is a dataset of 7,165 molecules, which provides quantum mechanical properties that are computed using density functional theory (DFT). It's primarily used for regression tasks on molecular properties.
    """

    SOURCE = "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/qm7.csv"


class QM8(CsvDataset):
    """
    QM8 includes electronic spectra and excited state energy of small molecules computed using time-dependent DFT (TD-DFT). It consists of over 20,000 molecules and is used for regression of electronic properties.
    """

    SOURCE = "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/qm8.csv"


class QM9(CsvDataset):
    """
    QM9 dataset contains geometric, energetic, electronic, and thermodynamic properties of roughly 134,000 molecules with up to 9 heavy atoms, computed using DFT.
    """

    SOURCE = "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/qm9.csv"


class MUV(CsvDataset):
    """
    MUV (Maximum Unbiased Validation) datasets consist of 17 assays designed for validation of virtual screening techniques. It includes about 93,000 compounds across various assays.
    """

    SOURCE = "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/muv.csv.gz"


class HIV(CsvDataset):
    """
    HIV dataset contains data on the ability of compounds to inhibit HIV replication. It is used for binary classification tasks, with over 40,000 compounds.
    """

    SOURCE = "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/HIV.csv"


class BACE(CsvDataset):
    """
    BACE dataset includes quantitative binding results for a set of inhibitors of human beta-secretase 1 (BACE-1). It's used for both classification and regression tasks on over 1,500 compounds.
    """

    SOURCE = "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/bace.csv"


class BBBP(CsvDataset):
    """
    BBBP (Blood-Brain Barrier Penetration) dataset. It contains compounds with features regarding permeability properties across the Blood-Brain Barrier, used for binary classification tasks.
    """

    SOURCE = "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/BBBP.csv"


class SIDER(CsvDataset):
    """
    SIDER contains information on marketed medicines and their recorded adverse drug reactions (ADR), used for multi-task classification of side effects.
    """

    SOURCE = "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/sider.csv.gz"


class ClinTox(CsvDataset):
    """
    ClinTox compares drugs approved by the FDA and those that have failed clinical trials for toxicity reasons. It's used for binary classification and toxicity prediction.
    """

    SOURCE = "https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/clintox.csv.gz"
