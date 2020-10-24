#!/usr/bin/python3

import matplotlib.pyplot as plt

def plot(x, y, xlab, ylab, mark="-"):
    plt.plot(x, y, mark)
    plt.xlabel(xlab, fontsize=18)
    plt.ylabel(ylab, fontsize=18)
    plot_format()

def plot2(x1, y1, x2, y2, xlab, ylab, lab1, lab2, mark1="o", mark2="-"):
    plt.plot(x1, y1, mark1, label=lab1)
    plt.plot(x2, y2, mark2, label=lab2)
    plt.xlabel(xlab, fontsize=18)
    plt.ylabel(ylab, fontsize=18)
    plot_format()

def plot_format():
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.grid()
    plt.tight_layout()
