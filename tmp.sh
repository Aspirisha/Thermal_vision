folder="samples/chessboard_lenovo"
prefixes[0]="rgb"
prefixes[1]="tv"

for pref in ${prefixes[@]}; do
	i=1
	out="samples/$pref"
	time1="$out/time_$pref.txt"
	tm=0
	rm -f $time1
	for f in "$folder"/IMG*.jpg; do
	    cp "$f" "$out/$pref$i.jpg"
	    i=$(($i+1)); 
	    echo "$pref$i.jpg : $tm" >> $time1
	    tm=`echo "scale=5; $tm+$RANDOM/32767" | bc`
	done
done