import glob
import xml.etree.ElementTree as ET

import numpy as np

from kmeans import kmeans, avg_iou

ANNOTATIONS_PATH = "Annotations"
CLUSTERS = 5

def load_dataset(path, 
	             relatice=True,
	             target_size=600):
    '''
    if relative=True, the images input should be of same size, like YOLO  mode. Relitive values will be caculated.
    if relative=False, the images input can be different size, like Faster R-CNN mode. Absolute values will be caculated.
    '''
	dataset = []
	for xml_file in glob.glob("{}/*xml".format(path)):
		tree = ET.parse(xml_file)

		height = int(tree.findtext("./size/height"))
		width = int(tree.findtext("./size/width"))
        
        if relative :
			for obj in tree.iter("object"):
				xmin = int(obj.findtext("bndbox/xmin")) / width
				ymin = int(obj.findtext("bndbox/ymin")) / height
				xmax = int(obj.findtext("bndbox/xmax")) / width
				ymax = int(obj.findtext("bndbox/ymax")) / height

				dataset.append([xmax - xmin, ymax - ymin])

		else :
			ratio = target_size / np.min(height, width)
			for obj in tree.iter("object"):
				xmin = int(obj.findtext("bndbox/xmin")) * ratio
				ymin = int(obj.findtext("bndbox/ymin")) * ratio
				xmax = int(obj.findtext("bndbox/xmax")) * ratio
				ymax = int(obj.findtext("bndbox/ymax")) * ratio

				dataset.append([xmax - xmin, ymax - ymin])


	return np.array(dataset)


data = load_dataset(ANNOTATIONS_PATH)
out = kmeans(data, k=CLUSTERS)
print("Accuracy: {:.2f}%".format(avg_iou(data, out) * 100))
print("Boxes:\n {}".format(out))

ratios = np.around(out[:, 0] / out[:, 1], decimals=2).tolist()
print("Ratios:\n {}".format(sorted(ratios)))