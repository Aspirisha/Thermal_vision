import numpy as np
import cv2

def get_image_points(fname, inner_width, inner_height):
    print("processing " + fname)

    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (inner_width, inner_height), 
        cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_NORMALIZE_IMAGE)

    # If found, add object points, image points (after refining them)
    if ret == True:
        print("success with " + fname)

        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        img = cv2.drawChessboardCorners(img, (inner_width, inner_height), corners2,ret)
        cv2.imwrite(fname.split(".")[0] + "_out.jpeg", img );
        return corners2
    else:
        print("fail with " + fname) 
    return None  

def build_obj_points(inner_width, inner_height):
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((inner_height*inner_width,3), np.float32)
    objp[:,:2] = np.mgrid[0:inner_width,0:inner_height].T.reshape(-1,2)
    return objp

def get_image_size(fname):
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    return gray.shape[::-1]

def calibrate_camera(images, inner_width, inner_height):
    objp = build_obj_points(inner_width, inner_height)

    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.
    file_names = []

    for fname in images:
        corners = get_image_points(fname, inner_width, inner_height)
        if corners is not None:
            objpoints.append(objp)
            imgpoints.append(corners)
            file_names.append(fname)

    image_size = get_image_size(fname)

    return cv2.calibrateCamera(objpoints, imgpoints, image_size, None, distCoeffs = np.zeros(5), flags=cv2.CALIB_ZERO_TANGENT_DIST) + (imgpoints, objpoints, file_names)


def calibrate_rgb_and_tv(objpoints, img_points_rgb, img_points_tv, image_size,
                         rgb_camera_matrix, rgb_dist_coeffs, tv_camera_matrix, tv_dist_coeffs):
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # matrix will be FROM tv TO rgb
    object_points = [objpoints for i in range(len(img_points_rgb))]
    return cv2.stereoCalibrate(objectPoints=object_points, imagePoints2=img_points_rgb, imagePoints1=img_points_tv, imageSize=image_size, \
        cameraMatrix2=rgb_camera_matrix, distCoeffs2=rgb_dist_coeffs, cameraMatrix1=tv_camera_matrix, distCoeffs1=tv_dist_coeffs)