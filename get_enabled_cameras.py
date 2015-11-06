import re
import PhotoScan
import shutil
import copy

aligned_rgb_chunk_idx = 0
unaligned_tv_chunk_idx = 1
result_chunk_idx = 2
doc = PhotoScan.app.document

def enable_by_name(enabled_camera_nums):
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
	enabled_camera_nums = []
	enabled_camera_indices = []
	enabled_camera_coords = []
	doc.chunk = doc.chunks[aligned_rgb_chunk_idx]
	unused_cameras = []
	for c in doc.chunk.cameras:
		if not c.enabled:
			unused_cameras.append(c)
	doc.chunk.remove(unused_cameras)
	
	for c in doc.chunk.cameras:
		if c.enabled:
			m = re.search("DSC\d+(\d{4})\.JPG", c.label)
			if m is not None:
				enabled_camera_nums.append(m.group(1))
				enabled_camera_coords.append(c.reference.location)
				enabled_camera_indices.append(doc.chunk.cameras.index(c))
	
	return enabled_camera_nums, enabled_camera_indices, enabled_camera_coords

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
		
def rebuild_texture(chunk):
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

def slerp(v1, v2, t):
	cos_omega = v1 * v2 / (v1.norm() * v2.norm())
	sin_omega = sqrt(1 - cos_omega ** 2)
	omega = acos(cos_omega)
	return (sin((1-t) * omega) * v1 + sin(t * omega) * v2)/sin(omega)

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
	
	translate = lerp(rgb_tr_matrix1.col(4), rgb_tr_matrix2.col(4), t)
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