i=1
folder=lenovo_offset_20cm
for f in $folder/IMG*; do
    mv "$f" "$folder/ch$i.jpg"
    i=$(($i+1)); 
done
