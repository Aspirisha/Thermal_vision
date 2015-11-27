import PhotoScan
import copy
import math

def get_default_calibration_file(file_name, tv_times_file):
	f = open(tv_times_file)
	name = f.readline().split(' ')[0]
	doc = PhotoScan.app.document

	sensor = None
	for c in doc.chunk.cameras:
		if c.label == name:
			sensor = c.sensor
			break
	sensor.calibration.save(file_name)

# returns dictionary: capture_name -> time
def get_capture_times(file_name):
	f = open(file_name)
	return [(lambda x: (x[0], float(x[1])))(x.split(' ')) for x in f]

def build_tv_texture(tv_to_rgb_matrix, rgb_times_file, tv_times_file, calibration_file):
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

	chunk_scale = get_chunk_scale(doc.chunk)
	tv_to_rgb_matrix = scale_transform_matrix(tv_to_rgb_matrix, chunk_scale)

    # apply calibration to cameras sensor
    # we can take any camera!
	tv_camera = doc.chunk.cameras[camera_name_to_index[tv_times[0][0]]]
	new_calibration = PhotoScan.Calibration()
	new_calibration.load(calibration_file) # /home/plaz/calib.xml
	print(tv_camera.sensor.calibration.fx)
	tv_camera.sensor.calibration = new_calibration
	print(tv_camera.sensor.calibration.fx)

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
			tv_camera.enabled = True

	#doc.chunk.buildUV()
	#doc.chunk.buildTexture(blending=PhotoScan.BlendingMode.MosaicBlending)


# returns scale. If we multiply it by distance in real world (meters), we get 
# distance in chunk crs (or, equally, in camera crs for they have same scale) 
def get_chunk_scale(chunk):
	e0 = PhotoScan.Vector([0, 0, 0])
	e1 = PhotoScan.Vector([0, 0, 1])
	try:
		scale = (chunk.transform.matrix.inv().mulp(chunk.crs.unproject(e1)) - chunk.transform.matrix.inv().mulp(chunk.crs.unproject(e0))).norm()
		return scale
	except:
		return 1

def scale_transform_matrix(m, chunk_scale):
	new_mat = m.copy()
	for i in range(3):
		new_mat[3, i] *= chunk_scale
	return new_mat

def slerp(v1, v2, t):
	cos_omega = v1 * v2 / (v1.norm() * v2.norm())
	omega = math.acos(cos_omega) / 2.0
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
	for i in range(3):
		v1 = rgb_tr_matrix1.col(i).copy()
		v2 = rgb_tr_matrix2.col(i).copy()
		v = slerp(v1, v2, t)
		for j in range(3):
			result_matrix[j, i] = v[j]
	
	translate = lerp(rgb_tr_matrix1.col(3), rgb_tr_matrix2.col(3), t)
	for j in range(3):
		result_matrix[j, 3] = translate[j]
	
	return result_matrix * tv_to_rgb_matrix
