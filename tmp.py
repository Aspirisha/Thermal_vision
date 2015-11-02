ans = 0
for i in range(0, 11):
    for j in range(0, 6):
        for k in range (0, 4):
            for l in range(0, 3):
                if i + j*2 + k*3 + l*5 == 10:
                    ans += 1
                    print ("n = 1*" + str(i) + "+ 2*" + str(j) + "+ 3*" + str(k) + "+ 5*" + str(l))
print (ans)