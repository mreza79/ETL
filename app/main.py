import pandas as pd
import numpy as np
import requests
from pandas import DataFrame
from pathlib import Path

# Function to download files from the DepMap Portal API
def download_file_from_depmap(filepath: Path, file_name: str) -> DataFrame:
    depmap_url = "https://depmap.org/portal/api/download/files"
    response = requests.get(depmap_url)
    if response.status_code == 200:
        data = response.content
        with open(filepath / "response.csv", "wb") as file:
            file.write(data)
        df = pd.read_csv(filepath / "response.csv")
        # df = df.convert_dtypes()
        url = df.loc[df['filename'] == file_name].values[0][3]
        response = requests.get(url)
        if response.status_code == 200:
            data = response.content
            with open(filepath / file_name, "wb") as file:
                file.write(data)
            return pd.read_csv(filepath / file_name, sep="\t")
        else:
            raise ValueError(f"Failed to download file {file_name} from DepMap Portal API.")
    else:
        raise ValueError(f"Failed to download file {file_name} from DepMap Portal API.")

def main(filepath: Path):
    rnaseq_tpm  = download_file_from_depmap(filepath, "CCLE_RNAseq_rsem_genes_tpm_20180929.txt.gz")
    rnaseq_metadata = download_file_from_depmap(filepath, "Cell_lines_annotations_20181226.txt")

    MISSING_VALUES_NUMBER = 700

    # Check for column-wise missing values in rnaseq_metadata
    missing_values = rnaseq_metadata.isnull().sum()
    # Drop columns with more than 700 missing values
    columns_to_drop = missing_values[missing_values > MISSING_VALUES_NUMBER].index
    rnaseq_metadata = rnaseq_metadata.drop(columns=columns_to_drop)

    # Drop column named transcript_ids
    rnaseq_tpm = rnaseq_tpm.drop(columns=['transcript_ids'])

    # apply Log2(x+0.001) where x is numeric
    rnaseq_tpm = rnaseq_tpm.apply(lambda x: np.log2(x + 0.001) if np.issubdtype(x.dtype, np.number) else x)

    # Subset rnaseq_metadata based on common cell line names between rnaseq_metadata and rnaseq_tpm
    common_cell_lines = rnaseq_metadata['CCLE_ID'].isin(rnaseq_tpm.columns)
    rnaseq_metadata = rnaseq_metadata[common_cell_lines]

    # Check and reorder metadata columns
    if not rnaseq_metadata['CCLE_ID'].equals(rnaseq_tpm.columns[1:]):
        rnaseq_metadata = rnaseq_metadata.set_index(rnaseq_metadata['CCLE_ID'])
        rnaseq_metadata = rnaseq_metadata.reindex(rnaseq_tpm.columns[1:]).reset_index().drop(columns=['index'])


    # Save transformed data to CSV files
    rnaseq_metadata.to_csv(filepath / "rnaseq_metadata.csv", index=False)
    rnaseq_tpm.to_csv(filepath / "rnaseq_tpm.csv", index=False)

if __name__ == "__main__":
    filepath = Path("files")
    filepath.mkdir(parents=True, exist_ok=True)

    main(filepath)

