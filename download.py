from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import io
from googleapiclient.http import MediaIoBaseDownload
import os

def download_files_from_folder(service, folder_id, local_folder_path):
    if not os.path.exists(local_folder_path):
        os.makedirs(local_folder_path)

    # フォルダ内のファイルを取得
    results = service.files().list(q=f"'{folder_id}' in parents", fields="files(id, name)").execute()
    items = results.get('files', [])

    for item in items:
        file_id = item['id']
        request = service.files().get_media(fileId=file_id)

        fh = io.FileIO(f"{local_folder_path}/{item['name']}", 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"ダウンロード完了 {item['name']}: {int(status.progress() * 100)}%.")

# サービスアカウントの認証
credentials = Credentials.from_service_account_file("jsonのapikeyのローカルパスを入力",
    scopes=["https://www.googleapis.com/auth/drive.readonly"])

# Google Drive API クライアントを構築
service = build('drive', 'v3', credentials=credentials)

# ダウンロードするフォルダのID drive.google.com/drive/u/0/folders/ここの部分がフォルダID
folder_id = ''

# ローカルの保存先フォルダのパス
local_folder_path = 'C:\\path\\to'

# ダウンロード開始
download_files_from_folder(service, folder_id, local_folder_path)