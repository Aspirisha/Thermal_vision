import calibration as calib
import cv2
import numpy as np
import glob
import json
import sys
from argparse import ArgumentParser
from PySide import QtCore, QtGui
from functools import partial

# number of inner corners of chessboard we would like to match

def get_tv_to_rgb_matrix(
    rgb_calibration_file_names, tv_calibration_file_names, rgb_relative_file_names,
        tv_relative_file_names, chessboard_cell_width_meters, inner_width, inner_height,
        on_calibrated_signal=None):

    ret_rgb, mtx_rgb, dist_rgb, rvecs_rgb, tvecs_rgb, img_points_rgb, objpoints, used_rgb_files = \
        calib.calibrate_camera(
            rgb_calibration_file_names, inner_width, inner_height, on_calibrated_signal)

    ret_tv, mtx_tv, dist_tv, rvecs_tv, tvecs_tv, img_points_tv, objpoints, used_tv_files = \
        calib.calibrate_camera(
            tv_calibration_file_names, inner_width, inner_height, on_calibrated_signal)

    if rgb_calibration_file_names is not None:
        image_size = calib.get_image_size(rgb_calibration_file_names[0])
    else:
        image_size = calib.get_image_size(rgb_relative_file_names[0])

    objpoints = calib.build_obj_points(inner_width, inner_height)

    solo_calibrated_points_tv = img_points_tv
    solo_calibrated_points_rgb = img_points_rgb
    img_points_tv = []
    img_points_rgb = []
    for fname_rgb, fname_tv in zip(rgb_relative_file_names, tv_relative_file_names):
        tv_points = solo_calibrated_points_tv[
            tv_calibration_file_names.index(fname_tv)]
        rgb_points = solo_calibrated_points_rgb[
            rgb_calibration_file_names.index(fname_rgb)]
        # rgb_points = calib.get_image_points(fname_rgb, inner_width, inner_height)
        # tv_points = calib.get_image_points(fname_tv, inner_width,
        # inner_height)

        if (rgb_points is not None and tv_points is not None):
            img_points_rgb.append(rgb_points)
            img_points_tv.append(tv_points)

    if len(img_points_rgb) == 0:
        print("Considered photos can't be used to determine relative position")
        return None

    retval, cameraMatrix1, distCoeffs1, cameraMatrix2, \
        distCoeffs2, R, T, E, F = calib.calibrate_rgb_and_tv(
            objpoints, img_points_rgb,
            img_points_tv, image_size, mtx_rgb, dist_rgb, mtx_tv, dist_tv)

    T *= chessboard_cell_width_meters  # now translations is in meters

    A = np.append(np.append(R, T, axis=1), np.array([[0, 0, 0, 1]]), axis=0)
    return A, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2


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


def run_calibration(rgb_images, tv_images, rgb_relative, tv_relative, cell_size, inner_width, inner_height,
                    on_calibrated_signal=None):
    A, cameraMatrix_tv, distCoeffs_tv, cameraMatrix_rgb, distCoeffs_rgb = \
        get_tv_to_rgb_matrix(rgb_images, tv_images, rgb_relative, tv_relative, cell_size, inner_width,
                inner_height, on_calibrated_signal)
    tv_image_width, tv_image_height = calib.get_image_size(tv_images[0])
    return tv_image_width, tv_image_height, \
        A, cameraMatrix_tv, distCoeffs_tv, cameraMatrix_rgb, distCoeffs_rgb


def dump_calibration_results(save_file, tv_image_width, tv_image_height,
                             A, cameraMatrix_tv, distCoeffs_tv, cameraMatrix_rgb, distCoeffs_rgb):
    with open(save_file, "w") as f:
        json.dump(cameraMatrix_rgb.tolist(), f)
        f.write('\n')
        json.dump(distCoeffs_rgb.tolist(), f)
        f.write('\n')
        json.dump(cameraMatrix_tv.tolist(), f)
        f.write('\n')
        json.dump(distCoeffs_tv.tolist(), f)
        f.write('\n')
        json.dump(A.tolist(), f)
        f.write('\n')
        json.dump([tv_image_width, tv_image_height], f)


def main(config_file=None, save_file=None):
    if config_file is None or save_file is None:
        parser = ArgumentParser()
        parser.add_argument('-c', '--config', action='store', type=str,
                            dest='config_file', help='Calibration configuration file')
        parser.add_argument('-s', '--save-file', action='store', type=str,
                            dest='save_file', help='File to save calibration results')
        args = parser.parse_args()
        config_file = args.config_file
        save_file = args.save_file

    with open(config_file, 'r') as f:
        rgb_images = read_images(f)
        tv_images = read_images(f)
        cell_size = float(f.readline().strip('\n'))

        s = f.readline()
        corners_rows, corners_cols = [int(x) for x in s.split(" ")]
        rgb_relative, tv_relative = read_pairs(f)

    res = run_calibration(rgb_images, tv_images, rgb_relative, tv_relative, cell_size, corners_rows,
                          corners_cols)
    dump_calibration_results(save_file, *res)


class CalibratorThread(QtCore.QThread):
    update_progress = QtCore.Signal(int)

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.config_file = None
        self.save_file = None
        self.calibrated_images = 0
        self.corners_number = None
        self.cell_size = None
        self.tv_images = None
        self.rgb_images = None
        self.rgb_relative = None
        self.tv_relative = None
        self.images_to_calibrate = None
        self.corners_rows = 9
        self.corners_cols = 5
        self.percent_per_image = 100

    def reset(self, config_file, save_file):
        self.config_file = config_file
        self.save_file = save_file
        self.calibrated_images = 0

        with open(config_file, 'r') as f:
            self.rgb_images = read_images(f)
            self.tv_images = read_images(f)
            self.cell_size = float(f.readline().strip('\n'))
            self.corners_rows, self.corners_cols = [int(x) for x in f.readline().split(" ")]
            self.rgb_relative, self.tv_relative = read_pairs(f)
            self.images_to_calibrate = len(
                self.rgb_images) + len(self.tv_images)
            self.percent_per_image = 100.0 / self.images_to_calibrate

    def on_image_calibrated(self, success):
        self.calibrated_images += 1
        self.update_progress.emit(
            int(self.calibrated_images * self.percent_per_image))

    def run(self):
        res = run_calibration(
            self.rgb_images, self.tv_images, self.rgb_relative,
            self.tv_relative, self.cell_size, self.corners_rows, self.corners_cols,
            partial(CalibratorThread.on_image_calibrated, self))
        dump_calibration_results(self.save_file, *res)


if __name__ == '__main__':
    main()
