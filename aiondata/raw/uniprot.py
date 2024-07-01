import gzip
import urllib.request
from io import BytesIO
from typing import Iterable, Dict

from ..datasets import GeneratedDataset


class UniProt(GeneratedDataset):
    """
    A class to parse and process protein data from the UniProtKB Swiss-Prot database.

    UniProtKB Swiss-Prot is a manually annotated and reviewed protein sequence database
    which is part of the Universal Protein Resource (UniProt). It provides a high level
    of annotation (such as the description of protein function, domains structure, post-translational
    modifications, and variants), and is enriched with automatic annotation pipelines.

    This class provides methods to directly download and parse the gzipped UniProtKB data file
    from the UniProt server, and convert the entries into human-readable dictionaries
    suitable for further data analysis or integration into bioinformatics workflows.

    Attributes:
        SOURCE (str): The URL to the gzipped UniProtKB Swiss-Prot data file. Default is set to the
                      current release's complete Swiss-Prot data.

    Methods:
        to_generator(): Streams the UniProt data, parsing it into human-readable dictionaries
                        representing each protein record.
    """

    SOURCE = "https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.dat.gz"
    COLLECTION = "uniprot"

    def __init__(self, source: str = SOURCE):
        """
        Initializes the UniProt class with a source URL.

        Args:
            source (str, Optional): The URL to the gzipped UniProtKB data file.
        """
        self.source = source
        self.uni_prot_key_descriptions = {
            "ID": "Entry Identifier",
            "AC": "Accession Numbers",
            "DT": "Date",
            "DE": "Protein Description",
            "GN": "Gene Name",
            "OS": "Organism Species",
            "OC": "Organism Classification",
            "OX": "Organism Taxonomy Cross-reference",
            "OH": "Organism Host",
            "RN": "Reference Number",
            "RP": "Reference Position",
            "RX": "Reference Cross-reference",
            "RA": "Reference Author(s)",
            "RT": "Reference Title",
            "RL": "Reference Location",
            "CC": "Comments",
            "DR": "Database Cross-references",
            "PE": "Protein Existence",
            "KW": "Keywords",
            "FT": "Feature Table",
            "SQ": "Sequence Data",
            "RC": "Reference Comment",
            "RG": "Reference Group",
            "OG": "Organelle",
        }

    def to_generator(self) -> Iterable[Dict]:
        """
        Streams and parses the gzipped UniProtKB data file, yielding each entry as a dictionary
        with human-readable keys.

        This method downloads the data file from the specified `source`, decompresses it,
        and reads it line by line. Each line is parsed into key-value pairs with keys converted
        from short codes to descriptive names using an internal dictionary. Each complete entry
        is yielded as a dictionary.

        Yields:
            dict: A dictionary representing a single UniProtKB entry with descriptive keys.
        """
        with urllib.request.urlopen(self.source) as response:
            with gzip.open(BytesIO(response.read()), "rt") as file:
                entry = {}
                sequence_mode = False
                sequence_lines = []
                for line in file:
                    if line.startswith("//"):  # End of an entry
                        if (
                            sequence_lines
                        ):  # Ensure the sequence is concatenated if it exists
                            entry["SQ"] = "".join(sequence_lines).replace(" ", "")
                        human_readable_entry = {
                            self.uni_prot_key_descriptions.get(key, key): value
                            for key, value in entry.items()
                        }
                        yield human_readable_entry
                        entry = {}
                        sequence_mode = False
                        sequence_lines = []
                    elif line.startswith("SQ"):
                        sequence_mode = True
                    elif sequence_mode:
                        if line.strip():
                            sequence_lines.append(line.strip())
                    else:
                        key, _, value = line.partition("   ")
                        key = key.strip()
                        if key:
                            if key in entry:
                                entry[key] += f" {value.strip()}"
                            else:
                                entry[key] = value.strip()
