import calibration as calib
import cv2
import numpy as np
import glob

def test():
    folder = 'chess_lenovo/'
    images = glob.glob(folder + 'ch*.jpg')
    ret, mtx, dist, rvecs, tvecs, img_points, objpoints = calib.get_calibration_matrix(images)

    img = cv2.imread(folder + 'ch1.jpg')
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    image_size = gray.shape[::-1]
    print("img.shape is ")
    print(gray.shape)
    print('img size is ')
    print(image_size)

    return ret, mtx, dist, rvecs, tvecs, img_points, objpoints, image_size
   # retval, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F = calib.calibrate_rgb_and_tv(
   #     objpoints, [img_points[0]], [img_points[1]], image_size, mtx, dist, mtx, dist)

    #print("R = ")
    #print(R)

    #print("T = ")
    #print(T)


def get_tv_to_rgb_matrix():
    images = glob.glob('rgb*.jpg')
    ret_rgb, mtx_rgb, dist_rgb, rvecs_rgb, tvecs_rgb, img_points_rgb, objpoints = calib.get_calibration_matrix(images)

    images = glob.glob('tv*.jpg')
    ret_tv, mtx_tv, dist_tv, rvecs_tv, tvecs_tv, img_points_tv, objpoints = calib.get_calibration_matrix(images)
    
    img_rgb = glob.glob('rgb1.jpg')
    img_tv = glob.glob('tv1.jpg')

    img = cv2.imread(img_rgb)
    image_size = img.shape[::-1]

    retval, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F = calib.calibrate_rgb_and_tv(
        objpoints, img_points_rgb, img_points_tv, image_size, mtx_rgb, dist_rgb, mtx_tv, dist_tv)

ret, mtx, dist, rvecs, tvecs, img_points, objpoints, image_size = test()