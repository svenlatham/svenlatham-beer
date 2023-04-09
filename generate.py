# This will generate the site in _site for upload to pages

import os, shutil
from distutils.dir_util import copy_tree
import json
import frontmatter

# Set the directory path of the markdown files
md_directory = "./_beer/"

# Set the directory path of the template files
template_directory = "./base/"

image_directory = "./beer-images/"
image_thumb_directory = "./beer-final/480/"

# Set the name of the output files
output_directory = "./_site/"


### STEP 0 - Empty everything in _site

for root, dirs, files in os.walk(output_directory):
    for f in files:
        os.unlink(os.path.join(root, f))
    for d in dirs:
        shutil.rmtree(os.path.join(root, d))

### STEP 1 - Copy everything to _site

copy_tree(template_directory, output_directory)





### STEP 2 - Generate JSON

# Initialize an empty dictionary to store the metadata
metadata_dict = {}

# Iterate over each file in the markdown directory
for file_name in os.listdir(md_directory):
    if file_name.endswith(".md"):
        # Construct the full file path
        file_path = os.path.join(md_directory, file_name)

        id = file_name[:-3] # strip .md extension

        # Open the file and extract the front matter and content
        with open(file_path, "r") as f:
            md_content = f.read()
            md = frontmatter.loads(md_content)
            front_matter = md.metadata
            front_matter['id'] = id

            # Check existence of image:
            img_file = ("%s.jpg" % (id))
            img_check = os.path.join(image_directory, img_file)
            img_actual = os.path.join(image_thumb_directory, img_file)
            if (os.path.exists(img_check)):
                front_matter['image'] = img_actual


            # Add the metadata to the dictionary
            metadata_dict[id] = front_matter

output_file = os.path.join(output_directory, "metadata.json")
# Write the metadata dictionary to a JSON file
with open(output_file, "w") as f:
    json.dump(metadata_dict, f)