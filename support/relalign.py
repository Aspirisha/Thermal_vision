import PhotoScan
import copy
import math

DISTANCE_EPS = 1e-5


def get_photo_matching_by_file(matching_file):
    matching = {}
    with open(matching_file) as f:
        for s in f:
            rgb_photo, tv_photo = s.split(' ')
            matching[rgb_photo] = tv_photo.strip()

    return matching


def get_photo_matching_by_location():
    doc = PhotoScan.app.document
    matching = {}
    for c1 in doc.chunk.camers:
        if c1.transform is None:
            continue
        for c2 in doc.chunk.cameras:
            if c1 == c2:
                continue
            delta = c1.reference.location - c2.reference.location
            dist = delta.norm()
            if dist < DISTANCE_EPS:
                matching[c1.label] = c2.label
    return matching

def perform_relative_alignment(tv_to_rgb_matrix, photo_matching_file, calibration_file):
    camera_name_to_index = {}
    doc = PhotoScan.app.document

    for idx, c in enumerate(doc.chunk.cameras):
        camera_name_to_index[c.label] = idx

    for c in doc.chunk.cameras:
        c.enabled = False

    chunk_scale = get_chunk_scale(doc.chunk)
    tv_to_rgb_matrix = scale_transform_matrix(tv_to_rgb_matrix, chunk_scale)

    rgb_to_tv_matching = get_photo_matching_by_location() if photo_matching_file is None \
        else get_photo_matching_by_file(photo_matching_file)

    print(rgb_to_tv_matching)
    # apply calibration to cameras sensor
    # we can take any camera!
    tv_camera = None
    for name, index in camera_name_to_index.items():
        if name in rgb_to_tv_matching.values():
            tv_camera = doc.chunk.cameras[index]
            break

    if tv_camera is None:
        print('No satisfying unaligned cameras found')
        return

    new_calibration = PhotoScan.Calibration()
    new_calibration.load(calibration_file) # /home/plaz/calib.xml
    tv_camera.sensor.calibration = new_calibration

    for rgb_photo, tv_photo in rgb_to_tv_matching.items():
        idx_tv = camera_name_to_index.get(tv_photo)
        idx_rgb = camera_name_to_index.get(rgb_photo)

        if idx_tv is None or idx_rgb is None:
            continue

        rgb_tr_matrix = doc.chunk.cameras[idx_rgb].transform

        if not rgb_tr_matrix:
            continue

        tr_mat = get_transfom_matrix_for_tv(rgb_tr_matrix, tv_to_rgb_matrix)
        tv_camera = doc.chunk.cameras[camera_name_to_index[tv_photo]]
        tv_camera.transform = tr_mat
        tv_camera.enabled = True


# returns scale. If we multiply it by distance in real world (meters), we get 
# distance in chunk crs (or, equally, in camera crs for they have same scale) 
def get_chunk_scale(chunk):
    e0 = PhotoScan.Vector([0, 0, 0])
    e1 = PhotoScan.Vector([0, 0, 1])
    try:
        scale = (chunk.transform.matrix.inv().mulp(chunk.crs.unproject(e1)) - chunk.transform.matrix.inv().mulp(chunk.crs.unproject(e0))).norm()
        return scale
    except:
        return 0.4

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
def get_transfom_matrix_for_tv(rgb_tr_matrix, tv_to_rgb_matrix):
    return rgb_tr_matrix * tv_to_rgb_matrix
