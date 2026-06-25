#!/bin/bash

DIR_WORK="/root/wso2/convert"
LIMIT=1

PROCESSED=0
    
while IFS= read -r FILE
do
[ "$PROCESSED" -ge "$LIMIT" ] && break

MP4="${FILE%.*}.mp4"

# Đã convert rồi
if [ -f "$MP4" ]; then
    continue
fi

BASENAME=$(basename -- "${FILE%.*}")

DIR_MOV="$DIR_WORK/inbox/${BASENAME}.mov"
DIR_MP4="$DIR_WORK/done/${BASENAME}.mp4"

echo "Processing: $FILE"

# Convert trên VPS
nice -n 15 ionice -c3 \
ffmpeg -y -hide_banner -loglevel error \
    -i "$DIR_MOV" \
    -vf "scale=1920:-2,format=yuv420p" \
    -c:v libx264 \
    -preset veryfast \
    -crf 24 \
    -c:a aac \
    -b:a 128k \
    -movflags +faststart \
    "$DIR_MP4"

if [ $? -eq 0 ]; then
    if [ $? -eq 0 ]; then
        touch -r "$FILE" "$MP4"
        echo "Success: $MP4"
        PROCESSED=$((PROCESSED + 1))
        # Nếu muốn xóa MOV gốc:
        # rm -f "$FILE"
    fi
else
    echo "Convert failed: $FILE"
fi

done < <(
    find "$DIR_WORK/inbox" -type f \( -iname "*.MOV" -o -iname "*.mov" \)
)

echo "Processed: $PROCESSED file(s)"
