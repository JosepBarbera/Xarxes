if {$argc == 1} {
    set flag  [lindex $argv 0] 
} else {
    puts "      CBR0-UDP n0"
    puts "                \\"
    puts "                 n2 ---- n3"
    puts "                /"
    puts "      CBR1-TCP n1 "
    puts ""
    puts "  Usage: ns $argv0 (0: RFC793 with slow start, 1: Reno) "
    puts ""
    exit 1
}

# MSS: 1000 bytes
set mss 1000

# CWMAX: 10 MSS
set cwmax [expr 10 * $mss]

# Time resolution: 0.01 s
set time_resolution 0.01

# Simulation time: 200 s
set sim_time 200

# UDP traffic activates 20 s after start and ends 20 s before ending simulation
set udp_start 20.0
set udp_end [expr $sim_time - 20.0]

# Links speed:
set link_speed_n0_n2 "250Kbps"
set link_speed_n1_n2 "250Kbps"
set link_speed_n2_n3 "50Kbps"

# Links delay
set link_delay_n0_n2 "20ms"
set link_delay_n1_n2 "20ms"
set link_delay_n2_n3 "0.5s"

# CBR traffic generator for UDP agent: 50 Kbps
set cbr_traffic_rate_udp "50Kbps"

# Exponential traffic generator for UDP agent: 50 Kbps
set exp_traffic_rate_udp "50Kbps"

# Node 2 buffer size: 20
set node_2_buffer_size 20

# TCP agent parameters
set tcp1_algorithm "Reno"  ;# Set to "Reno" by default
if {$flag == 0} {
    set tcp1_algorithm "RFC793 with slow start"
}

# Creating the simulator object
set ns [new Simulator]

#file to store results
set tracefile "sor.$tcp1_algorithm.tr"
set cwfile "cw.$tcp1_algorithm.tr"

set nf [open $tracefile w]
$ns trace-all $nf

set nff [open $cwfile w]

#Finishing procedure
proc finish {} {
    global ns nf nff tracefile cwfile

    $ns flush-trace

    # Process "sor.tr" to get sent packets
    exec awk {{ if ($1=="-" && $3==1 && $4==2) print $2, 49}}  $tracefile > tx.tr
    # Process "sor.tr" to get dropped packets
    exec awk {{ if ($1=="d" && $3==2 && $4==3) print $2, 44}}  $tracefile  > drop.tr
    exec awk {{ print $2,$3}}  $tracefile  > out.tr

    close $nf
    close $nff
    exit 0
}

# TCP times recording procedure
proc record { } {
    global ns tcp1 nff
    # Getting the congestion window
    set cw  [$tcp1 set cwnd_] 
    set now [$ns now]
    puts $nff "$now $cw"

    $ns at [expr $now+0.1] "record"
}

#Create 4 nodes
set n0 [$ns node]
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]

#Duplex lines between nodes
$ns duplex-link $n0 $n2 $link_speed_n0_n2 $link_delay_n0_n2 DropTail
$ns duplex-link $n1 $n2 $link_speed_n1_n2 $link_delay_n1_n2 DropTail
$ns duplex-link $n2 $n3 $link_speed_n2_n3 $link_delay_n2_n3 DropTail

# Node 0: UDP agent with Exponential traffic generator
set udp0 [new Agent/UDP]
$ns attach-agent $n0 $udp0

set cbr0 [new Application/Traffic/Exponential]
$cbr0 set rate_ $exp_traffic_rate_udp
$cbr0 attach-agent $udp0
$udp0 set class_ 0

set null0 [new Agent/Null]
$ns attach-agent $n3 $null0

$ns connect $udp0 $null0
$ns at $udp_start "$cbr0 start"
$ns at $udp_end "$cbr0 stop"

# Node 1: TCP agent
set tcp1 [new Agent/TCP/$tcp1_algorithm]
$tcp1 set class_ 1

$tcp1 set add793karnrtt_ true
$tcp1 set add793expbackoff_ true

if {$flag == 0} {
    $tcp1 set add793slowstart_ true
}

$ns attach-agent $n1 $tcp1
$tcp1 set tcpTick_ $time_resolution
$tcp1 set window_ $cwmax

set null1 [new Agent/TCPSink]
$ns attach-agent $n3 $null1

# Add a CBR traffic generator
set cbr1 [new Application/Traffic/CBR]
$cbr1 set rate_ $cbr_traffic_rate_udp
$cbr1 attach-agent $tcp1
$ns at 0.0 "$cbr1 start"
$ns at 0.0 "record"

$ns connect $tcp1 $null1 

# Stop simulation at 200 s
$ns at $sim_time "finish"

# Run simulation
$ns run
