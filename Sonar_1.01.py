import brping
from brping import Ping1D
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.signal import find_peaks
from datetime import datetime



if __name__ == "__main__":
    Sonar = Ping1D()
    Deneme = brping.Ping360
    Sonar.connect_serial("COM8",1152000)
    paused = False
    fig = plt.figure()
    ax1 = fig.add_subplot(2, 1, 1)
    ax2 = fig.add_subplot(2, 1, 2)
    def on_press(event):
        global paused
        if event.key.isspace():
            if paused:
                ani.resume()
                paused = False
            else:
                ani.pause()
                paused = True
        elif event.key == 'left':
            ani.direction = -1
        elif event.key == 'right':
            ani.direction = +1
    fig.canvas.mpl_connect('key_press_event', on_press)
    def animate(i):
        print("----------------------------NEW DATA----------------------------")
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time: ", current_time)

        print(f"Time: f{time.time()}")
        print("Distance: %s\tConfidence: %s%%" % (float(data["distance"] / 1000), data["confidence"]))
        print(Sonar.get_gain_setting())
        print(Sonar.get_range())
        profile_data = Sonar.get_profile()["profile_data"]
        # for i in range(100):
        #     print(Sonar.get_profile()["profile_data"])
        A=Sonar.get_range()["scan_length"]
        distance=Sonar.get_distance()["distance"]
        print(distance)
        list = []
        for i in profile_data:
            list.append(i)
        print(f"Raw data: {list}")
        y = list
        a = 0
        x = []
        y2=list
        indices = []
        biggest = 0

        for i in range(len(list)):
            x.append(a*(A/200))
            a+=1
        ax1.clear()
        ax1.plot(x, list)

        for i in range(200):
            if y2[i]>200:
                y2[i]=0
                indices.append(i)
            if y[i]<20:
                y[i]=0
            if x[i]<distance*1.10 and x[i]>distance*0.9:
                y[i] = 0
            if x[i]>distance:
                y[i] = 0
            if x[i]<600 or x[i]<A*0.10:
                y[i] = 0
        interval=[0,0]

        for i in range(len(indices)):
            if (i+1)<len(indices):
                if (indices[i+1]-indices[i])>biggest:
                    biggest = indices[i+1]-indices[i]
                    interval = [indices[i], indices[i+1]]

        for i in range(interval[0]):
            y2[len(range(interval[0]))-i] = 0

        for i in range(100):
             if y2[interval[0]+i+1] == 0:
                 break
             if y2[interval[0]+i+1] > 0:
                 y2[interval[0] + i + 1] = 0

        print(f"İndices: {indices}")
        print(f"Biggest interval: {interval}")
        print(f"Second graph y axis: {y2}")

        ax2.clear()
        ax2.plot(x,y2)

        latest_data = y2[interval[0]:interval[1]]
        peaks, _ = find_peaks(y2, height=0)
        maximum_values_distance = []
        derivative = np.diff(latest_data)
        print(f"Peaks: {peaks}")
        for i in range(len(peaks)):
            try:
                maximum_values_distance.append(peaks[i]*(A/200))
            except IndexError:
                pass
        maximum_values_distance_sp = np.std(maximum_values_distance)
        maximum_values_distance_mean = np.mean(maximum_values_distance)
        print(f"Peak values: {maximum_values_distance}")
        print(f"Standard Deviaton of the maximum values: {maximum_values_distance_sp}")
        print(f"Mean Avarage of the maximum values: {maximum_values_distance_mean}")
        print(f"Derivative: {derivative}")

        dataset_count = 10

        if len(dataset)<dataset_count:
            dataset.append(latest_data)
        else:
            for i in range(len(dataset)):
                if i != len(dataset)-1:
                    dataset[i]=dataset[i+1]
            dataset[dataset_count-1]=latest_data

        if len(standard_deviation)<dataset_count:
            maximum_values_distance_dataset_sp.append(maximum_values_distance_sp)
            maximum_values_distance_dataset_mean.append(maximum_values_distance_mean)
            standard_deviation.append(round(np.std(latest_data), 3))
            mean.append(round(np.mean(latest_data), 3))
            maximum.append(round(np.amax(latest_data), 3))
            try:
                gradient.append(np.gradient(latest_data))
            except ValueError:
                print("Value Error")
        else:
            for i in range(len(standard_deviation)):
                if i != len(dataset)-1:
                    try:
                        maximum_values_distance_dataset_mean[i] = maximum_values_distance_dataset_mean[i+1]
                        maximum_values_distance_dataset_sp[i] = maximum_values_distance_sp[i+1]
                    except IndexError:
                        pass
                    try:
                        gradient[i] = np.gradient(latest_data)
                    except:
                        pass
                    standard_deviation[i]=standard_deviation[i+1]
                    mean[i] = mean [i+1]
                    maximum[i] = maximum [i+1]
            try:
                gradient[dataset_count-1]=np.gradient(latest_data)
                maximum_values_distance_dataset_sp[dataset_count - 1] = maximum_values_distance_sp
                maximum_values_distance_dataset_mean[dataset_count - 1] = maximum_values_distance_mean
                standard_deviation[dataset_count - 1] = round(np.std(latest_data), 3)
                mean[dataset_count - 1] = round(np.mean(latest_data), 3)
                maximum[dataset_count - 1] = round(np.amax(latest_data), 3)
            except ValueError:
                print("Value Error")


        print(f"Discrete Maximums of last 10 data: {maximum}")
        print(f"Discrete Means of last 10 data: {mean}")
        print(f"Discrete Standard deviations of last 10 data: {standard_deviation}")
        #print(f"Discrete gradients of last 10 data: {gradient}")

        print(f"Avarage Maximum of the last 10 data: {round(np.mean(maximum),3)}")
        print(f"Mean of the last 10 data: {round(np.mean(mean),3)}")
        print(f"Avarage Standard deviation the of last 10 data: {round(np.mean(standard_deviation),3)}")
        print(f"Maximum of the last 10 data: {np.amax(maximum)}")
        print(f"Probable Distance of Object: {np.mean(maximum_values_distance_dataset_mean)}")
        print(f"Mean Average of the last 10 maximum values: {maximum_values_distance_dataset_mean}")
        print(f"Standard Deviation of the last 10 maximum values: {maximum_values_distance_dataset_sp}")

        print(f"Histogram: {np.histogram(list)}")

        print("----------------------------END DATA----------------------------")

        return

    while True:
        data = Sonar.get_distance()
        Sonar.set_mode_auto(1,True)
        dataset = []
        standard_deviation = []
        mean = []
        maximum = []
        gradient = []
        maximum_values_distance_dataset_sp = []
        maximum_values_distance_dataset_mean = []
        # Sonar.set_gain_setting(0,True)
        # Sonar.set_ping_interval(10,True)
        if data:

            ani = animation.FuncAnimation(fig, animate, interval = 300)
            plt.show()

            #print(profile_data)

        else:
            print("Failed to get distance data")
        #time.sleep(0.1)

