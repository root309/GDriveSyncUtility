import os
import io
from pytz import timezone
from datetime import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# もしローカルのmodifiedTimeがGoogle Driveのものと同じかそれより新しければTrueを返す関数
def is_up_to_date(local_file_path, modified_time_drive):
    # ローカルファイルのmodified_time_local(最終変更時間)とGoogle Driveのファイルのmodified_time_drive(最終変更時間)を比較
    if os.path.exists(local_file_path):
        modified_time_local = datetime.utcfromtimestamp(os.path.getmtime(local_file_path)).replace(tzinfo=timezone('UTC'))
        return modified_time_local >= modified_time_drive
    return False

def download_file(service, file_id, local_file_path, file_name):
    # ファイルをダウンロードする
    print(f"Downloading... {file_name}.")
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(local_file_path, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download completed! for -> {file_name}: {int(status.progress() * 100)}%.")
# 引数で指定されたDriveのフォルダ内のすべてのフォルダとファイルをダウンロードする関数
def download_files_from_folder(service, folder_id, local_folder_path):
    # Driveの特定のフォルダをダウンロードする関数
    if not os.path.exists(local_folder_path):
        os.makedirs(local_folder_path)  # ローカルのダウンロード先フォルダが存在しない場合は作成

    # フォルダ内のファイルとサブフォルダを取得
    results = service.files().list(
        q=f"'{folder_id}' in parents",
        fields="files(id, name, modifiedTime, mimeType)").execute()
    items = results.get('files', [])

    for item in items:
        file_id = item['id']
        file_name = item['name']
        mime_type = item['mimeType']
        local_file_path = os.path.join(local_folder_path, file_name)
        # すべてのファイルとサブフォルダに対して、ファイルであるかサブフォルダであるかを判断させる
        if mime_type == 'application/vnd.google-apps.folder':  # サブフォルダの場合
            new_folder_path = os.path.join(local_folder_path, file_name)
            download_files_from_folder(service, file_id, new_folder_path)  # 再帰的に探索
        else:
            # APIから取得されるmodifiedTimeをオブジェクト化
            modified_time_drive = datetime.fromisoformat(item['modifiedTime'][:-1]).replace(tzinfo=timezone('UTC'))
            # ダウンロードが必要かどうか
            if is_up_to_date(local_file_path, modified_time_drive):
                print(f"{file_name} is up to date!. skip the download.")
                continue

            download_file(service, file_id, local_file_path, file_name)



# API認証
credentials = Credentials.from_service_account_file("C:\\path\\.json", # ダウンロードしたAPI認証キーのjsonファイルのPath
    scopes=["https://www.googleapis.com/auth/drive.readonly"])

# Google Drive API クライアントを構築
service = build('drive', 'v3', credentials=credentials)

# ダウンロードするフォルダのID drive.google.com/drive/u/0/folders/ここの部分がフォルダID
folder_id = 'here'

# ローカルの保存先フォルダのパス
local_folder_path = 'C:\\path\\to'

# ダウンロード開始
download_files_from_folder(service, folder_id, local_folder_path)
