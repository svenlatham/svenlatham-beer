# This will generate the site in _site for upload to pages

import os
import json
import frontmatter

# Set the directory path of the markdown files
md_directory = "./_beer/"

# Set the directory path of the template files
template_directory = "./base/"

# Set the name of the output files
output_directory = "./_site/"

### STEP 1 - Generate JSON

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

            # Add the metadata to the dictionary
            metadata_dict[id] = front_matter

# Write the metadata dictionary to a JSON file
with open(output_file, "w") as f:
    json.dump(metadata_dict, f)