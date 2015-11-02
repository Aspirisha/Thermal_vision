import calibration as calib
import cv2
import numpy as np
import glob

# number of inner corners of chessboard we would like to match
inner_width=9
inner_height=5

def test():
    folder = 'chess_lenovo/'
    images = glob.glob(folder + 'ch*.jpg')
    ret, mtx, dist, rvecs, tvecs, img_points, objpoints, file_names = calib.calibrate_camera(images, inner_width, inner_height)

    img = cv2.imread(folder + 'ch1.jpg')
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    image_size = gray.shape[::-1]

    return ret, mtx, dist, rvecs, tvecs, img_points, objpoints, image_size
    retval, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F = calib.calibrate_rgb_and_tv([crp.objpoints[0]], [crp.img_points[0]], [crp.img_points[1]], crp.image_size, crp.mtx, crp.dist, crp.mtx, crp.dist)


def get_tv_to_rgb_matrix(rgb_calibration_file_names, tv_calibration_file_names, rgb_relative_file_names, tv_relative_file_names, calibration_images_with_this_names_as_relative = None):
    ret_rgb, mtx_rgb, dist_rgb, rvecs_rgb, tvecs_rgb, img_points_rgb, objpoints, used_rgb_files = calib.get_calibration_matrix(rgb_calibration_file_names)
    ret_tv, mtx_tv, dist_tv, rvecs_tv, tvecs_tv, img_points_tv, objpoints, used_tv_files = calib.get_calibration_matrix(tv_calibration_file_names)
    
    rgb_tv_corresponing_names = dict(zip(rgb_calibration_file_names, tv_calibration_file_names))
    rgb_files_to_points = dict(zip(used_rgb_files, img_points_rgb))
    tv_files_to_points = dict(zip(used_tv_files, img_points_tv))
    
    img = cv2.imread(rgb_file_names[0])
    image_size = img.shape[::-1]


    if calibration_images_with_this_names_as_relative is not None:
        temp_rgb_points = []
        temp_tv_points = []
        for rgb_file, rgb_img_points in zip(used_rgb_files, img_points_rgb):
            if rgb_file not in calibration_images_with_this_names_as_relative:
                continue
            temp_rgb_points.append(rgb_img_points)
            temp_tv_points.append(tv_files_to_points[rgb_tv_corresponing_names[rgb_file]])
        img_points_rgb = temp_rgb_points
        img_points_tv = temp_tv_points
    elif rgb_relative_file_names is not None:
        img_points_tv = []
        img_points_rgb = []
        for fname_rgb, fname_tv in zip(rgb_relative_file_names, tv_relative_file_names):
           img_points_rgb.append(get_image_points(fname_rgb, inner_width, inner_height))
           img_points_tv.append(get_image_points(fname_tv, inner_width, inner_height))
    else:
        pass

    retval, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F = calib.calibrate_rgb_and_tv(
        objpoints, img_points_rgb, img_points_tv, image_size, mtx_rgb, dist_rgb, mtx_tv, dist_tv)

    A = np.vstack((np.hstack((R, T[:, None])), [0, 0, 0 ,1]))
    return A

ret, mtx, dist, rvecs, tvecs, img_points, objpoints, image_size = test()