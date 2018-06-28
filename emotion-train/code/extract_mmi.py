import cv2
import glob
import xml.etree.ElementTree as ET

BASE_FOLDER = '/home/adriana/Documents/emotion-train/input/mmi_photos/'
video_folders = [f for f in glob.glob('/home/adriana/Documents/emotion-train/input/mmi/*')]

count = 0
for folder in video_folders:
	info_file = glob.glob(folder + '/S*.xml')[0]

	tree = ET.parse(info_file)
	root = tree.getroot()
	for child in root:
		if child.get('Name') == 'Emotion':
			emotion = int(child.get('Value'))
			print emotion
			break

	if emotion >= 7:
		continue

	video_file = glob.glob(folder + '/*.avi')[0]

	vidcap = cv2.VideoCapture(video_file)
	success,image = vidcap.read()
	frame_count = 0
	while success:
		frame_count += 1
		success, image = vidcap.read()


	vidcap = cv2.VideoCapture(video_file)

	local_count = 0
	success,image = vidcap.read()

	#add first photo to neutral
	if success:
		rows,cols,ch = image.shape
		M = cv2.getRotationMatrix2D((cols/2,rows/2), -90, 1)
		image = cv2.warpAffine(image,M,(cols,rows))
		cv2.imwrite((BASE_FOLDER + "0/frame%d.jpg") % count, image)
		count += 1

	while success:
		if local_count > frame_count / 3 and local_count < 2 * frame_count / 3:
			rows,cols, ch = image.shape
			M = cv2.getRotationMatrix2D((cols/2,rows/2), -90, 1)
			image = cv2.warpAffine(image,M,(cols,rows))

			cv2.imwrite((BASE_FOLDER + "%d/frame%d.jpg") % (emotion, count), image)
			count += 1

		success,image = vidcap.read()
		local_count += 1
