# Generate random image
docker run -v `pwd`:/mnt dpokidov/imagemagick:7.0.10-9 -size 128x128 xc:"gray(50%)" +noise random -level -20%,120%,1.0 -quality 50 /mnt/noise.jpg

# Stego magick here!
python stego.py noise.jpg secret.zip -o output.png

# Clean up
rm noise.jpg secret.zip
