#!/bin/bash

# Specify the path to the Wireshark capture file
CAPTURE_FILE="precedence1.pcapng"

# Function to compute average rate for traffic flows
compute_average_rate() {
    # Filter traffic for each traffic flow and calculate average rate
    echo "Average Rate for Traffic Flows:"
    echo "--------------------------------"

    # # Traffic from 11.0.0.1 with precedence 7
    # rate_flow_7=$(tshark -r $CAPTURE_FILE -Y "ip.src == 11.0.0.1 && ip.tos == 0x70" -T fields -e frame.len | awk '{sum += $1} END {printf("%.2f", sum / 1024)}')
    # echo "From 11.0.0.1 with precedence 7: $rate_flow_7 KB/s"

    # Traffic from 11.0.0.1 with precedence 1
    rate_flow_1=$(tshark -r $CAPTURE_FILE -Y "ip.src == 11.0.0.1 && ip.tos == 0x08" -T fields -e frame.len | awk '{sum += $1} END {printf("%.2f", sum / 1024)}')
    echo "From 11.0.0.1 with precedence 1: $rate_flow_1 KB/s"

    # # Traffic from 12.0.0.1
    # rate_flow_12=$(tshark -r $CAPTURE_FILE -Y "ip.src == 12.0.0.1" -T fields -e frame.len | awk '{sum += $1} END {printf("%.2f", sum / 1024)}')
    # echo "From 12.0.0.1: $rate_flow_12 KB/s"
}

# Main function
main() {
    compute_average_rate
}

# Execute main function
main
