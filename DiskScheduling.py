# To run the program, use the following command:
# python DiskScheduling.py <initial_position> requests.txt
# initial_position: initial position of the disk head (can be any number)
# Example: python DiskScheduling.py 2000 requests.txt

import sys

# read requests file
def read_requests(filename):
    with open(filename, 'r') as file:
        return [int(line.strip()) for line in file.readlines()]

# calculate amount of head movements
def calculate_head_movements(requests, initial_position):
    movements = 0
    current_position = initial_position
    for request in requests:
        movements += abs(request - current_position)
        current_position = request
    return movements

# FCFS algorithm
def fcfs(requests, initial_position):
    return calculate_head_movements(requests, initial_position)

# before serving the requests, I sorted them in ascending order
def optimized_fcfs(requests, initial_position):
    requests.sort()
    return calculate_head_movements(requests, initial_position)

# SCAN algorithm
def scan(requests, initial_position):
    requests.sort()
    left = [r for r in requests if r <= initial_position]
    right = [r for r in requests if r > initial_position]

    # moving to innermost cylinder (smallest number) initially
    movements = calculate_head_movements(left[::-1], initial_position)
    if right:
        movements += abs(left[0] - right[0])
        movements += calculate_head_movements(right, right[0])
    return movements

# I split the requests into two halves based on the initial position, then do the algorithm for each half
def optimized_scan(requests, initial_position):
    # Split requests based on initial position
    lower_half = [r for r in requests if r <= initial_position]
    upper_half = [r for r in requests if r > initial_position]

    # Initialize movements
    total_movements = 0

    # Process lower half with SCAN
    if lower_half:
        lower_half.sort(reverse=True)
        total_movements += calculate_head_movements(lower_half, initial_position)

    # Process upper half with SCAN
    if upper_half:
        upper_half.sort()
        if lower_half:
            total_movements += abs(lower_half[0] - upper_half[0])
            total_movements += calculate_head_movements(upper_half, upper_half[0])
        else:
            total_movements += calculate_head_movements(upper_half, initial_position)

    return total_movements

# C-SCAN algorithm
def c_scan(requests, initial_position):
    requests.sort()
    left = [r for r in requests if r <= initial_position]
    right = [r for r in requests if r > initial_position]

    # moving to innermost cylinder (smallest number) initially
    movements = calculate_head_movements(left[::-1], initial_position)
    if right:
        movements += abs(left[0] - 0)
        movements += abs(4999 - 0)
        movements += calculate_head_movements(right, 4999)
    return movements

# with basic c-scan, when the head reaches the end, it jumps to the beginning of the opposite direction (0 / 4999),
# with the optimized version, it jumps to the closest request in the opposite direction
def optimized_cscan(requests, initial_position):
    requests.sort()
    left = [r for r in requests if r < initial_position]
    right = [r for r in requests if r >= initial_position]
    movements = 0

    if right:
        movements += calculate_head_movements(right, initial_position)
        if left:
            optimal_jump = min(left, key=lambda x: abs(4999 - x))
            movements += abs(right[-1] - optimal_jump)
            movements += calculate_head_movements(left, optimal_jump)
    else:
        # Service left requests if no right requests
        optimal_jump = min(left, key=lambda x: abs(4999 - x))
        movements += abs(initial_position - optimal_jump)
        movements += calculate_head_movements(left, optimal_jump)

    return movements

if __name__ == "__main__":
    initial_position = int(sys.argv[1])
    filename = sys.argv[2]
  
    requests_fcfs = read_requests(filename)
    requests_scan = requests_fcfs.copy()
    requests_cscan = requests_fcfs.copy()
    
    print("FCFS Total Movements:", fcfs(requests_fcfs, initial_position))
    print("SCAN Total Movements:", scan(requests_scan, initial_position))
    print("C-SCAN Total Movements:", c_scan(requests_cscan, initial_position))

    print("Optimized FCFS Total Movements:", optimized_fcfs(requests_fcfs, initial_position))
    print("Optimized SCAN Total Movements:", optimized_scan(requests_scan, initial_position))
    print("Optimized C-SCAN Total Movements:", optimized_cscan(requests_cscan, initial_position))
    