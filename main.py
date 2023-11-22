import pandas as pd
import numpy as np

rnaseq_tpm  = pd.read_csv("./CCLE_RNAseq_rsem_genes_tpm_20180929.txt", sep='\t')
rnaseq_metadata = pd.read_csv("./Cell_lines_annotations_20181226.txt", sep='\t')

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

print(rnaseq_tpm.shape)

# common_cell_lines = rnaseq_metadata[rnaseq_metadata['CCLE_ID'].isin(rnaseq_tpm['CCLE_ID'])]


common_cell_lines = rnaseq_metadata['CCLE_ID'].isin(rnaseq_tpm.columns)
rnaseq_metadata = rnaseq_metadata[common_cell_lines]

# Check and reorder metadata columns
if not rnaseq_metadata['CCLE_ID'].equals(rnaseq_tpm.columns[1:]):
    rnaseq_metadata = rnaseq_metadata.set_index(rnaseq_metadata['CCLE_ID'])
    rnaseq_metadata = rnaseq_metadata.reindex(rnaseq_tpm.columns[1:]).reset_index().drop(columns=['index'])


# Save transformed data to CSV files
# rnaseq_metadata.to_csv("rnaseq_metadata.csv", index=False)
# rnaseq_tpm.to_csv("rnaseq_tpm.csv", index=False)

