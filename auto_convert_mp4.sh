#!/bin/bash

LOCKFILE="/var/run/convert_mov.lock"

exec 200>"$LOCKFILE"
flock -n 200 || {
    echo "$(date): Another instance is running."
    exit 0
}

DIR_WORK="/root/wso2/convert"
LIMIT=1

PROCESSED=0
    
while IFS= read -r FILE
do
[ "$PROCESSED" -ge "$LIMIT" ] && break

MP4="${FILE%.*}.mp4"

BASENAME=$(basename -- "${FILE%.*}")

# DIR_MOV="$DIR_WORK/inbox/${BASENAME}.MOV"
DIR_MP4="$DIR_WORK/done/${BASENAME}.mp4"

if [ -f "$DIR_MP4" ]; then
    continue
fi

if [ ! -f "$FILE" ]; then
    echo "Missing file: $FILE"
    continue
fi

echo "FILE=$FILE"

# Convert trên VPS
/usr/local/bin/ffmpeg -nostdin \
    -y -hide_banner -loglevel error \
    -i "$FILE" \
    -vf "scale=1920:-2,format=yuv420p" \
    -c:v libx264 \
    -preset veryfast \
    -crf 24 \
    -c:a aac \
    -b:a 128k \
    -movflags +faststart \
    "$DIR_MP4"

if [ $? -eq 0 ]; then
    touch -r "$FILE" "$DIR_MP4"
    echo "Success: $DIR_MP4"
    PROCESSED=$((PROCESSED + 1))
    rm -f "$FILE"
else
    echo "Convert failed: $FILE"
fi

done < <(
    find "$DIR_WORK/inbox" -type f \( -iname "*.MOV" -o -iname "*.mov" \)
)

echo "$(date): Processed: $PROCESSED file(s)"
