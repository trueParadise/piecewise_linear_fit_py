import numpy as np
import matplotlib.pyplot as plt
import pwlf
from pyDOE import lhs


def adjiman(x):
    F = np.cos(x[:, 0])*np.sin(x[:, 1]) - ((x[:, 0])/(x[:, 1]**2 + 1.0))
    return F


np.random.seed(1231)
lhd = lhs(2, samples=100, criterion='maximin')
lb = -10.0
ub = 10.0
x = (ub - lb) * lhd + lb
y = adjiman(x)

n_segments = 2
my_mv_model = pwlf.PiecewiseMultivariate(x, y, n_segments, degree=4,
                                         multivariate_degree=3)
my_mv_model.fit()

n_contours = 100
xt = np.linspace(lb, ub, n_contours)
x1, x2 = np.meshgrid(xt, xt)
x_hat = np.array([x1.flatten(), x2.flatten()]).T
y_true = adjiman(x_hat)
y_hat = my_mv_model.predict(x_hat)

plt.figure()
plt.title('Adjiman function')
plt.contourf(x1, x2, y_true.reshape(n_contours, n_contours))
plt.plot(x[:, 0], x[:, 1], 'ok', label='DOE')
plt.colorbar()
plt.legend()
plt.ylabel(r'$x_2$')
plt.xlabel(r'$x_1$')

plt.figure()
plt.title('pwlf multivariate model')
plt.contourf(x1, x2, y_hat.reshape(n_contours, n_contours))
plt.plot(x[:, 0], x[:, 1], 'ok', label='DOE')
plt.colorbar()
plt.ylabel(r'$x_2$')
plt.xlabel(r'$x_1$')
plt.legend()

# qq plot
plt.figure()
plt.plot(y_true, y_hat, '.')
plt.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], '-k', label='best possible')
plt.legend()
plt.xlabel('True response')
plt.ylabel('Multivariate pwlf model')
plt.show()

# plot individual models
for i in range(2):
    plt.figure()
    plt.plot(xt, my_mv_model.models[i].predict(xt), '-',
             label='model ' + str(i))
    plt.plot(x[:, i], y, 'ok', label='Training data')
    plt.legend()
    plt.xlabel('x ' + str(i))
    plt.ylabel('y')
plt.show()
