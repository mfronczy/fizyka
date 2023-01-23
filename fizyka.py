import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import time
try:
    plt.ion()
    #zakres osi X
    b = 10
    #zakres osi Y
    c = 10
    #ilość klatek do wygenerowania
    frames=500
    #czas opóźnienia między renderowaniem kolejnych klatek
    tts=0.000001
    #mnożnik ładunków
    mn = 1
    #szybkość zmienności, domyślnie 0 - czyli stały ładunek, przykładowo można wpisać 1/8, aby na każdy cykl zmienności przypadało 8 klatek
    faza = 1/8
    #przesunięcie wartości ładunków
    vert=0



    def func(q, r0, x, y):
        den = np.hypot(x - r0[0], y - r0[1]) ** 3
        return q * (x - r0[0]) / den, q * (y - r0[1]) / den

    def plotting():

        a = int(input("Podaj ilość ładunków: "))

        nx, ny = 64, 64
        x = np.linspace(-b, b, nx)
        y = np.linspace(-c, c, ny)
        X, Y = np.meshgrid(x, y)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        nq = a
        charges = []
        charges1 = []
        for i in range(nq):

            ladunek = int(input("Podaj wielkość " + str(i+1) + " ładunku: " ))
            xcoord = int(input("Podaj współrzędną X " + str(i + 1) + " ładunku: "))
            ycoord = int(input("Podaj współrzędną Y " + str(i + 1) + " ładunku: "))
            q = ladunek
            charges1.append((q, (xcoord, ycoord)))

        for j in range(frames):
            chargestemp = []

            for charge in charges1:
                as_list_charge = list(charge)
                as_list_charge[0] = mn * as_list_charge[0] * np.cos(np.pi * j * faza) + vert
                chargestemp.append(as_list_charge)

            Ex, Ey = np.zeros((ny, nx)), np.zeros((ny, nx))
            for charge in chargestemp:
                ex, ey = func(*charge, x=X, y=Y)
                Ex += ex
                Ey += ey

            color = 4 * np.log(np.hypot(Ex, Ey))
            #plot linii, odkomentować, aby zaczął działać#######################################################################
            #magne = ax.streamplot(x, y, Ex, Ey, color=color, linewidth=1, cmap=plt.cm.inferno,density=2, arrowstyle='->', arrowsize=1.5)


            charge_colors = {True: '#aa0000', False: '#0000aa'}
            for q, pos in chargestemp:
                ax.add_artist(Circle(pos, 0.2, color=charge_colors[q > 0]))
                if q < 0:
                    ax.annotate("-" + str(q), xy=pos)
                else:
                    ax.annotate(q, xy=pos)

            C = 4 * np.log(np.hypot(Ex, Ey))
            ax.set_xlabel('$x$')
            ax.set_ylabel('$y$')
            ax.set_xlim(-b, b)
            ax.set_ylim(-c, c)
            ax.set_aspect('equal')
            E = (Ex ** 2 + Ey ** 2) ** .5
            Ex = Ex / E
            Ey = Ey / E
            skip = (slice(None, None, 5), slice(None, None, 5))
            #plot strzałkowy, odkomentować, aby zaczął działać#############################################################
            plt.quiver(X[skip], Y[skip], Ex[skip], Ey[skip], C[skip], pivot='mid')
            cbar = plt.colorbar()
            cbar.ax.set_ylabel('Natężęnie pola elektrycznego')
            plt.axis('equal')
            fig.canvas.draw()
            fig.canvas.flush_events()
            plt.show()
            time.sleep(tts)
            cbar.remove()

            plt.cla()


    if __name__ == "__main__":
        plotting()
except ValueError:
    print("Podana wartość nie jest liczbą!")