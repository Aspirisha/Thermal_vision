folder="samples/real_photos"
prefixes[0]="rgb"
prefixes[1]="tv"

paths[1]="1"
paths[2]="2"

correspondence_file="$folder/correspondence.txt"
rm -f $correspondence_file

j=1
for pref in ${prefixes[@]}; do
	i=1
	out="$folder/$pref"

	tm=0
	for f in "$folder/${paths[$j]}"/DSC*.JPG; do
	    cp "$f" "$out/$pref$i.jpg"
	    if [ "$pref" == "rgb" ]; then  
		    echo "rgb$i.jpg tv$i.jpg" >> $correspondence_file
	    fi
	   	i=$(($i+1));
	done
	j=$(($j + 1))
done