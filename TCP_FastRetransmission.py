import numpy as np
import matplotlib.pyplot as plt

# Function to parse the trace file and extract cw and rto values
def parse_trace_file(trace_file):
    time = []
    cw_values = []
    rto_values = []
    
    with open(trace_file, 'r') as file:
        for line in file:
            if line.startswith('r'):
                fields = line.split()
                if fields[6] == 'tcp' and fields[7] == '1':
                    time.append(float(fields[1]))
                    cw_values.append(int(fields[12]))
                    rto_values.append(float(fields[15]))
                    print('time=' + fields[1] + 'cw=' + fields[12] + 'rto=' + fields[15])
    return time, cw_values, rto_values

# Function to plot congestion window and timeout
def plot_cw_and_rto(time, cw_values, rto_values):
    plt.figure(figsize=(10, 6))
    plt.plot(time, cw_values, label='Congestion Window (cw)', color='blue')
    plt.plot(time, rto_values, label='Timeout (rto)', color='red')
    plt.xlabel('Time (s)')
    plt.ylabel('Value')
    plt.title('Congestion Window and Timeout over Time')
    plt.legend()
    plt.grid(True)
    plt.show()

# Main function
def main():
    trace_file = 'trace_file_rfc793.res'  # Path to the simulation trace file
    time, cw_values, rto_values = parse_trace_file(trace_file)
    plot_cw_and_rto(time, cw_values, rto_values)

if __name__ == "__main__":
    main()
