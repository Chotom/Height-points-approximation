import yaml
import math
import pandas as pd
import matplotlib.pyplot as plt

from lagrange_interpolation import lagrange_interpolation
from spline_interpolation import spline_interpolation


# ----------------------------------------------- FUNCTIONS ------------------------------------------------------------
def _chebyshev_points(x: [], y: [], n: int):
    """
    Chebyshev point distribution for more accurate lagrange interpolation

    :param x: x array
    :param y: y array
    :param n: number of points to interpolate
    :return: x, y points with chebyshev distribution in x array interval
    """
    size_n = len(x) / 2
    x_points = []
    y_points = []

    for i in range(n):
        results = math.cos((2 * i + 1) * math.pi / (2 * n))  # result for interval [-1; 1]
        index = int(size_n - size_n * results)  # results for interval [x[0]; x[n]]
        x_points.append(x[index])
        y_points.append(y[index])

    return x_points, y_points


def _print_data(x_array: [], y_array: [], x_point: [], y_point: [], title: str, func, print_points=True, do_scale=True):
    """
    :param x_array: All x values data
    :param y_array: All y values data
    :param x_point: Interpolated x points
    :param y_point: Interpolated y points
    :param title: Graph title
    :param func: Function to calculate func(x) points
    :param print_points: Boolean tell to print or not interpolated points
    :param do_scale: Scale graph
    """

    plt.plot(x_array, y_array, color='orange', label='original function')
    plt.plot(x_array, [func(x) for x in x_array], label='interpolation function')

    if print_points:
        plt.plot(x_point, y_point, 'g.', label='interpolation points')
    if do_scale:
        plt.ylim((min(y_array) - abs(min(y_array) / 10), max(y_array) + abs(max(y_array) / 10)))

    plt.ylabel('Height')
    plt.xlabel('Distance')
    plt.title(title + "\n" + str(len(x_point)) + " interpolation points")
    plt.legend()
    plt.show()


# ----------------------------------------------- MAIN BODY ------------------------------------------------------------
def main():
    # Init values
    try:
        with open("settings.yml", "r") as config_file:
            config = yaml.safe_load(config_file)
            params = config['main_params']
            path = params['filepath']
            step = params['step']
        config_file.close()
    except FileNotFoundError as e:
        print("SettingsFileNotFoundError: ", e)
        raise

    # Load data
    df = pd.read_csv(path, names=["distance", "height"])
    x_array, y_array = df['distance'].to_numpy(), df['height'].to_numpy()
    x_array, y_array = x_array[:-(len(x_array) % step - 1)], y_array[:-(len(y_array) % step - 1)]
    x_point, y_point = x_array[::step], y_array[::step]
    x_cheby, y_cheby = _chebyshev_points(x_array, y_array, (len(x_array) // step + 1))

    # Create interpolation functions
    f_spline = spline_interpolation(x_point, y_point)
    f_lagrange = lagrange_interpolation(x_point, y_point)
    f_cheby = lagrange_interpolation(x_cheby, y_cheby)

    # Print function
    _print_data(x_array, y_array, x_point, y_point, path + "\nlagrange interpolation", f_lagrange)
    _print_data(x_array, y_array, x_cheby, y_cheby, path + "\nlagrange interpolation - chebyshev distribution", f_cheby)
    _print_data(x_array, y_array, x_point, y_point, path + "\nspline interpolation", f_spline)


if __name__ == '__main__':
    main()
