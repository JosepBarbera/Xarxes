from heapq import heappop, heappush
import heapq
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

        time = 0.0
        transmission_order = []
        first_packet = True
        first_arrival_time = 0.0
        first_iteration = True
        while packets:
            next_transmission = None
            for packet in packets:

                priority_time = max(time, packet.arrival_time) + packet.packet_length / (self.bandwidth_fractions[packet.flow_id - 1] / 100)

                if first_packet:

                    first_arrival_time = packet.arrival_time
                    next_transmission = (priority_time, packet)
                    first_packet = False

                if ((next_transmission is None or priority_time < next_transmission[0]) or (first_arrival_time > packet.arrival_time and priority_time < next_transmission[0])) and not first_iteration:
                    first_arrival_time = packet.arrival_time
                    next_transmission = (priority_time, packet)
                elif((next_transmission is None or priority_time < next_transmission[0]) and first_arrival_time == packet.arrival_time  and first_iteration):
                    first_arrival_time = packet.arrival_time
                    next_transmission = (priority_time, packet)


            if next_transmission is None:
                break

            first_iteration = False
            priority_time, packet = next_transmission
            packets.remove(packet)
            transmission_order.append(packet)
            time = priority_time
             
            print(str(packet.arrival_time) + " " + str(packet.packet_length) + " " + str(packet.flow_id) + " Tiempo: " + str(time))
        print (transmission_order)

        

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
