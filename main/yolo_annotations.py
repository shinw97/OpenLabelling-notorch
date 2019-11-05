from PIL import Image
import os

def convert(image_width, image_height, params, classes):
	for i in range(len(params) - 1):
		params[i] = int(params[i])
	
	bounding_box_width = params[2] - params[0]
	bounding_box_height = params[3] - params[1]
	params[0] += bounding_box_width/2
	params[0] /= image_width
	params[1] += bounding_box_height/2
	params[1] /= image_height
	
	params[2] = bounding_box_width
	params[2] /= image_width
	params[3] = bounding_box_height
	params[3] /= image_height
	params[4] = classes.index(params[4])
	params.insert(0, params.pop())
	return params

image_dir = 'Images/002/'
bbox_annotation_path = 'Labels/002/'
output_new_annotation_path = 'Converted_Labels/002/'
classes = ['bee']

images_path = os.listdir(image_dir)
annotations_path = os.listdir(bbox_annotation_path)

image_names = [x.split('.')[0] for x in annotations_path]

for image in image_names:
	with open(bbox_annotation_path + image + '.txt') as f:
		lines = f.readlines()
	
	cleaned_lines = [l.split('\n')[0] for l in lines]

	num_objects = int(cleaned_lines[0])

	im = Image.open(image_dir + image + '.jpg')
	image_width, image_height = im.size
	print(image_width, image_height)
	converted_params = []
	for i in range(1, len(cleaned_lines)):
		converted_params.append(convert(image_width, image_height, cleaned_lines[i].split(' '), classes))
	print(num_objects)
	print(converted_params)
	with open(output_new_annotation_path + image + '.txt', 'w') as w:
		content = ''
		for param in converted_params:
			content += " ".join([str(p) for p in param])
			content += '\n'
		w.write(content)
