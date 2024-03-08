from heapq import heappop, heappush
import heapq
from struct import pack
class Packet:
    def __init__(self, arrival_time, packet_length, flow_id, id):
        self.arrival_time = arrival_time
        self.packet_length = packet_length
        self.flow_id = flow_id
        self.priority_time = 0.0
        self.id = id

class WFQScheduler:
    def __init__(self, bandwidth_fractions):
        self.bandwidth_fractions = bandwidth_fractions
        self.queue = []
        self.current_time = 0
        self.flow_counters = {}
        self.time_per_flow = {}
        self.total_packets_processed = 0

        self.packet_to_send = Packet(0,0,0,0)
        self.packets = []
        self.transmission_order = []
        self.arrived_packet = {}
        self.time = 0.0
        self.p = 0.0

    def send_packet(self):
        self.packets.remove(self.packet_to_send)
        self.transmission_order.append(self.packet_to_send)
        self.time += self.packet_to_send.packet_length
        self.p = self.packet_to_send.priority_time
        print(self.packet_to_send.id)

        
    
    def check_queue(self):
        already_sended_packet = self.packet_to_send
        next_to_send_time = self.time
        first_packet = True
        for packet in self.packets:

            if packet not in self.arrived_packet and packet.arrival_time <= next_to_send_time:#self.time
                if first_packet:
                    first_packet = False
                    self.packet_to_send = packet
                packet.priority_time = max(self.p, packet.arrival_time) + packet.packet_length * (1 / (self.bandwidth_fractions[packet.flow_id - 1] / 100 ))
                self.arrived_packet[packet] = True
                if self.packet_to_send.priority_time > packet.priority_time:
                    self.packet_to_send = packet
            elif packet in self.arrived_packet and not packet in self.transmission_order:
                if first_packet:
                    first_packet = False
                    self.packet_to_send = packet
                if self.packet_to_send.priority_time > packet.priority_time:
                    self.packet_to_send = packet

        #POR SI NO HA LLEGADO NINGÚN PAQUETE ANTES DE QUE FINALICE
        if already_sended_packet == self.packet_to_send:
            self.packets[0].priority_time = max(self.p, packet.arrival_time) + packet.packet_length * (1 / (self.bandwidth_fractions[packet.flow_id - 1] / 100 ))
            self.packet_to_send = self.packets[0]


    def schedule_packets(self, packets):

        self.packets = packets
        time = 0.0
        first_packet = True
        first_packet_arrival =  0
        
        for packet in self.packets:
            if first_packet:
                first_packet_arrival = packet.arrival_time
                first_packet = False
                self.packet_to_send = packet
            if first_packet_arrival == packet.arrival_time:
                packet.priority_time = max(self.p, packet.arrival_time) + packet.packet_length * (1 / (self.bandwidth_fractions[packet.flow_id - 1] / 100 ))
                self.arrived_packet[packet] = True
                if self.packet_to_send is None or self.packet_to_send.priority_time > packet.priority_time:
                    self.packet_to_send = packet

        #print(str(self.packet_to_send.packet_length) + " " + str(self.packet_to_send.priority_time))
        ##ENVIAR PRIMER PAQUETE
        self.send_packet()

        while self.packets:
            ##COMPROBAMOS SI HAY PAQUETES QUE HAN ENTRADO MIENTRAS SE ENVIABA EL PRIMER PAQUETE Y LOS AÑADIMOS COMO SIGUIENTES A ENVIAR

            self.check_queue()

            #print(str(self.packet_to_send.arrival_time) + " " + str(self.packet_to_send.priority_time))
            self.send_packet()



def main(bandwidth_fractions, filename):
    packets = []
    i = 0
    with open(filename, 'r') as file:
        for line in file:
            i +=1
            arrival_time, packet_length, flow_id = map(float, line.split())
            packets.append(Packet(arrival_time, packet_length, int(flow_id), i))

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
