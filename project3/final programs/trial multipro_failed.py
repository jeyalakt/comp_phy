from numpy import *
import time as time
import sys
import matplotlib.pyplot as plt
from scipy.stats import uniform
from random import random
from random import seed
import multiprocessing as mp

# monte carlo brute force method using uniform distribution
tol = 1e-10
outf = open('improved_montecarlo_expon_samp.txt', 'w+')
outf.write("n \t a\t  MC_expon_samp_result\t exact_result\t realtive error\t sigma\t exe time_MC_expon samp\n")
outf.close()


def Integrand(u1, u2, theta1, theta2, phi1, phi2):
    # print(u1,u2,theta1,theta2,phi1,phi2)
    cos_val = (cos(theta1) * cos(theta2) + sin(theta1) * sin(theta2) * cos(phi1 - phi2))
    sq = abs((u1 * u1) + (u2 * u2) - (2.0 * u1 * u2 * cos_val))
    # print (sq)
    r1r2 = sqrt(sq)
    fvalue = u1 * u1 * u2 * u2 * sin(theta1) * sin(theta2) / r1r2

    # print("r1r2",r1r2)
    epsil = 1.0E-8
    if (r1r2 <= epsil):
        q.put(0)
    # return 0
    else:
        q.put(np.exp(-2 * alpha * (r1 + r2)) / r1r2)
        # return fvalue


def iteration(n):
    for j in range(n):
        # seed(1)
        xx1 = random()
        xx2 = random()
        x1 = -0.25 * log(1 - xx1)
        x2 = -0.25 * log(1 - xx2)
        t1 = random() * M_PI
        t2 = random() * M_PI
        p1 = random() * 2 * M_PI
        p2 = random() * 2 * M_PI

        func_res = Integrand(x1, x2, t1, t2, p1, p2);
        return func_res

        # print(x1,y1,z1,x2,y2,z2)
        # func_res=func_6D(x1,y1,z1,x2,y2,z2)
        int_MC = int_MC + func_res
        # print("int mc",int_MC)
        sum_sigma += func_res * func_res


if __name__ == '__main__':
    mp.set_start_method('spawn')
    MC_start_time = time.time()
    # A=[100000,1000000,10000000]
    A = [100]
    for i in range(len(A)):
        n = A[i]
        a = -1
        # b=1
        # d=6
        int_MC = 0
        sum_sigma = 0
        sigma = 0
        func_res = 0
        M_PI = 3.14159265359
        jacobi_det = (4 * (M_PI ** 4)) / 16
        # exact_integral=5*3.14*3.14/256
        MC_start_time = time.time()
        q = mp.Queue()
        p = mp.Process(target=iteration, args=(n, q))
        p.start()
        func_res = (q.get())

        MC_finish_time = time.time()
        MC_exe_time = MC_finish_time - MC_start_time
        # print("MC exe time", MC_exe_time)
        # print("int_MC")
        # print(int_MC)
        int_MC /= n
        sum_sigma = (sum_sigma / n)
        variance = sum_sigma - int_MC * int_MC
        int_MC *= jacobi_det
        sigma = jacobi_det * sqrt(variance / n)
        std = sqrt(sigma) / sqrt(n)
        exact_integral = 5 * 3.14 * 3.14 / 256
        relative_error = abs(int_MC - exact_integral) / exact_integral;
        print("int_MC")
        print(int_MC)

        # print("exact integral")
        # print(exact_integral)

        print("relatative_error")
        print(relative_error)

        outf = open('improved_montecarlo_expon_samp.txt', 'a')
        outf.write(str(n))
        outf.write("\t")
        outf.write(str(a))
        outf.write("\t")
        outf.write("{:.6f}".format(int_MC))
        outf.write("\t")
        outf.write("{:.6f}".format(exact_integral))
        outf.write("\t")
        outf.write("{:.6f}".format(relative_error))
        outf.write("\t")
        outf.write("{:.6f}".format(sigma))
        outf.write("\t")
        outf.write("{:.6f}".format(MC_exe_time))
        outf.write("\n")
        outf.close()
