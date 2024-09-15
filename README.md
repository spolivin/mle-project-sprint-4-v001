# Recommendation system of music tracks: building and testing

## Cloning repository

Firsly, we need to clone the repository:

```
git clone git@github.com:spolivin/mle-project-sprint-4-v001.git
```

## Loading data

Files used during building the recommendation system are downloaded using the following commands:

```bash
wget https://storage.yandexcloud.net/mle-data/ym/tracks.parquet -P data

wget https://storage.yandexcloud.net/mle-data/ym/catalog_names.parquet -P data

wget https://storage.yandexcloud.net/mle-data/ym/interactions.parquet -P data
```

The entire process of building the recommendations can be consulted in [this notebook](./recommendations.ipynb).

## Virtual environment

We can activate the virtual environment using the following series of commands:

```bash
sudo apt-get update
sudo apt-get install python3.10-venv
python3.10 -m venv .venv_recsys_app
source .venv_recsys_app/bin/activate
pip install --no-cache-dir -r requirements.txt
```
> NOTE: Before installing the packages into the virtual environment, it might be necessary to firstly run `sudo apt-get install build-essential` to install additional packages to *Ubuntu* system.

## Preparation for launching a microservice

Before launching the services, it is essential to firstly load data files with recommendations from *S3* cloud storage. Data take up quite a lot of memory so this method was chosen to avoid overloading the repository with large files.

Loading all required files is pretty straightforward, all one need to do is run [this script](./s3_scripts/prepare_datasets.py) using the following command:

```bash
python s3_scripts/prepare_datasets.py
```

After running the script all files are loaded to `data` folder by default.

## Application launch

Microservice is made up of 4 modules in `services`:

* [`recommendations_service.py`](service/recommendations_service.py) => Main application which generates recommendations of all types 
* [`events_service.py`](service/events_service.py) => Service for adding online events (musical tracks) to the online history of a user
* [`features_service.py`](service/features_service.py) => Service for generating online recommendations based on musical tracks similarity
* [`recs_offline_service.py`](service/recs_offline_service.py) => Service for generating offline recommendations
* [`constants.py`](service/constants.py) => File with main constants used for the application functioning.

Recommendation service can be launched using [main script](./run_service.py) which executes each of the aforementioned services by `--service-name` flag: 

```bash
# Terminal window 1
python run_service.py --service-name=main_app
```
```bash
# Terminal window 2
python run_service.py --service-name=recs_store
```
```bash
# Terminal window 3
python run_service.py --service-name=features_store
```
```bash
# Terminal window 4
python run_service.py --service-name=events_store
```

After all services having been launched successfully (which will be shown in each terminal), requests to the application can be sent.

## Microservice testing

Testing the application can be launched using the following command:

```python
# Terminal window 5 (testing)
python test_service.py
```

The output of the testing process is automatically logged to [`test_service.log`](./test_service.log).

## Strategy of blending recommendations

As can be seen in the [main application code](service/recommendations_service.py), provided that a user has an online history, the final recommendations for such a user are computed by mixing up online and offline recommendations where online ones are located on odd places, while offline recommendations - on even places.

## Stopping the application

After finishing working with the application, one needs to stop each of the 4 service by entering `Ctrl+C` in each of the respective terminal windows.
