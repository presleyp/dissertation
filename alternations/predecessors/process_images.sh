for i in $(ls *.png); do
    #convert $i -resize 320x240 ${i%.*}.png
    convert $i -resize 320x240 ${i}
done
