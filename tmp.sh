folder="wall2"
prefixes[0]="rgb"
prefixes[1]="tv"

time_rgb="$folder/rgb/time_rgb.txt"
time_tv="$folder/tv/time_tv.txt"
rm -f $time_tv
rm -f $time_rgb

for pref in ${prefixes[@]}; do
	i=1
	out="$folder/$pref"

	tm=0
	for f in "$folder"/DSC*.JPG; do
	    cp "$f" "$out/$pref$i.jpg"
	    if [ "$pref" == "rgb" ]; then  
		    echo "rgb$i.jpg $tm" >> $time_rgb
		    tm=`echo "scale=5; $tm+0.001" | bc`
		    echo "tv$i.jpg $tm" >> $time_tv
		    tm=`echo "scale=5; $tm+$RANDOM/32767" | bc`
	    fi
	   	i=$(($i+1));
	done
done