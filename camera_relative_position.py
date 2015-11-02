import PhotoScan as ps
import math

points_number = 8

def get_raw_picture_coords(pixel_point, focal_lengths, picture_sizes):
    tangent_x = picture_sizes[0] / (2.0 * focal_lengths[0])
    tangent_y = picture_sizes[1] / (2.0 * focal_lengths[1])
    x = ps.Vector([pixel_point[0] / focal_lengths[0] - tangent_x, pixel_point[1] / focal_lengths[1] - tangent_y, 1])
    return x

def det(l):
    n=l.size[0]
    if (n>2):
        i=1
        t=0
        sum=0
        while t<=n-1:
            d={}
            t1=1
            while t1<=n-1:
                m=0
                d[t1]=[]
                while m<=n-1:
                    if (m==t):
                        u=0
                    else:
                        d[t1].append(l[t1,m])
                    m+=1
                t1+=1
            l1 = ps.Matrix([d[x] for x in d])
            sum=sum+i*(l[0,t])*(det(l1))
            i=i*(-1)
            t+=1
        return sum
    elif n == 2:
        return (l[0,0]*l[1,1]-l[0,1]*l[1,0])
    else:
        return l[0,0]

def cofact(x):
    dim = x.size[0]
    
    fac = ps.Matrix([[0 for i in range(dim)] for j in range(dim)])
    b = ps.Matrix([[0 for i in range(dim - 1)] for j in range(dim - 1)])
     
    for q in range(dim):
        for p in range(dim):
            m=0;
            n=0;
            for i in range(dim):
                for j in range(dim):
                    if i != q and j != p:
                        b[m,n]= x[i,j]
                        if n < (dim-2):
                            n += 1
                        else:
                            n = 0
                            m += 1
            fac[q, p] = ((-1) ** (q+p)) * det(b)
    return trans(x, fac, dim)
    
def trans(x, fac, dim):
    d = det(x);
    y = x.copy()
    
    for i in range(dim):
        for j in range(dim):
            y[i,j]=fac[j,i]/d
     
    return y

def inv(m):
    d = det(m)
    if (d < 1e-20 and d > -1e-20):
        return None
        
    return cofact(m)

def get_matrix_norm(m):
    res = 0
    for a in m:
        res += a * a
    return res ** 0.5

def vector_mul(a, b):
    res = ps.Vector([0,0,0])
    for i in range(3):
        res[i] = (-1)**i * (a[(i + 1) % 3] * B[(i + 2) % 3] - a[(i + 2) % 3] * b[(i + 1) % 3])
    return res

def assemble_transform_matrix(R, T):
    res = ps.Matrix([[0]*4]*4)
    for i in range(3):
        for j in range(3):
            res[i,j] = R[i][j]
        res[i, 3] = T[i]
    res[3, 3] = 1
    
def get_transform_matrix(points_rgb, points_tv, focal_lengths_rgb, focal_lengths_tv, picture_sizes_rgb, picture_sizes_tv):
    x_rgb = [get_raw_picture_coords(points_rgb[i], focal_lengths_rgb, picture_sizes_rgb) for i in range(points_number)]
    x_tv = [get_raw_picture_coords(points_tv[i], focal_lengths_tv, picture_sizes_tv) for i in range(points_number)]
    
    print("x_rgb = " + str(x_rgb))
    
    dets = []
    q_ids = []
    Qs = []
    for identity_index in range(9):
        b = ps.Vector([0 for i in range(points_number)])
        X = ps.Matrix([[0 for i in range(points_number)]] * points_number)
        for i in range(points_number):
            offset = 0
            idx = 0
            for k in range(0, 3):
                for l in range(0, 3):
                    if (offset != identity_index):
                        X[i,idx] = x_rgb[i][l] * x_tv[i][k]
                        idx += 1
                    else:
                        b[i] = -x_rgb[i][l] * x_tv[i][k]
                    offset += 1
        dets.append(det(X))
        
        q = inv(X) * b
        Q = ps.Matrix([[0, 0, 0]] * 3)
        idx = 0
        offset = 0
        for i in range(3):
            for j in range(3):
                if offset != identity_index:
                    Q[i,j] = q[idx] 
                    idx += 1
                else:
                    Q[i,j] = 1 
                offset += 1
        Q2 = Q.t() * Q
        tr = 0
        for i in range(3):
            tr += Q2[i, i]
        q_id = (2.0 / float(tr)) ** 0.5
        for i in range(3):
            for j in range(3):
                Q[i,j] *= q_id
        Qs.append(Q)
        q_ids.append(q_id) # +- in fact
    
    min_mu = 1e200
    best_idx = -1
    mus = []
    for i in range(9):
        Q = Qs[i]
        inv_Q = inv(Q)
        if inv_Q is None:
            continue
        mu = get_matrix_norm(inv_Q) * get_matrix_norm(Q)
        mus.append(mu)
        if mu < min_mu:
            best_idx = i
    
    if best_idx == -1:
        print('All matrices have 0 det :(')
        return None
            
    print('mus = ' + str(mus))
    print('q_ids = ' + str(q_ids))
    print('dets = ' + str(dets))
    for i in range(4):
        Q = Qs[best_idx].copy()
        sign_q_id = i & 1
        sign_T1 = i & 2
        
        if sign_q_id == 1:
            Q *= -1
        Q2 = Q.t() * Q
        print(Q2)
        
        T = ps.Vector([((1 - Q2[j,j]) ** 0.5) for j in range(3)])
            
        if sign_T1 == 1:
            T[0] = -T[0]
        for j in range(1, 3):
            if T[0] * T[j] * Q2[j,0] < 0:
                T[j] = -T[j]  
       
        
        print("T = " + str(T))
        W = []
        for i in range(3):
            W.append(vector_mul(Q.row(i), T))
        R = []
        for i in range(3):
            R.append(vector_mul(W[(i + 1) % 3], W[(i + 2) % 3]) + w[i])
        
        fail = False
        for j in range(points_number):
            val = (R[0] - x_tv[0] * R[2]) * T / ((R[0] - x_tv[0] * R[2]) * x_rgb)
            if val < 0:
                fail = True
        if fail:
            print('failed with sighs: ' + str(i))
            continue
        else:
            return assemble_transform_matrix(R, T)
    return None

def scale_transform_matrix(m, distance_between_cameras_meters, chunk_scale):
    for i in range(3):
        m[3, i] *= (distance_between_cameras_meters * chunk_scale)
    return m
    
def main():
    m = ps.Matrix([[1,2], [3, 4]])
    print(det(m))
    print(inv(m))

#if __name__ == '__main__':
main()