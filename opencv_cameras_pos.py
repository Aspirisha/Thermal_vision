import cv2
import math
import numpy as np
from matplotlib import pyplot as plt

def drawlines(img1,img2,lines,pts1,pts2):
    ''' img1 - image on which we draw the epilines for the points in img2
        lines - corresponding epilines '''
    r,c = img1.shape
    img1 = cv2.cvtColor(img1,cv2.COLOR_GRAY2BGR)
    img2 = cv2.cvtColor(img2,cv2.COLOR_GRAY2BGR)
    for r,pt1,pt2 in zip(lines,pts1,pts2):
        color = tuple(np.random.randint(0,255,3).tolist())
        x0,y0 = map(int, [0, -r[2]/r[1] ])
        x1,y1 = map(int, [c, -(r[2]+r[0]*c)/r[1] ])
        img1 = cv2.line(img1, (x0,y0), (x1,y1), color,1)
        img1 = cv2.circle(img1,tuple(pt1),5,color,-1)
        img2 = cv2.circle(img2,tuple(pt2),5,color,-1)
    return img1,img2

img1 = cv2.imread('1.jpg',0)  #queryimage # left image
img2 = cv2.imread('2.jpg',0) #trainimage # right image
'''
sift = cv2.xfeatures2d.SIFT_create()

# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)

# FLANN parameters
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks=50)

print ('****START***')
# create BFMatcher object
bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)

print ('****A***')
# Match descriptors.
matches = bf.match(des1,des2)

print ('****B***')

good = []
pts1 = []
pts2 = []

# ratio test as per Lowe's paper
for m in matches:
   print (m.distance)
   if m.distance < 50:
       good.append(m)
       pts2.append(kp2[m.trainIdx].pt)
       pts1.append(kp1[m.queryIdx].pt)

pts1 = np.int32(pts1)
pts2 = np.int32(pts2)
print(pts1[:10])
print(pts2[:10])'''

pts1 = np.array([[2346, 1270], [2134, 756], [962, 1623], [1383, 791], [3110, 910], [1893, 1264], [966, 1220], [2133, 1382], [950, 790], [1783, 783], [1814, 1292], [1324, 905], [1666, 662]])
pts2 = np.array([[3450, 1447], [1976, 634], [796, 2212], [976, 724], [3464, 788], [1856, 1352], [772, 1533], [2618, 1544],  [60, 741],  [1787, 698], [1557, 1367], [646, 874], [1133, 512]])

pts1 = np.int32(pts1)
pts2 = np.int32(pts2)

F, mask = cv2.findFundamentalMat(pts1,pts2,cv2.FM_8POINT)

# We select only inlier points
pts1 = pts1[mask.ravel()==1]
pts2 = pts2[mask.ravel()==1]



print(F)

print(mask)

#exit(0)

# Find epilines corresponding to points in right image (second image) and
# drawing its lines on left image
lines1 = cv2.computeCorrespondEpilines(pts2.reshape(-1,1,2), 2,F)
lines1 = lines1.reshape(-1,3)
img5,img6 = drawlines(img1,img2,lines1,pts1,pts2)

# Find epilines corresponding to points in left image (first image) and
# drawing its lines on right image
lines2 = cv2.computeCorrespondEpilines(pts1.reshape(-1,1,2), 1,F)
lines2 = lines2.reshape(-1,3)
img3,img4 = drawlines(img2,img1,lines2,pts2,pts1)

plt.subplot(121),plt.imshow(img5)
plt.subplot(122),plt.imshow(img3)
#plt.show()

def vector_mul(a, b):
    print a
    #print b
    res = np.array([0,0,0])
    for i in range(3):
        res[i] = (-1)**i * (a[(i + 1) % 3] * b[(i + 2) % 3] - a[(i + 2) % 3] * b[(i + 1) % 3])
    return res

def assemble_transform_matrix(R, T):
    res = np.ndarray([[0]*4]*4)
    for i in range(3):
        for j in range(3):
            res[i,j] = R[i][j]
        res[i, 3] = T[i]
    res[3, 3] = 1

def get_transition_marix(E, x_rgb, x_tv):
    for i in range(4):
        Q = np.copy(E)
        sign_q_id = i & 1
        sign_T1 = i & 2
        
        if sign_q_id == 1:
            Q *= -1
        Q2 = np.transpose(Q) * Q
        print(Q2)
        
        dist = ((Q2[0, 0] + Q2[1, 1] + Q2[2, 2]) / 2 ) **0.5
        print dist**2

        T = np.array([((math.fabs(dist ** 2 - Q2[j,j])) ** 0.5) for j in range(3)])
            
        if sign_T1 == 1:
            T[0] = -T[0]
        for j in range(1, 3):
            if T[0] * T[j] * Q2[j,0] < 0:
                T[j] = -T[j]  
       
        
        print("T = " + str(T))
        W = []
        for i in range(3):
            W.append(vector_mul(Q[i, :], T))
        R = []
        for i in range(3):
            R.append(vector_mul(W[(i + 1) % 3], W[(i + 2) % 3]) + W[i])
        
        fail = False
        for j in range(points_number):
            val = np.dot((R[0] - x_tv[0] * R[2]), T) / np.dot((R[0] - x_tv[0] * R[2]), x_rgb)
            if val < 0:
                fail = True
        if fail:
            print('failed with sighs: ' + str(i))
            continue
        else:
            return assemble_transform_matrix(R, T)
    return None


#matrix = get_transition_marix(F, pts1, pts2)

#print(matrix)

u = np.array([2968, 737, 1])
v = np.array([3275, 578, 1])
r = np.array([2368, 737, 1])

x = np.array([2134, 756, 1])
y = np.array([1976, 634, 1])
print(np.dot(np.dot(u, F), v))
print(np.dot(np.dot(v, F), u))
print(np.dot(np.dot(y, F), x))

print("points:")
for i in range(8):
    p1 = pts1[i]
    p2 = pts2[i]
    x = np.array([p1[0], p1[1], 1])
    y = np.array([p2[0], p2[1], 1])
    print(np.dot(np.dot(y, F), x))