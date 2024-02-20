📊 AionData
===========

AionData is a common data access layer designed for AI-driven drug discovery software. It provides a unified interface to access diverse biochemical databases.

Installation
------------

To install AionData, ensure you have Python 3.10 or newer installed on your system. You can install AionData via pip:

```bash
pip install aiondata
```

Datasets
--------

AionData provides access to the following datasets:

- **BindingDB**: A public, web-accessible database of measured binding affinities, focusing chiefly on the interactions of proteins considered to be drug-targets with small, drug-like molecules.

- **MoleculeNet**: An extensive collection of datasets curated to support and benchmark the development of machine learning models in the realm of drug discovery and chemical informatics. Covers a broad spectrum of molecular data including quantum mechanical properties, physical chemistry, biophysics, and physiological effects.
 
    - **Tox21**: Features qualitative toxicity measurements for 12,000 compounds across 12 targets, used for toxicity prediction.
    - **ESOL**: Contains water solubility data for 1,128 compounds, aiding in solubility prediction models.
    - **FreeSolv**: Provides experimental and calculated hydration free energy for small molecules, crucial for understanding solvation.
    - **Lipophilicity**: Includes experimental measurements of octanol/water distribution coefficients (logD) for 4,200 compounds.
    - **QM7**: A dataset of 7,165 molecules with quantum mechanical properties computed using density functional theory (DFT).
    - **QM8**: Features electronic spectra and excited state energies of over 20,000 small molecules computed with TD-DFT.
    - **QM9**: Offers geometric, energetic, electronic, and thermodynamic properties of ~134k molecules computed with DFT.
    - **MUV**: Datasets designed for the validation of virtual screening techniques, with about 93,000 compounds.
    - **HIV**: Contains data on the ability of compounds to inhibit HIV replication, for binary classification tasks.
    - **BACE**: Includes quantitative binding results for inhibitors of human beta-secretase 1, with both classification and regression tasks.
    - **BBBP**: Features compounds with information on permeability properties across the Blood-Brain Barrier.
    - **SIDER**: Contains information on marketed medicines and their recorded adverse drug reactions, for side effects prediction.
    - **ClinTox**: Compares drugs approved by the FDA and those that failed clinical trials for toxicity reasons, for binary classification and toxicity prediction.

License
-------

AionData is licensed under the Apache License. See the LICENSE file for more details.