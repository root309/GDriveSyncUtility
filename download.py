from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import io
from googleapiclient.http import MediaIoBaseDownload
import os

def download_files_from_folder(service, folder_id, local_folder_path): # Driveの特定のフォルダをダウンロードする関数
    if not os.path.exists(local_folder_path): # ローカルのダウンロード先フォルダの存在確認条件文
        os.makedirs(local_folder_path) # 存在しない場合は作成

    # フォルダ内のファイルとサブフォルダを取得
    results = service.files().list(q=f"'{folder_id}' in parents", fields="files(id, name, mimeType)").execute()
    items = results.get('files', [])

    for item in items:
        file_id = item['id'] # ファイルまたはフォルダの一意な識別子
        file_name = item['name'] # ファイルまたはフォルダの名前
        mime_type = item['mimeType'] # ファイルのMIMEタイプ
        # ファイルorフォルダの識別
        if mime_type == 'application/vnd.google-apps.folder':
            # サブフォルダの場合、再帰的にダウンロード
            new_local_folder_path = os.path.join(local_folder_path, file_name)
            download_files_from_folder(service, file_id, new_local_folder_path)
        else:
            # ファイルの場合、ダウンロード
            request = service.files().get_media(fileId=file_id)
            fh = io.FileIO(os.path.join(local_folder_path, file_name), 'wb')
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(f"ダウンロード完了 {file_name}: {int(status.progress() * 100)}%.")

# API認証
credentials = Credentials.from_service_account_file("C:\\path\\to", # ダウンロードしたAPI認証キーのjsonファイルのPath
    scopes=["https://www.googleapis.com/auth/drive.readonly"])

# Google Drive API クライアントを構築
service = build('drive', 'v3', credentials=credentials)

# ダウンロードするフォルダのID drive.google.com/drive/u/0/folders/ここの部分がフォルダID
folder_id = ''

# ローカルの保存先フォルダのパス
local_folder_path = 'C:\\path\\to'

# ダウンロード開始
download_files_from_folder(service, folder_id, local_folder_path)
