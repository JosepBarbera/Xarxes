from heapq import heappop, heappush

class Packet:
    def __init__(self, arrival_time, packet_length, flow_id):
        self.arrival_time = arrival_time
        self.packet_length = packet_length
        self.flow_id = flow_id

class WFQScheduler:
    def __init__(self, bandwidth_fractions):
        self.bandwidth_fractions = bandwidth_fractions
        self.queue = []
        self.current_time = 0
        self.flow_counters = {}
        self.time_per_flow = {}
        self.total_packets_processed = 0

    def schedule_packets(self, packets):
        for packet in packets:
            heappush(self.queue, (packet.arrival_time, packet))
        
        while self.queue:

            # arrival_time = temps arribada = A sub i 
            # packet = longitud = S sub i
            # flow = r sub j =(bandwidth_fraction / 100)
            # F prima = temps de finalització del paquet actual
            
            # F sub i = max (F prima i A sub i) + S sub i * r sub j

            arrival_time, packet = heappop(self.queue)
            self.current_time = max(self.current_time, arrival_time)

            flow_id = packet.flow_id
            packet_length = packet.packet_length
            bandwidth_fraction = self.bandwidth_fractions[flow_id - 1]

            if flow_id not in self.flow_counters:
                self.flow_counters[flow_id] = 0
                self.time_per_flow[flow_id] = 0

            # Calculate the time taken to transmit the packet based on bandwidth fraction
            time_taken = packet_length / (bandwidth_fraction / 100)
            self.time_per_flow[flow_id] += time_taken

            # Update current time
            self.current_time += time_taken
            self.flow_counters[flow_id] += 1
            self.total_packets_processed += 1

            print(f"Packet {self.total_packets_processed}: Flow {flow_id}, "
                  f"Arrival Time: {packet.arrival_time}, "
                  f"Transmission Start Time: {self.current_time - time_taken}, "
                  f"Transmission End Time: {self.current_time}, "
                  f"Time taken: {time_taken}")







def main(bandwidth_fractions, filename):
    packets = []
    with open(filename, 'r') as file:
        for line in file:
            arrival_time, packet_length, flow_id = map(float, line.split())
            packets.append(Packet(arrival_time, packet_length, int(flow_id)))

    scheduler = WFQScheduler(bandwidth_fractions)
    scheduler.schedule_packets(packets)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python script.py <bandwidth_fractions> <filename>")
        sys.exit(1)
    
    bandwidth_fractions = list(map(float, sys.argv[1].split(',')))
    filename = sys.argv[2]
    main(bandwidth_fractions, filename)
