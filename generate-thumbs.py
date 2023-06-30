import os
from PIL import Image, ImageOps

indir = "/app/beer-images/"
outdir = "/app/beer-thumbs/"
# Ensure the outdir exists
os.makedirs(outdir, exist_ok=True)

def generate_all():
    onlyfiles = [f for f in os.listdir(indir) if os.path.isfile(os.path.join(indir, f))]
    for res in onlyfiles:
        infile = os.path.join(indir, res)
        outfile = os.path.join(outdir, res)
        image = Image.open(infile)
        thumb = ImageOps.fit(image, (500, 300), Image.ANTIALIAS)
        thumb.save(outfile)
        print("Writing to %s" % (outfile))

generate_all()

# Generate a blank file:
img = Image.new("RGB", (500, 300), (255, 255, 255))
img.save(os.path.join(outdir, "empty.jpg"))