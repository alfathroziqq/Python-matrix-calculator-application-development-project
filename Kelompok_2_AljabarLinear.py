import numpy as np
import re
import math

def hitung_gauss_gaussjordan(A, b):
    n = len(A)
    
    for i in range(n):
        if A[i][i] == 0:
            return None
        
        for j in range(i+1, n):
            ratio = A[j][i]/A[i][i]
            
            for k in range(n):
                A[j][k] = A[j][k] - ratio * A[i][k]
            
            b[j] = b[j] - ratio * b[i]
    
    x = np.zeros(n)
    x[n-1] = b[n-1] / A[n-1][n-1]
    
    for i in range(n-2,-1,-1):
        x[i] = b[i]
        
        for j in range(i+1,n):
            x[i] = x[i] - A[i][j]*x[j]
        
        x[i] = x[i] / A[i][i]
    
    return x

def solve_gauss():
    print("\n-- SPL metode Gauss/Gauss Jordan --")
    n = int(input("Masukkan jumlah baris: "))
    m = int(input("Masukkan jumlah kolom: "))

    print("Masukkan koefisien matriks A (ukuran {}x{}):".format(n, m))
    A = []
    for _ in range(n):
        row = [float(x) for x in input().split()]
        A.append(row)
    A = np.array(A)

    print("\nMasukkan vektor b (ukuran {}):".format(n))
    b = np.array([float(x) for x in input().split()])

    solution = hitung_gauss_gaussjordan(A, b)

    if solution is None:
        print("\nHasil = Tidak ada solusi")
    elif solution == "Solusi tak terbatas":
        print("\nHasil = Solusi tak terbatas")
    else:
        print("\nHasil = Solusi unik:")
        for i, sol in enumerate(solution):
            print("x{} = {}".format(i+1, sol))
                
def masuk_persamaan(n):
    print("Masukkan Persamaan")
    print("xa+yb+zc+kd+=i", '\n')
    
    kiri_matrix = []  
    kanan_matrix = []  
    variables = set()

    for _ in range(n):
        equation = input("Persamaan ke-{}: ".format(_ + 1))

        equation = equation.replace(" ", "").split("=")
        kiri = equation[0]
        kiri_terms = re.split(r"([+-])", kiri)  
        kiri_coefficients = []
        for term in kiri_terms:
            if term != "+" and term != "-":
                coefficient = term[:-1]  
                if coefficient == "":
                    coefficient = "1"  
                kiri_coefficients.append(float(coefficient))
                variable = term[-1]
                variables.add(variable)
        kiri_matrix.append(kiri_coefficients)
        kanan = float(equation[1])
        kanan_matrix.append(kanan)

    kiri_matrix = np.array(kiri_matrix)
    kanan_matrix = np.array(kanan_matrix)
    variables = np.sort(np.array(list(variables)))
    return kiri_matrix, kanan_matrix, variables

def determine_solution(matrix1, matrix2):
    baris, kolom = matrix1.shape
    if baris != kolom:
        return "\nHasil = Tidak ada solusi"
    a = np.linalg.det(matrix1)
    if a != 0:
        return "\nHasil = Solusi unik"
    matrix_aug = np.hstack((matrix1, matrix2.reshape(-1, 1)))
    matrix_ref = np.linalg.matrix_rank(matrix_aug)

    if matrix_ref < np.linalg.matrix_rank(matrix1):
        return "\nHasil = Tidak ada solusi"

    elif matrix_ref < kolom:
        return "\nHasil = Solusi tak terbatas"
    else:
        return "\nHasil = Solusi unik"

def spl_variables():
    print("\n-- SPL dengan Variabel --")    
    n = int(input("Masukkan jumlah persamaan: "))
    matrix1, matrix2, c = masuk_persamaan(n)

    solution = determine_solution(matrix1, matrix2)
    print("Solusi: {}".format(solution))

    if solution == "\nHasil = Solusi unik":
        x = np.linalg.solve(matrix1, matrix2)
        for index in range(len(c)):
            hasil = "{} = {}".format(c[index], x[index])
            print(hasil)
            
def matriks_diagonal():
    print("\n-- Matriks Diagonal --")
    n = int(input("Masukkan jumlah baris: "))
    m = int(input("Masukkan jumlah kolom: "))

    print("Masukkan koefisien matriks A (ukuran {}x{}):".format(n, m))
    A = []
    for _ in range(n):
        row = [float(x) for x in input().split()]
        A.append(row)
    A = np.array(A)

    eigenvalues, eigenvectors = np.linalg.eig(A)
    poly_char = np.poly(eigenvalues)
    diagonal_matrix = np.diag(eigenvalues)
    inverse_eigenvectors = np.linalg.inv(eigenvectors)
    diagonalized_matrix = np.matmul(np.matmul(eigenvectors, diagonal_matrix), inverse_eigenvectors)

    print("\nPolinomial Karakteristik:")
    print(poly_char)
    print("\nEigenvalues:")
    print(eigenvalues)
    print("\nEigenvector (P):")
    print(eigenvectors)
    print("\nD:")
    print(diagonal_matrix)
    print("\nP^-1:")
    print(inverse_eigenvectors)

def svd():
    print("\n-- Singular Value Decomposition --")
    n = int(input("Masukkan jumlah baris: "))
    m = int(input("Masukkan jumlah kolom: "))

    print("Masukkan koefisien matriks A (ukuran {}x{}):".format(n, m))
    A = []
    for _ in range(n):
        row = [float(x) for x in input().split()]
        A.append(row)
    A = np.array(A)
    
    u, s, vh = np.linalg.svd(A)

    print("\nMatriks U:")
    print(u)
    print("\nMatriks S:")
    print(np.diag(s))
    print("\nMatriks Vh:")
    print(vh)

def hitung_complex(persamaan, variabel):
    matrix1 = np.zeros((persamaan, variabel), dtype=complex)
    matrix2 = np.zeros(persamaan, dtype=complex)
    eqVariable = set()

    print("\nMasukkan persamaan-persamaan:")
    for i in range(persamaan):
        persamaan = input(f"Persamaan {i+1}: ")
        persamaan = re.sub(r'([a-z])', r'1j*\1', persamaan) 
        koefisien = re.findall(r'[+-]?\d+\.?\d*|\d*\.?\d+[j]', persamaan)
        for j in range(variabel):
            matrix1[i, j] = complex(koefisien[j])
        matrix2[i] = complex(koefisien[-1])
        variables = re.findall(r'[a-z]', persamaan)
        eqVariable.update(variables)

    eqVariable = sorted(list(eqVariable))

    return matrix1, matrix2, eqVariable

def round_complex(complex_number, digit):
    real = math.ceil(complex_number.real * (10 ** digit)) / (10 ** digit)
    imag = math.ceil(complex_number.imag * (10 ** digit)) / (10 ** digit)
    return complex(real, imag)
    
def spl_complex():
    print("\n-- SPL kompleks dengan SVD --")
    n = int(input("Masukkan jumlah persamaan: "))
    m = int(input("Masukkan jumlah variabel : "))
    
    matrix1, matrix2, c = hitung_complex(n, m)
    U, s, Vh = np.linalg.svd(matrix1)
    s_inv = np.zeros_like(matrix1.T, dtype=complex)
    s_inv[:s.size, :s.size] = np.diag(1 / s)
    x = Vh.T @ s_inv @ U.T @ matrix2

    print("\nHasil")
    for i in range(m):
            round = round_complex(x[i], 3)
            print(f"x{i+1} = {round}") 

while True:
    print("\n------- PROGRAM KALKULATOR MATRIX -------")
    print("Menu:")
    print("1. Mencari SPL metode Gauss/Gauss Jordan")
    print("2. Mencari SPL dengan Variabel")
    print("3. Mencari Diagonalisasi Matriks")
    print("4. Mencari SVD (Singular Value Decomposition)")
    print("5. Mencari SPL kompleks dengan SVD")
    print("0. Keluar")
    menu = int(input("Pilihan Anda: "))

    if menu == 1:
        solve_gauss()
    elif menu == 2:
        spl_variables()
    elif menu == 3:
        matriks_diagonal()
    elif menu == 4:
        svd()
    elif menu == 5:
        spl_complex()
    elif menu == 0:
        break
    else:
        print("Pilih sesuai angka tertera")