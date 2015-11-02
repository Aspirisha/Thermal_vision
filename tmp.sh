i=3
for f in IMG*; do
mv "$f" "ch$i.jpg"
i=$(($i+1)); 
done
