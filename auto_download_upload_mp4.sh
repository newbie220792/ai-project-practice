#!/bin/bash

WATCH_DIR="/media/rasp/H/nextcloud-data/data/rasp/files/Photos"
DIR_WORK="/root/wso2/convert"
DIR_DOWNLOAD="/media/rasp/H/convert"
PASSWORD="rasp"
VPS_IP="100.120.162.6"
VPS_USERNAME="app_altek"
LIMIT=1

# mkdir -p "$DIR_WORK"
mkdir -p "$DIR_DOWNLOAD"

PROCESSED=0
    
while IFS= read -r FILE
do
[ "$PROCESSED" -ge "$LIMIT" ] && break

MP4="${FILE%.*}.mp4"

# Đã convert rồi
if [ -f "$MP4" ]; then
    continue
fi

echo "Uploading: $FILE"

# Copy MOV sang VPS
sshpass -p "$PASSWORD" rsync -aHAX --partial --append-verify "$FILE" "${VPS_USERNAME}@${VPS_IP}:${DIR_WORK}/inbox/" || {
        echo "Copy to VPS failed: $FILE"
        continue
    }

done < <(
    find "$WATCH_DIR" -type f \( -iname "*.MOV" -o -iname "*.mov" \)
)

sshpass -p "$PASSWORD" rsync -avP --remove-source-files "${VPS_USERNAME}@${VPS_IP}:${DIR_WORK}/done/*.mp4" "${DIR_DOWNLOAD}/" || {
        echo "Download from VPS failed: $FILE"
        continue
    }

echo "Processed: $PROCESSED file(s)"
