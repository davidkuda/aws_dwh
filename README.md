# AWS Cloud Data Warehouse with Redshift

### Table of Contents
- Introduction to this project
- Database schema design and ETL process
- Files in repository
- How to run the python scripts

### Introduction: Sparkify Audio Streaming, User Data and AWS.

Sparkify is a (fictional) startup that offers music streaming services. They accumulate 
data but do not yet leverage them. In this project I build an
ETL pipeline that loads data from S3 to Redshift. A walk through a concept in [a jupyter notebook.](./notebooks/Sample_Loads.ipynb) 

In order to perform the ETL process, I connect to the S3 bucket using Python and boto3. I then copy all json files that are stored in that bucket to AWS Redshift.
The data first lands to a staging table. From there the ETL processes transform the data by using SQL to SQL design in Redshift. 

With the data model and the Sparkify will have the ability to perform several analyses.
For instance, Sparkify will gain the ability to understand which songs are being played
the most, which OS and browser their users use or how the distribution between free
and paid users is.

Now that we have learned more about Sparkify and the purpose of this project, 
I will present more details about the data in the next chapter.

### Database Schema Design and ETL Process

The data is  stored as json files in AWS S3. The buckets are:

- Song data: s3://udacity-dend/song_data
- Log data: s3://udacity-dend/log_data

The first ETL step is to copy all these files into Redshift. Here is the data model for the two staging tables:

![staging tables](tbd)

The next steps of the ETL is to distribute these columns into their respective dimensions tables. 

__song data:__
- a
- b

__log data:__
- c
- d

#### song_data transforms into the tables "artists" and "songs"

![The Dimension Tables based on song_data](documentation/images/schemas/songs_data_dimensions.png)

#### log_data transforms into the tables "users" and "time"

![The Dimension Tables based on log_data](documentation/images/schemas/log_data_dimensions.png)

#### Dimension Tables

The following diagram shows all four dimension tables.

![The Four Dimension Tables](documentation/images/schemas/dimension_tables.png)

In the center of the dimension table will be the fact table. together, these form
a star schema.

#### The Facts Table "Songplays" and the Star Schema

The `songplays` table is in the center of the four dimension tables. It gets its
data from the original `log_data` as well as the `user_id` from the `users` and the 
`artist_id` from the `artists` table. The `songplays` table references every dimension 
table with a corresponding foreign key. The following diagram depicts the relation
of every column of the facts table:

![The Star Schema](documentation/images/schemas/songplays.png)

The following image shows sample data of the `songplays` facts table:

![The Facts Table](documentation/images/tables/songplays_table.png)

#### Justification, benefit and analysis

With the facts table, sparkify has now many uses for business analysis. Here are some questions that can
be answered now:

- What songs are being played the most?
- What is the preferred time for songplays?
- What browser / operating system are being used?
- What is the distribution between free and paid users?

These additional information will enable sparkify to leverage data and make use of it. 

### Files in this repository

There are four folders in this repository.

- __data__ holds the original data.
- __notebooks__ holds all jupyter notebook. These are files ending in `ipynb`.
- __src__ holds the python scripts that perform the ETL process. 
- __documentation__ contains pictures, screenshots, diagrams, etc.

Inside __notebooks__ you will find three files. Here is a brief explanation of 
the notebooks:

- `etl.ipynb` walks through the ETL process and explains the steps. 
- `explore_data.ipynb` is a means to explore all five postgres tables.
- `test.ipynb` tests if all tables have been successfully created.

Inside __src__ you will find five files upon which this project depends. Here is
a short introduction to these scripts:

- `TableProperties.py` defines the class TableProperties. This class
  builds objects that have properties such as `songs_tableproperties.columns`.
- `sql_queries.py` holds every SQL query that is necessary for this project.
- `create_table.py` deletes all tables and creates them again (without rows). 
- `etl.py` is a programmatic representation of `etl.ipynb`.  
- `etl_david.py` refactors `etl.py` to improve readability and stability.

### How to run the python scripts

Make sure that the machine that runs the scripts have Postgres installed and available.
It's important that the directory `src/` is set to the root. So either make sure to
run the scripts with PYTHONPATH set or make sure to change `sys.path[0]`.

As soon as you fulfill these two requirements, you can run `etl_david.ipynb`. This
script will create all tables and populate the data from `data/`.

```bash
PYTHONPATH="~/path/to/folder/src/:$PYTHONPATH" python3 <script_to_execute>
PYTHONPATH="~/dev/repos/postgres_data_modeling/src/:$PYTHONPATH" python3 etl_david.py
```