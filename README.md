# GDriveSyncUtility (English)
GDriveSyncUtility is a tool to easily synchronize files in Google Drive with local files, using Google Drive API to batch download files in a specified folder.

When a file in GDrive is updated, the program can be re-run to download only the updated file and synchronize GDrive and local files.
# GDriveSyncUtility (日本語)
GDriveSyncUtilityは、Google Drive内のファイルとローカルファイルを簡単に同期させるツールです。Google Drive APIを利用して、指定したフォルダ内のファイルを一括ダウンロードします。

GDrive内のファイルが更新された場合、プログラムを再実行することで、更新されたファイルのみをダウンロードし、GDriveとローカルファイルを同期させることができます。
# Technologies Used
- Google Drive API
- Python 3.11
# Setup
1. Configure the Google Drive API.
2. Clone or fork this repository.
3. Create a `.env` file in the root of the repository and configure it as follows
    ## `.env` example
    Place `.env` file to repository root that contains `FOLDER_ID`, `LOCAL_FOLDER_PATH`,      `CREDENTIALS_PATH`.
    ```
    FOLDER_ID=your_folder_id_here
    LOCAL_FOLDER_PATH=your_local_folder_path_here
    CREDENTIALS_PATH=your_credentials_path_here
    ```
# Execution
In the cloned repository root, execute the following commands:
```sh
pip install -r requirements.txt
```
```sh
python downloader.py
```
# Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.