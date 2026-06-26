#!/bin/bash

WATCH_DIR="/media/rasp/H/nextcloud-data/data/rasp/files/Photos/icloud"
DIR_WORK="/root/wso2/convert"
DIR_DOWNLOAD="/media/rasp/D/convert"
PASSWORD="password"
VPS_IP="100.120.162.6"
VPS_USERNAME="app_altek"
LIMIT=1

DATE=$(date '+%d/%m/%Y %H:%M:%S')

mkdir -p "$DIR_DOWNLOAD"

echo "$DATE: Downloading converted files from VPS..."

sshpass -p "$PASSWORD" rsync -avP --remove-source-files "${VPS_USERNAME}@${VPS_IP}:${DIR_WORK}/done/*.mp4" "${DIR_DOWNLOAD}/" || {
        echo "$DATE: Download from VPS failed: $DIR_WORK/done"
    }

PROCESSED=0
    
while IFS= read -r FILE
do
[ "$PROCESSED" -ge "$LIMIT" ] && break

MP4="${FILE%.*}.mp4"
BASENAME=$(basename -- "${FILE%.*}")

DIR_MP4="$DIR_DOWNLOAD/${BASENAME}.mp4"

# Đã convert rồi
if [ -f "$DIR_MP4" ] || grep -q "^$FILE$" "${DIR_DOWNLOAD}/file_uploaded.txt" 2>/dev/null; then
    continue
fi

echo "$DATE: Uploading: $FILE"

# Copy MOV sang VPS
sshpass -p "$PASSWORD" rsync -aHAX --partial --append-verify "$FILE" "${VPS_USERNAME}@${VPS_IP}:${DIR_WORK}/inbox/" || {
        echo "$DATE: Copy to VPS failed: $FILE"
        continue
    }

PROCESSED=$((PROCESSED + 1))
echo "$FILE" >> "${DIR_DOWNLOAD}/file_uploaded.txt"

done < <(
    find "$WATCH_DIR" -type f \( -iname "*.MOV" -o -iname "*.mov" \)
)

echo "$DATE: Processed: $PROCESSED file(s)"