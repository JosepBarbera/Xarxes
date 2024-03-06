def find_fast_retransmission(trace_file):
    dupack_count = 0
    last_ack_info = None  # Store information about the last received ACK

    fast_retransmissions = []

    with open(trace_file, 'r') as file:
        for line in file:
            fields = line.split()

            # Check if the line represents an ACK received by node 1
            if fields[0] == 'r' and fields[3] == '1' and fields[4] == 'ack':
                # Extract ACK information
                ack_info = (fields[2],fields[3], fields[10])  # Source, destination, sequence number

                # Check if the ACK is a duplicate acknowledgment (dupack)
                if last_ack_info == ack_info:
                    dupack_count += 1
                else:
                    # Reset dupack count if the ACK is not for the same packet
                    dupack_count = 0

                last_ack_info = ack_info

                # Check if we have received three consecutive dupacks
                if dupack_count >= 3:
                    fast_retransmissions.append(line.strip())  # Store the line

    return fast_retransmissions

# Usage
trace_file = "trace_file_reno.res"
fast_retransmissions = find_fast_retransmission(trace_file)

if fast_retransmissions:
    print("Fast retransmission detected at the following lines:")
    for line in fast_retransmissions:
        print(line)
else:
    print("No fast retransmission detected.")
