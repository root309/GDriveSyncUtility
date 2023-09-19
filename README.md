# use API
- Google Drive API
# Execution Steps
### First, configure the Google Drive API.
#### To use this feature, clone or fork this repository.
## `.env` example
Place `.env` file to repository root that contains `FOLDER_ID`, `LOCAL_FOLDER_PATH`,`CREDENTIALS_PATH`.

```
FOLDER_ID=
LOCAL_FOLDER_PATH=
CREDENTIALS_PATH=
```
#### Execute the following command in the cloned repository root
```sh
pip install -r requirements.txt
```
```sh
python downloader.py
```