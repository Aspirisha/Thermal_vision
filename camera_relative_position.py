import calibration as calib
import cv2
import numpy as np
import glob
import json
import sys
from argparse import ArgumentParser

# number of inner corners of chessboard we would like to match
inner_width=9
inner_height=5

def test():
    folder = 'chess_lenovo/'
    rgb_images = glob.glob(folder + 'ch*.jpg')
    tv_images = glob.glob(folder + 'ch*.jpg')
    
    folder = "lenovo_offset_20cm/"
    rgb_relative_file_names = glob.glob(folder + 'ch1.jpg')
    tv_relative_file_names = glob.glob(folder + 'ch2.jpg')

    return get_tv_to_rgb_matrix(rgb_images, tv_images, rgb_relative_file_names, tv_relative_file_names,0.027)[0]

def get_tv_to_rgb_matrix(rgb_calibration_file_names, tv_calibration_file_names, rgb_relative_file_names, 
    tv_relative_file_names, chessboard_cell_width_meters, rgb_camera_matrix = None, rgb_camera_dist = None, tv_camera_matrix = None, tv_camera_dist = None, 
    calibration_rgb_images_with_this_names_as_relative = None):
    
    if rgb_camera_matrix is None or rgb_camera_dist is None or calibration_rgb_images_with_this_names_as_relative is not None:
        ret_rgb, mtx_rgb, dist_rgb, rvecs_rgb, tvecs_rgb, img_points_rgb, objpoints, used_rgb_files = calib.calibrate_camera(rgb_calibration_file_names, inner_width, inner_height)
    
    if tv_camera_matrix is None or tv_camera_dist is None or calibration_rgb_images_with_this_names_as_relative is not None:
        ret_tv, mtx_tv, dist_tv, rvecs_tv, tvecs_tv, img_points_tv, objpoints, used_tv_files = calib.calibrate_camera(tv_calibration_file_names, inner_width, inner_height)
    
    rgb_tv_corresponing_names = dict(zip(rgb_calibration_file_names, tv_calibration_file_names))
    rgb_files_to_points = dict(zip(used_rgb_files, img_points_rgb))
    tv_files_to_points = dict(zip(used_tv_files, img_points_tv))
    
    if rgb_calibration_file_names is not None:
        image_size = calib.get_image_size(rgb_calibration_file_names[0])
    else:
        image_size = calib.get_image_size(rgb_relative_file_names[0])

    objpoints = calib.build_obj_points(inner_width, inner_height)

    if calibration_rgb_images_with_this_names_as_relative is not None:
        temp_rgb_points = []
        temp_tv_points = []
        for rgb_file, rgb_img_points in zip(used_rgb_files, img_points_rgb):
            if rgb_file not in calibration_rgb_images_with_this_names_as_relative:
                continue
            temp_rgb_points.append(rgb_img_points)
            temp_tv_points.append(tv_files_to_points[rgb_tv_corresponing_names[rgb_file]])
        img_points_rgb = temp_rgb_points
        img_points_tv = temp_tv_points
    elif rgb_relative_file_names is not None:
        img_points_tv = []
        img_points_rgb = []
        for fname_rgb, fname_tv in zip(rgb_relative_file_names, tv_relative_file_names):
           img_points_rgb.append(calib.get_image_points(fname_rgb, inner_width, inner_height))
           img_points_tv.append(calib.get_image_points(fname_tv, inner_width, inner_height))
    else:
        print("Error: ")
        pass

    #return objpoints, img_points_rgb, img_points_tv, image_size, mtx_rgb, dist_rgb, mtx_tv, dist_tv

    retval, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F = calib.calibrate_rgb_and_tv([objpoints], img_points_rgb, img_points_tv, image_size, mtx_rgb, dist_rgb, mtx_tv, dist_tv)

    T *= chessboard_cell_width_meters # now translations is in meters

    A = np.append(np.append(R, T, axis=1), np.array([[0, 0, 0, 1]]), axis=0)
    return A, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2

#ret, mtx, dist, rvecs, tvecs, img_points, objpoints, image_size = test()
def read_images(f):
    img_num = int(f.readline().strip('\n'))
    images = []
    for i in range(img_num):
        images.append(f.readline().strip('\n'))
    return images

def read_pairs(f):
    pairs_num = int(f.readline().strip('\n'))
    imgs1 = []
    imgs2 = []
    for i in range(pairs_num):
        imgs1.append(f.readline().strip('\n'))
        imgs2.append(f.readline().strip('\n'))
    return imgs1, imgs2

def main():
    import os

    print(os.getcwd())
    
    parser = ArgumentParser()
    parser.add_argument('-c', '--config', action='store', type=str, dest='config_file', help='Calibration configuration file')
    parser.add_argument('-s', '--save-file', action='store', type=str, dest='save_file', help='File to save calibration results')
    args = parser.parse_args()

    f = open(args.config_file, 'r')

    rgb_images = read_images(f)
    tv_images = read_images(f)
    cell_size = float(f.readline().strip('\n'))
    rgb_relative, tv_relative = read_pairs(f)
    f.close()

    A, cameraMatrix_rgb, distCoeffs_rgb, cameraMatrix_tv, distCoeffs_tv = get_tv_to_rgb_matrix(rgb_images, tv_images, rgb_relative, tv_relative, cell_size)
    f = open(args.save_file, "w")

    json.dump(cameraMatrix_rgb.tolist(), f)
    f.write('\n')
    print('TYPE: ')
    print(type(distCoeffs_rgb))
    json.dump(distCoeffs_rgb.tolist(), f)
    f.write('\n')
    json.dump(cameraMatrix_tv.tolist(), f)
    f.write('\n')
    json.dump(distCoeffs_tv.tolist(), f)
    f.write('\n')
    json.dump(A.tolist(), f)

    f.close()

if __name__ == '__main__':
    main()