# ETL
Simple ETL to process data

## Run

You can use this command to automate the whole process of running the installation if you want to
```bash
sh run.sh
```
Or

You can use this command to automate the whole process of running the installation if you want to
```bash
make run
```
Or if you have docker installed on your machine you can simply run this code to run the project and it will generate files into files directory
```bash
make run-docker
```
Or

First create a python virtual environment by
```bash 
python3.12 -m venv venv
```
And then use 
```bash 
source venv/bin/activate
```
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.txt.

```bash
pip3 install -r requirements.txt
```
After the installation, simply run the code with 
```bash
python3 main.py
```
It will download the CCLE_RNAseq_rsem_genes_tpm_20180929.txt.gz and Cell_lines_annotations_20181226.txt based on a file downloaded by depmap and then it will create two csv files with rnaseq_metadata.csv and rnaseq_tpm.csv


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)