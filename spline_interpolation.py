import numpy as np


def _interpolated_polynomial_value(vx: [], x: int, i: int, xi: int, ) -> int:
    """
    :param vx: result vector
    :param x: current x
    :param i: index
    :param xi: x from given index
    :return: value of polynomial: ai + bi(x - xi) + ci(x - xi)^2 + di(x - xi)^3
    """
    return vx[4 * i] + vx[4 * i + 1] * (x - xi) + vx[4 * i + 2] * ((x - xi) ** 2) + vx[4 * i + 3] * ((x - xi) ** 3)


def _create_vector_b(y: [], size_n: int):
    """
    Create vector with half 0 values and half y values
    :param y: values of given interpolation points
    :param size_n: number of spline functions
    :return: vector_b = [y[0], y[1], y[1], y[2], y[2], ..., y[n-1], y[n-1], y[n], 0, ... 0]
    """
    vector_b = [0] * size_n * 4

    # Calc vector_b = [y0, y1, y1, y2, y2, ..., y(n-1), y(n-1), yn, 0, ... 0]
    for i in range(size_n):
        vector_b[2 * i] = y[i]
        vector_b[2 * i + 1] = y[i + 1]

    return vector_b


def _create_matrix(h: float, size_n: int):
    """
    Fill matrix with values defined by below formulas:
    1) S_i(x[i]) = f(x[i])              ⮕   a[i] = y[i]
    2) S_i(x[i+1]) = f(x[i+1])          ⮕   a[i] + h*b[i] + h^2*c[i] + h^3*d[i] = y[i+1]
    3) S_i`(x[i+1]) = S_i`(x[i+1])      ⮕   b[i] + 2h*c[i] + 3h^2*d[i] - b[i+1] = 0
    4) S_i``(x[i+1]) = S_i+1``(x[i+1])  ⮕   2c[i] + 6h*d[i] - c[i+1] = 0
    5) S_0``(x[0]) = 0                  ⮕   2c[0] = 0
    6) S_n-1``(x[n]) = 0                ⮕   2c[n-1] + 6h*d[n-1] = 0

    :param h: difference between x and x + 1
    :param size_n: number of spline functions
    :return: filled matrix
    """
    matrix_a = np.zeros((size_n * 4, size_n * 4))  # define matrix A filled with zeros

    for i in range(size_n):
        row = i * 2  # for first half of matrix
        row2 = (i + size_n) * 2  # for second half of matrix
        a_i_0, b_i_0, c_i_0, d_i_0 = 4 * i, 4 * i + 1, 4 * i + 2, 4 * i + 3  # indexes: i
        a_i_1, b_i_1, c_i_1, d_i_1 = 4 * (i + 1), 4 * (i + 1) + 1, 4 * (i + 1) + 2, 4 * (i + 1) + 3  # indexes: i + 1

        # 1) S_i(x[i]) = f(x[i]) ⮕ a[i] = y[i]
        matrix_a[row][a_i_0] = 1  # a(i): 1

        # 2) S_i(x[i+1]) = f(x[i+1]) ⮕ a[i] + h*b[i] + h^2*c[i] + h^3*d[i] = y[i+1]
        matrix_a[row + 1][a_i_0] = 1  # a[i]: 1
        matrix_a[row + 1][b_i_0] = h  # b[i]: h
        matrix_a[row + 1][c_i_0] = h ** 2  # c[i]: h^2
        matrix_a[row + 1][d_i_0] = h ** 3  # d[i]: h^3

        if i != size_n - 1:
            # 3) S_i`(x[i+1]) = S_i`(x[i+1]) ⮕ b[i] + 2h*c[i] + 3h^2*d[i] - b[i+1] = 0
            matrix_a[row2][a_i_0] = 0
            matrix_a[row2][b_i_0] = 1  # b[i]: 1
            matrix_a[row2][c_i_0] = 2 * h  # c[i]: 2h
            matrix_a[row2][d_i_0] = 3 * h ** 2  # d[i]: 3h^2
            matrix_a[row2][a_i_1] = 0
            matrix_a[row2][b_i_1] = -1  # b[i+1]: -1
            matrix_a[row2][c_i_1] = 0
            matrix_a[row2][d_i_1] = 0

            # 4) S_i``(x[i+1]) = S_i+1``(x[i+1]) ⮕ 2c[i] + 6h*d[i] - c[i+1] = 0
            matrix_a[row2 + 1][a_i_0] = 0
            matrix_a[row2 + 1][b_i_0] = 0
            matrix_a[row2 + 1][c_i_0] = 2  # c[i]: 2
            matrix_a[row2 + 1][d_i_0] = 6 * h  # d[i]: 6h
            matrix_a[row2 + 1][a_i_1] = 0
            matrix_a[row2 + 1][b_i_1] = 0
            matrix_a[row2 + 1][c_i_1] = -2  # c[i+1]: -1
            matrix_a[row2 + 1][d_i_1] = 0
        else:
            # 5) S_0``(x[0]) = 0 ⮕ 2c[0] = 0
            matrix_a[row2][0] = 0
            matrix_a[row2][1] = 0
            matrix_a[row2][2] = 2  # c[0]: 2
            matrix_a[row2][3] = 0

            # 6) S_n-1``(x[n]) = 0 ⮕ 2c[n-1] + 6h*d[n-1] = 0
            matrix_a[row2 + 1][a_i_0] = 0
            matrix_a[row2 + 1][b_i_0] = 0
            matrix_a[row2 + 1][c_i_0] = 2  # d[n-1]: 6h
            matrix_a[row2 + 1][d_i_0] = 6 * h  # c[n-1]: 2

    return matrix_a


def spline_interpolation(x_array, y_array):
    # Init
    h = x_array[1] - x_array[0]
    size_n = len(x_array) - 1
    vector_b = _create_vector_b(y_array, size_n)
    matrix_a = _create_matrix(h, size_n)

    # Calculate coefficient vector for interpolation [a0, b0, c0, d0, a1, ...]
    vector_x = np.linalg.inv(matrix_a).dot(vector_b)

    def f(x):
        # return value for x in interval i
        for index, xi in enumerate(x_array[:-1]):
            if x_array[index] <= x < x_array[index + 1]:
                return _interpolated_polynomial_value(vector_x, x, index, xi)
        # return last value
        return _interpolated_polynomial_value(vector_x, x, -1, x_array[-2])

    return f
