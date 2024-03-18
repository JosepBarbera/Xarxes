from operator import contains


def calculate_throughput(trace_file):
    throughput = 0
    total_throughput = 0
    with open(trace_file, 'r') as file:
        for line in file:
            fields = line.split()
            if fields and fields[0] == 'r' and fields[3] == '3' and fields[4] == 'tcp' and 'A' not in fields[6]:
                packet_length = float(fields[5])
                total_throughput += packet_length
        throughput = ((total_throughput * 8) / 200)
    return throughput

# Usage
trace_file = "Trace_Reno.res"
throughput = calculate_throughput(trace_file)

print("Throughput:", str(throughput), "bps")
