def lagrange_interpolation(x_array, y_array):
    def f(x):
        base = [1] * len(x_array)

        # Calculate lagrange base
        for i, xi in enumerate(x_array):
            for j, xj in enumerate(x_array):
                if i != j and xi != xj:
                    base[i] *= ((x - xj) / (xi - xj))
        # F(x) = sum_i (yi * lagrange_base(xi))
        return sum([y * i_base for y, i_base in zip(y_array, base)])

    # return interpolated function
    return f
