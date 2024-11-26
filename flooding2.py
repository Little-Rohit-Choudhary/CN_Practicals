class Packet:
    def __init__(self, counter):
        self.counter = counter

def flooding_simulation(version, packet, lines, k=1, input_line=None):
    print(f"\n--- Version {version} ---")
    if version == 1:
        active_lines = lines
    elif version == 2:
        if input_line is None:
            print("Error: input_line is required for version 2.")
            return
        active_lines = [line for line in lines if line != input_line]
    elif version == 3:
        active_lines = sorted(lines)[:k]

    for line in active_lines:
        if packet.counter > 0:
            print(f"Forwarding to Line {line}, Remaining Counter: {packet.counter - 1}")
            packet.counter -= 1
        else:
            print(f"Packet on Line {line} is Discarded (Counter Reached Zero).")
            break

# Example simulation
lines = [1, 2, 3, 4]
initial_counter = 3

flooding_simulation(1, Packet(initial_counter), lines)  # Version 1
flooding_simulation(2, Packet(initial_counter), lines, input_line=1)  # Version 2
flooding_simulation(3, Packet(initial_counter), lines, k=2)  # Version 3