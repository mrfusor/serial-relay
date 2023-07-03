#!/usr/bin/env python3
import sys
import curses
import subprocess
import time
import random

def execute_relay_command(relay_script, relay_index, relay_state):
    command = [relay_script, str(relay_index), relay_state]
    subprocess.run(command, check=True)

def toggle_all_relays(relay_script, relay_states_dict, relay_states, toggle_state):
    new_relay_state = relay_states[toggle_state]
    for i in range(1, 17):
        relay_states_dict[i] = new_relay_state
        execute_relay_command(relay_script, i, new_relay_state)
    # Update the state of "Relay 0" as well
    relay_states_dict[0] = new_relay_state

def toggle_relays_in_order(relay_script, relay_states_dict, relay_states, delay):
    for i in range(1, 17):
        relay_state = relay_states_dict[i]
        new_relay_state = relay_states[(relay_states.index(relay_state) + 1) % len(relay_states)]
        execute_relay_command(relay_script, i, new_relay_state)
        relay_states_dict[i] = new_relay_state
        time.sleep(delay)

def toggle_relays_randomly(relay_script, relay_states_dict, relay_states, delay):
    relay_indices = list(range(1, 17))
    random.shuffle(relay_indices)
    for relay_index in relay_indices:
        relay_state = relay_states_dict[relay_index]
        new_relay_state = relay_states[(relay_states.index(relay_state) + 1) % len(relay_states)]
        execute_relay_command(relay_script, relay_index, new_relay_state)
        relay_states_dict[relay_index] = new_relay_state
        time.sleep(delay)

def main(stdscr):
    relay_script = './relay.py'  # Relay control script
    relay_states = ['-off', '-on']  # Possible states for the relays

    # Initialize the terminal
    stdscr.nodelay(1)
    stdscr.timeout(100)

    # Set up initial relay states
    relay_states_dict = {i: relay_states[0] for i in range(17)}
    relay_index = 0  # Initialize relay_index

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Display instructions and relay status
        stdscr.addstr(0, 0, "Use arrow keys to select a relay or option. Press ENTER to toggle its state. Press 'q' to quit.")

        # Display additional menu options
        stdscr.addstr(2, 0, "Toggle All in Order")
        stdscr.addstr(3, 0, "Toggle All Randomly")

        # Display relay states
        for i in range(17):
            relay_state = relay_states_dict[i]
            cursor = " >> " if i == relay_index else "    "
            stdscr.addstr(5 + i, 0, cursor + "Relay {}: {}".format(i, relay_state))

        # Get user input
        key = stdscr.getch()

        # Process user input
        if key == curses.KEY_UP:
            relay_index = max(0, relay_index - 1)
        elif key == curses.KEY_DOWN:
            relay_index = min(16, relay_index + 1)
        elif key == ord('\n'):
            # Toggle the state of the selected relay
            if relay_index == 0:
                # Toggle all relays based on relay 0 state
                toggle_state = relay_states.index(relay_states_dict[0])
                toggle_state = (toggle_state + 1) % len(relay_states)
                toggle_all_relays(relay_script, relay_states_dict, relay_states, toggle_state)
            else:
                # Toggle a single relay
                relay_state = relay_states_dict[relay_index]
                new_relay_state = relay_states[(relay_states.index(relay_state) + 1) % len(relay_states)]
                execute_relay_command(relay_script, relay_index, new_relay_state)
                relay_states_dict[relay_index] = new_relay_state
        elif key == ord('o'):
            # Toggle all relays in order with a delay
            delay = 0.1  # Delay between toggling relays (adjust as needed)
            toggle_relays_in_order(relay_script, relay_states_dict, relay_states, delay)
        elif key == ord('r'):
            # Toggle all relays in random order with a delay
            delay = 0.1  # Delay between toggling relays (adjust as needed)
            toggle_relays_randomly(relay_script, relay_states_dict, relay_states, delay)
        elif key == ord('q'):
            break

if __name__ == '__main__':
    curses.wrapper(main)
