import matplotlib.pyplot as plt

def compare_against_range(x_range, times, labels=None):
    if labels is None:
        labels = [f'solver{i+1}' for i in range(len(x_range))]
    for solver_times, solver_label in zip(times, labels):
        plt.plot(x_range, solver_times, label=solver_label)
    plt.legend()
    plt.show()