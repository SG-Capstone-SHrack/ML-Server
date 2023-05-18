import numpy as np 
from scipy import signal

class RealtimePeakDetector():
    def __init__(self, lag, filterOrder, threshold):
        self.lag = lag
        self.threshold = threshold
        # initialize array
        self.y = []
        self.filteredY = []
        self.avg = []
        self.std = []
        self.signal = []
        # filter design
        fs = 30; fcut = 0.5; cutoff = 2*fcut/fs
        self.filterParam = signal.firwin(filterOrder, cutoff)

    def thresholding_algo(self, new_value):
        self.y.append(new_value)
        i = len(self.y)-1
        if i==0:
            self.filteredY.append(self.y[i])
            self.avg.append(self.y[i])
            self.std.append(0)
            self.signal.append(0)
            return 0
        if i<self.lag:
            self.filteredY.append(signal.lfilter(self.filterParam, 1.0, self.y)[-1])
            self.avg.append(np.mean(self.filteredY))
            self.std.append(np.std(self.filteredY))
            self.signal.append(0)
            return 0

        self.filteredY.append(signal.lfilter(self.filterParam, 1.0, self.y)[-1])

        if (self.filteredY[i] - self.avg[i-1]) > self.threshold*self.std[i-1]:
            self.signal.append(1)
        else:
            self.signal.append(0)

        # self.filteredY.append(signal.lfilter(self.filterParam, 1.0, self.y)[-1])
        self.avg.append(np.mean(self.filteredY[(i-self.lag):i]))
        self.std.append(np.std(self.filteredY[(i-self.lag):i]))

        return self.signal[i]
    
if __name__ == "__main__":
    new_data_point = 200
    rt_peak_finder = RealtimePeakDetector(60, 10, 0.1)
    prev_peak_value = 0
    count = 0
    for i in range(250):
        if i<30:
            new_data_point = new_data_point - 1
        elif 30<=i<60:
            new_data_point = new_data_point + 1
        elif 60<=i<90:
            if i%2 == 0:
                new_data_point = new_data_point + 1
            elif i%2 == 1:
                new_data_point = new_data_point - 1
        elif 90<=i<120:
            new_data_point = new_data_point - 1
        elif 120<=i<150:
            new_data_point = new_data_point + 1
        elif 150<=i<180:
            new_data_point = new_data_point - 1
        elif 180<=i<210:
            new_data_point = new_data_point + 1
        else:
            new_data_point = new_data_point - 1
        is_peak = rt_peak_finder.thresholding_algo(new_data_point)
        print("{} : {}".format(new_data_point, is_peak))
        if prev_peak_value ==0 and is_peak == 1:
            print("peak detected")
            count = count + 1
        prev_peak_value = is_peak
    
    print("count: {}".format(count))