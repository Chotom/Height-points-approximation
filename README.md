# Height-points-approximation
Height points approximation by different interpolation methods written in Python using pandas, numpy and matplotlib. 

## Table of contents
* [Description](#description)
* [Settings](#settings)
* [Examples](#examples)

## Description
Program compare two methods of interpolation:
- spline interpolation
- lagrange interpolation (with and without chebyshev nodes)

It compares them by printing approximated function.

## Settings
In yaml file, you can configurate path to csv file with given functions and number of nodes to approximate function (take every x node).
```yml
main_params:
  filepath: './data/MountEverest.csv'   # path for file
  step: 21                              # get every step'th point
```

## Examples
- Spline interpolation:

![spline interpolation](/data/chart_spline.png)

- Lagrange interpolation with evenly spaced 20 nodes, which cause Runge's phenomenon:

![spline interpolation](/data/chart_lagrange.png)

- Lagrange interpolation with 20 Chebyshev nodes:

![spline interpolation](/data/chart_chebyshev.png)
