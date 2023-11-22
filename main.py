import pandas as pd
import numpy as np
import requests

# Function to download files from the DepMap Portal API
def download_file_from_depmap(file_name):
    depmap_url = f"https://depmap.org/portal/api/download/files"
    response = requests.get(depmap_url)
    if response.status_code == 200:
        data = response.content
        open("response.csv", "wb").write(data)
        df = pd.read_csv("./response.csv")
        # df = df.convert_dtypes()
        url = df.loc[df['filename'] == file_name].values.tolist()[0][3]
        response = requests.get(url)
        if response.status_code == 200:
            data = response.content
            open(f"{file_name}", "wb").write(data)
            return pd.read_csv(f"{file_name}", sep="\t")
        else:
            raise ValueError(f"Failed to download file {file_name} from DepMap Portal API.")
    else:
        raise ValueError(f"Failed to download file {file_name} from DepMap Portal API.")


rnaseq_tpm  = download_file_from_depmap("CCLE_RNAseq_rsem_genes_tpm_20180929.txt.gz")
rnaseq_metadata = download_file_from_depmap("Cell_lines_annotations_20181226.txt")

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
rnaseq_metadata.to_csv("rnaseq_metadata.csv", index=False)
rnaseq_tpm.to_csv("rnaseq_tpm.csv", index=False)

