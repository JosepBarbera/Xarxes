def calculate_throughput(trace_file):
    total_bytes = 0
    start_time = 0
    end_time = 0

    with open(trace_file, 'r') as file:
        for line in file:
            fields = line.split()

            # Check if the line represents data transmission
            if fields and fields[0] in ('+', '-'):
                # Extract relevant fields (arrival time, packet length)
                arrival_time = float(fields[1])
                packet_length = float(fields[5])

                # Update total bytes transferred
                total_bytes += packet_length

                # Update start and end time
                if start_time is None:
                    start_time = arrival_time
                end_time = arrival_time

    # Calculate duration of trace
    duration = end_time - start_time

    # Calculate throughput (bits per second)
    throughput_bps = (total_bytes * 8) / duration

    return throughput_bps

# Usage
trace_file = "trace_file_reno.res"
throughput = calculate_throughput(trace_file)
print("Throughput:", throughput, "bps")