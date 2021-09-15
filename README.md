# Synthea to OMOP

## Installation

Make sure you have installed:

- PostgreSQL 13 (https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)
    - Create admin user "postgres"
    - Password "HDRUK2021"

- Install R (https://cran.r-project.org/bin/windows/base/) and Rstudio (https://www.rstudio.com/products/rstudio/download/#download)



## Instructions

### Step 1 - Obtain synthea csv output:

1. Clone the following repos:

- https://github.com/synthetichealth/synthea.git
- https://github.com/HDRUK/synthea-international.git

2. Then run:
```
cd synthea
./gradlew build
cd ../synthea-international
cp -R gb-master/* ../synthea
cd ../synthea
./run_synthea -p 5 UnitedKingdom
```
3. Clone this repo https://github.com/HDRUK/synthea-to-omop.git and copy the output csv format of synthea data to the synthea-to-omop in the **tmp/synthea/output/csv** directory (instruction given below):
```
cd ../synthea-to-omop
mkdir omop
mkdir output
mkdir -p tmp/synthea/output/csv
mkdir tmp/Vocabulary_20181119
cp ../synthea/output/csv tmp/synthea/output
```



### Step 2 - Downloads:
1. Download postgresql-42.2.23.jar to base directory of the synthea-to-omop clone using link: https://jdbc.postgresql.org/download/postgresql-42.2.23.jar
Or run wget in terminal:
```
wget https://jdbc.postgresql.org/download/postgresql-42.2.23.jar
```

2. (Optional) Also download the vocabulary file into the directory **tmp/Vocabulary_20181119**.
- Go to https://athena.ohdsi.org/search-terms/start
- Go to the download tab
- You will need to create an account
- Download the recommended vocabularies
- Move the downloaded files into **tmp/Vocabulary_20181119** (WARNING: Takes up ~4GB)



### Step 3 - Create synthea10 database:
First create a **.env** file containing the following variables:
```
USER="postgres"
PASSWORD="HDRUK2021"
HOST="localhost"
PORT=5432
NEW_DATABASE_NAME="synthea10"
```

Run the following:

```
pip install requirements.txt
python create_psql_db.py
```



### Step 4 - Run RStudio synthea_to_omop.Rmd file

####(*TODO: Add these into environment variable compatible with R instead of manually changing in script*)

1. Open the synthea_to_omop.Rmd in RStudio
2. Within the notebook, where ever `C:\\Users\\user\\Documents\\GitHub\\synthea-to-omop` occurs, you will need to change the path so it points to your synthea-to-omop directory relative to your filesystem. Here are the following variables which will change:
```
pathToDriver = "C:\\Users\\user\\Documents\\GitHub\\synthea-to-omop"

syntheaFileLoc <- "C:\\Users\\user\\Documents\\GitHub\\synthea-to-omop\\tmp\\synthea\\output\\csv"
vocabFileLoc   <- "C:\\Users\\user\\Documents\\GitHub\\synthea-to-omop\\tmp\\Vocabulary_20181119"
```
3. In the top right of the notebook, select "Restart R and Run All Chunks"

4. Run the **psql_export_query.py** script to export the OMOP formatted synthea output (results saves in the */omop* directory):
```
python psql_export_query.py
```
