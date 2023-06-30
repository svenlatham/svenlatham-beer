import os
from markdown import Markdown

filepath = "/app/_beer/"
imgpath = "/app/beer-thumbs/"

class Beer:
    name = None
    description = None
    strength = None

def get_all():
    md = Markdown(extensions=['meta'])
    onlyfiles = [f for f in os.listdir(filepath) if os.path.isfile(os.path.join(filepath, f))]
    files = []
    for res in onlyfiles:
        fileloc = os.path.join(filepath, res)
        mdfile = md.convertFile(fileloc)
        mdmeta = md.Meta
        file = Beer()
        file.name = "".join(mdmeta['name'])
        file.description = "".join(mdmeta['description'])
        file.strength = "".join(mdmeta['strength']) if 'strength' in mdmeta else None
        file.trappist = True if 'trappist' in mdmeta else False
        file.brewer = "".join(mdmeta['brewer']) if 'brewer' in mdmeta else None
        file.country = "".join(mdmeta['country']) if 'country' in mdmeta else None
        file.img = None

        # check to see if there's an image:
        imgfile = res.replace(".md",".jpg")
        if os.path.isfile(os.path.join(imgpath, imgfile)):
            file.img = imgfile

        files.append(file)
        md.reset()
    return files


#{'name': ['Gouverneur Tripel'], 'description': ['First few tastes were quite sour, but it steadily improved through the bottle. Nice smooth texture with a creamy aftertaste.'], 'strength': ['8.2%'], 'kcalhundredml': ['62'], 'brewer': ['Lindeboom Bierbrouwerij'], 'country': ['nl']}
#\trappist: True