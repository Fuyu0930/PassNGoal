from PIL import Image
import os
import PIL

def resize_images(input_dir, output_dir, size = (120, 100)):
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)

	for filename in os.listdir(input_dir):
		if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
			input_path = os.path.join(input_dir, filename)
			output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '_edit' + '.png')

			try:
				img = Image.open(input_path)
				img = img.resize(size, Image.BICUBIC)
				img.save(output_path, 'PNG')
				print(f'{filename} has been resized and saved as {output_path}')
			except Exception as e:
				print(f"Error processing {filename}: {e}")

#input_directory = '/Users/william/Desktop/PassNGoal/PassNGoalBlog/static/profile_pics'
#output_directory = '/Users/william/Desktop/PassNGoal/PassNGoalBlog/static/profile_pics'
input_directory = '/Users/william/Desktop/PassNGoal/PassNGoalBlog/static/logo'
output_directory = '/Users/william/Desktop/PassNGoal/PassNGoalBlog/static/logo'

resize_images(input_directory, output_directory)