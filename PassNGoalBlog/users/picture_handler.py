# users/picture_handler.py

import os
from PIL import Image
from flask import url_for, current_app

# Add the profile pic to the certain folder, and return the storage filename
def add_profile_pic(pic_upload, username):
    filename = pic_upload.filename
    ext_type = filename.split('.')[-1]
    storage_filename = str(username) + '.' + ext_type

    filepath = os.path.join(current_app.root_path, 'static/profile_pics', storage_filename)

    # Store the picture
    output_size = (200, 200)
    pic = Image.open(pic_upload)
    pic.thumbnail(output_size)
    pic.save(filepath)

    return storage_filename