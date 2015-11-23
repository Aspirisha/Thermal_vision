import re
import PhotoScan
import shutil
import copy
from collections import OrderedDict
import math

aligned_rgb_chunk_idx = 0
unaligned_tv_chunk_idx = 1
result_chunk_idx = 2
doc = PhotoScan.app.document

def enable_by_name(enabled_camera_nums, ):
	global doc
	doc.chunk = doc.chunks[unaligned_tv_chunk_idx]
	
	idx = 0
	if len(enabled_camera_nums) > 0:
		for c in doc.chunk.cameras:
			m = re.search("photo_" + enabled_camera_nums[idx] + "\.", c.label)
			if m is not None:
				c.enabled = True
				idx += 1
				if idx == len(enabled_camera_nums):
					break
			else:
				c.enabled = False

def enable_by_distance(enabled_camera_coords, enabled_camera_indices):
	global doc
	doc.chunk = doc.chunks[unaligned_tv_chunk_idx]
	
	rgb_tv_correspondence = {}
	for c in doc.chunk.cameras:
		c.enabled = False
	if len(enabled_camera_coords) > 0:
		for c in doc.chunk.cameras:
			if not c.reference.location:
				continue
			for point, num in zip(enabled_camera_coords, enabled_camera_indices):
				dist = 0
				for coord1, coord2 in zip(point, c.reference.location):
					dist += (coord1 - coord2) ** 2
				if dist < 0.00000001:
					#print(doc.chunks[3].cameras[num].label)
					#print(c.label)
					#print("\n")
					c.enabled = True
					'''if num in rgb_tv_correspondence:
						print('Already have key for ' + 
						str(doc.chunks[aligned_rgb_chunk_idx].cameras[num].label) + ": " 
						+ str(doc.chunk.cameras[rgb_tv_correspondence[num]].label) + " " + c.label)'''
					rgb_tv_correspondence[num] = doc.chunk.cameras.index(c)
					
	return rgb_tv_correspondence

def get_enabled_rgb_cameras():
	global doc
	enabled_camera_indices = []
	enabled_camera_coords = []
	doc.chunk = doc.chunks[aligned_rgb_chunk_idx]
	unused_cameras = []
	for c in doc.chunk.cameras:
		if not c.enabled:
			unused_cameras.append(c)
	
	for idx, c in enumerate(doc.chunk.cameras):
		if c.enabled:
			enabled_camera_coords.append(c.reference.location)
			enabled_camera_indices.append(idx)
	
	return enabled_camera_indices, enabled_camera_coords

def rebuild_merged_chunk():
	global doc
	
	for c in doc.chunks:
		if c.label == 'tv+photo':
			doc.remove(c)
			break
	result_chunk_idx = len(doc.chunks)
	
	enabled_camera_nums, enabled_camera_indices, enabled_camera_coords = get_enabled_rgb_cameras()
	rgb_tv_correspondence = enable_by_distance(enabled_camera_coords, enabled_camera_indices)
	
	doc.mergeChunks([doc.chunks[aligned_rgb_chunk_idx], doc.chunks[unaligned_tv_chunk_idx]], False)
	doc.chunk = doc.chunks[result_chunk_idx]
	doc.chunk.label = 'tv+photo'
	
	offset = len(doc.chunks[aligned_rgb_chunk_idx].cameras)
	for k in rgb_tv_correspondence.keys():
		doc.chunk.cameras[offset + rgb_tv_correspondence[k]].enabled = False
		
	#build model according to normal photos
	#doc.chunk.matchPhotos()
	#doc.chunk.alignCameras()
	doc.chunk.buildModel()	
	
	return rgb_tv_correspondence
		
# returns dictionary: capture_name -> time
def get_capture_times(file_name):
	f = open(file_name)
	return [(lambda x: (x[0], float(x[1])))(x.split(' ')) for x in f]

def build_tv_texture(tv_to_rgb_matrix, rgb_times_file, tv_times_file, cameraMatrix_tv, distCoeffs_tv):
	camera_name_to_index = {}
	doc = PhotoScan.app.document

	for idx, c in enumerate(doc.chunk.cameras):
		camera_name_to_index[c.label] = idx

	rgb_times = get_capture_times(rgb_times_file) # 
	tv_times = get_capture_times(tv_times_file)

	tv_times.sort(key=lambda x: x[1])
	rgb_times.sort(key=lambda x: x[1])

	print(tv_times)
	print(rgb_times)

	rgb_idx = 0
	for c in doc.chunk.cameras:
		c.enabled = False

	for tv_photo, tv_time in tv_times:
		print('tv_time = ' + str(tv_time))
		if rgb_times[rgb_idx][1] > tv_time: # we need to get into interval
			continue
		next_idx = rgb_idx + 1
		if next_idx >= len(rgb_times):
			break

		while rgb_times[next_idx][1] < tv_time:
			next_idx += 1
			if next_idx >= len(rgb_times):
				break
		else:
			print('here')
			rgb_idx = next_idx - 1

			name2, t2 = rgb_times[next_idx]
			name1, t1 = rgb_times[rgb_idx]
			print('rgb_idx: ' + str(rgb_idx))
			print('next_idx: ' + str(next_idx))
			print('name1: ' + name1)
			print('name2: ' + name2)

			idx1 = camera_name_to_index.get(name1)
			idx2 = camera_name_to_index.get(name2)
			print(idx1)
			print(idx2)

			if idx1 is None or idx2 is None:
				continue

			rgb_tr_matrix1 = doc.chunk.cameras[idx1].transform
			rgb_tr_matrix2 = doc.chunk.cameras[idx2].transform

			if not rgb_tr_matrix1 or not rgb_tr_matrix2:
				continue

			print('there')
			tr_mat = get_transfom_matrix_for_tv(rgb_tr_matrix1, t1, rgb_tr_matrix2, t2, tv_to_rgb_matrix, tv_time)
			tv_camera = doc.chunk.cameras[camera_name_to_index[tv_photo]]
			tv_camera.transform = tr_mat
			tv_camera.sensor.calibration.fx = cameraMatrix_tv[0,0]
			tv_camera.sensor.calibration.fy = cameraMatrix_tv[1,1]
			tv_camera.sensor.calibration.cx = cameraMatrix_tv[0,2]
			tv_camera.sensor.calibration.cy = cameraMatrix_tv[1,2]
			tv_camera.sensor.calibration.k1 = distCoeffs_tv[0]
			tv_camera.sensor.calibration.k2 = distCoeffs_tv[1]
			tv_camera.sensor.calibration.p1 = distCoeffs_tv[2]
			tv_camera.sensor.calibration.p2 = distCoeffs_tv[3]
			tv_camera.enabled = True


	#for c in doc.chunk.cameras:
	#	c.enabled = not c.enabled
	doc.chunk.buildUV()
	doc.chunk.buildTexture(blending=PhotoScan.BlendingMode.AverageBlending)
		
def main(need_rebuild):	
	global result_chunk_idx
	if need_rebuild:
		rgb_tv_correspondence = rebuild_merged_chunk()
	else:
		enabled_camera_nums, enabled_camera_indices, enabled_camera_coords = get_enabled_rgb_cameras()
		rgb_tv_correspondence = enable_by_distance(enabled_camera_coords, enabled_camera_indices)
	
	for c in doc.chunks:
		if c.label == 'tv+photo':
			result_chunk_idx = doc.chunks.index(c)
			break
		
	print(rgb_tv_correspondence)
	doc.chunk = doc.chunks[result_chunk_idx]
	refine_tv_coordinates()
	offset = len(doc.chunks[aligned_rgb_chunk_idx].cameras)
	
	print(len(doc.chunk.cameras))
	for k in rgb_tv_correspondence.keys():
		rgb_camera = doc.chunk.cameras[k]
		tv_camera = doc.chunk.cameras[offset + rgb_tv_correspondence[k]]
		
		rgb_camera.enabled = False
		tv_camera.enabled = True
		
		center_position = doc.chunk.transform.matrix.inv().mulp(doc.chunk.crs.unproject(tv_camera.reference.location))
		
		tmp = rgb_camera.transform.copy()
		for i in range(0, 3):
			tmp[i, 3] = center_position[i]
	
		tv_camera.transform = tmp
		print(tv_camera.center)
		
	#doc.chunk.alignCameras()
	rebuild_texture(doc.chunk)

def temp():
	global doc
	doc.chunk = doc.chunks[3]
	for k in range(0, 39):
		rgb_camera = doc.chunk.cameras[k]
		tv_camera = doc.chunk.cameras[39 + k]
		
		rgb_camera.enabled = True
		tv_camera.enabled = False
		
		#center_position = doc.chunk.transform.matrix.inv().mulp(doc.chunk.crs.unproject(tv_camera.reference.location))
		
		tmp = tv_camera.transform.copy()
		#for i in range(0, 3):
		#	tmp[i, 3] = center_position[i]

		rgb_camera.transform = tmp
	
def remove_unused_cameras(chunk_idx): 
	global doc
	doc.chunk = doc.chunks[chunk_idx]
	unused_cameras = []
	for c in doc.chunk.cameras:
		if not c.enabled:
			unused_cameras.append(c)
	doc.chunk.remove(unused_cameras)


#"C:/Users/pscan.user/Desktop/TEPLOVIZOR-Komintern-f1/RGB/"
#"C:/Users/pscan.user/Desktop/TEPLOVIZOR-Komintern-f1/tmp"
def copy_chosen_photos(chunk, folder_src, folder_dst):
	global doc
	for c in chunk.cameras:
		name = os.path.normpath(folder_src + '/' + c.label)
		name1 = os.path.normpath(folder_dst)
		shutil.copy2(name, name1)	

# returns scale. If we multiply it by distance in real world (meters), we get 
# distance in chunk crs (or, equally, in camera crs for they have same scale) 
def get_chunk_scale(chunk):
	e0 = PhotoScan.Vector([0, 0, 0])
	e1 = PhotoScan.Vector([0, 0, 1])
	scale = (chunk.transform.matrix.inv().mulp(chunk.crs.unproject(e1)) - chunk.transform.matrix.inv().mulp(chunk.crs.unproject(e0))).norm()
	return scale

def scale_transform_matrix(m, chunk_scale):
	new_mat = m.copy()
	for i in range(3):
		new_mat[3, i] *= chunk_scale
	return new_mat

def slerp(v1, v2, t):
	cos_omega = v1 * v2 / (v1.norm() * v2.norm())
	sin_omega = math.sqrt(1 - cos_omega ** 2)
	omega = math.acos(cos_omega)
	return (math.sin((1-t) * omega) * v1 + math.sin(t * omega) * v2)/math.sin(omega)

def lerp(v1, v2, t):
	return (v1 * (1 - t) + v2 * t)
	
	
# we assume time1 <= time <= time2 
# tv_to_rgb_matrix should be somehow predefined
def get_transfom_matrix_for_tv(rgb_tr_matrix1, time1, rgb_tr_matrix2, time2, tv_to_rgb_matrix, time):
	# decompose rgb_tr_matrix1, rgb_tr_matrix2 into (R1, T1) and (R2, T2). 
	# apply slerp to R1 and R2 column-wise, apply lerp to T1 and T2
	t = (time - time1) / (time2 - time1)
	
	result_matrix = PhotoScan.Matrix.diag(PhotoScan.Vector([0, 0, 0, 1]))
	for i in range(0, 2):
		v1 = rgb_tr_matrix1.col(i).copy()
		v2 = rgb_tr_matrix2.col(i).copy()
		v = slerp(v1, v2, t)
		for j in range(0, 2):
			result_matrix[i, j] = v[j]
	
	translate = lerp(rgb_tr_matrix1.col(3), rgb_tr_matrix2.col(3), t)
	for j in range(0, 2):
		result_matrix[3, j] = translate[j]
	
	return result_matrix * tv_to_rgb_matrix


def refine_tv_coordinates():
	global doc
	
	doc.chunk = doc.chunks[result_chunk_idx]
	scale = get_chunk_scale(doc.chunk)
	offset = len(doc.chunks[aligned_rgb_chunk_idx].cameras)
	cameras = doc.chunk.cameras 
	tv_cameras_number = len(doc.chunks[unaligned_tv_chunk_idx].cameras)
	
	for i in range(offset, offset + tv_cameras_number):
		rgb_camera = cameras[i - offset]
		tv_camera = cameras[i]
		estimated_location = doc.chunk.crs.project(doc.chunk.transform.matrix.mulp(rgb_camera.center))
		dx = estimated_location - rgb_camera.reference.location
		print(dx)
		doc.chunk.cameras[i].reference.location += dx
		

#main(True)