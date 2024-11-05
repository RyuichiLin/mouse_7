#---------------------------------- FILE INFO ---------------------------------#
#                                                                              #
# Project       : Micromouse Simulation                                        #
# Filename      : tests.py                                                     #
# Author        : Team Kirbo                                                   #
# Revision      : 1.0                                                          #
# Updated       : 2024-10-6                                                    #
#                                                                              #
# Contains function definitions to run various Micromouse tests.               #
#                                                                              #
#-------------------------------- END FILE INFO -------------------------------#

#----------------------------- SPHINX FILE HEADER -----------------------------#
"""
tests.py

This file contains test function definitions to run various Micromouse tests.
"""
#--------------------------- END SPHINX FILE HEADER ---------------------------#

#------------------------------------------------------------------------------#
#                                Import Files                                  #
#------------------------------------------------------------------------------#
import matplotlib.pyplot as plt
import numpy as np
import logging
from maze import *

#------------------------------------------------------------------------------#
#                                  Definitions                                 #
#------------------------------------------------------------------------------#
__all__ = ['run_threshold_test']

#------------------------------------------------------------------------------#
#                               Global Variables                               #
#------------------------------------------------------------------------------#
# None

#------------------------------------------------------------------------------#
#                      Private Exceptions (DO NOT EXPORT)                      #
#------------------------------------------------------------------------------#
# None

#------------------------------------------------------------------------------#
#                               Public Exceptions                              #
#------------------------------------------------------------------------------#
# None

#------------------------------------------------------------------------------#
#                        Private Classes (DO NOT EXPORT)                       #
#------------------------------------------------------------------------------#
# None

#------------------------------------------------------------------------------#
#                                Public Classes                                #
#------------------------------------------------------------------------------#
# None

#------------------------------------------------------------------------------#
#                       Private Functions (DO NOT EXPORT)                      #
#------------------------------------------------------------------------------#
# None

#------------------------------------------------------------------------------#
#                                Public Functions                              #
#------------------------------------------------------------------------------#
def run_diagonal_threshold_test(wall_length, wall_width, post_length, 
    start_distance, end_distance, threshold
):
    """
    Run a test to determine the best thresholds for diagonal IR sensors.

    Args:
        wall_length  (float):  Length (long side) of micromouse maze wall
        wall_width   (float):  Width (short side) of micromouse maze wall
        post_length  (float):  Side length of micromouse maze post
        start_distance (int):  Distance to start checking for a left/right wall
        end_distance   (int):  Distance to end checking for a left/right wall
        threshold      (int):  Threshold to determine left/right wall presence
    """
    vertical_wall_matrix = [
        " | ",
        "|  ",
        " | "
    ]
    horizontal_wall_matrix = [
        "  ",
        "- ",
        "- ",
        " -"
    ]
    move_forward_1_distance = wall_length + post_length
    
    # Initialize maze
    test_maze = Maze(
        len(vertical_wall_matrix), len(horizontal_wall_matrix[0]), 
        wall_length, wall_width, post_length,
        vertical_wall_matrix, horizontal_wall_matrix
    )
    distance_traveled = []
    diagonal_readings_list = [
        [], [], [], [], [], [], [], [], []
    ]
    mouse_x_offsets_list = [0.0, -35.0, 35.0]
    mouse_y_offsets_list = [0.0, -35.0, 35.0]
    movement_divisions = 100
    movement_unit = move_forward_1_distance / movement_divisions
    
    # Move mouse up the cooridor
    reading_list_index = 0
    for x_offset in mouse_x_offsets_list:
        for y_offset in mouse_y_offsets_list:
            #plt.figure(figsize=(8, 8))
            #plt.gca().set_aspect('equal', adjustable='box')
            test_maze.move_mouse(1, 2)
            test_maze.mouse.move_mouse(x_offset, y_offset)
            #test_maze.plot_maze()
            for i in range(movement_divisions):
                test_maze.mouse.move_mouse(0, movement_unit)
                left_diagonal_reading = test_maze.get_sensor_distances()[1]
                if left_diagonal_reading is not None:
                    adc_reading = \
                        test_maze.mouse \
                        .convert_distance_to_adc(left_diagonal_reading)
                    diagonal_readings_list[reading_list_index] \
                        .append(adc_reading)
                    #test_maze.mouse \
                    #    .plot_line_from_left_diagonal_sensor(left_diagonal_reading)
                else:
                    diagonal_readings_list[reading_list_index] \
                        .append(1024)
            reading_list_index += 1
            #test_maze.mouse.plot_mouse()

    # Plot results
    distance_traveled = [i for i in range(1, 101)]
    for i in range(reading_list_index):
        if i % 9 == 0:
            plt.figure(figsize=(5,5))
            plt.xticks([i for i in range(0, 101, 2)])
            plt.yticks([i for i in range(0, 1024, 5)])
            plt.grid(True, which='both')
        plt.plot(
            distance_traveled, 
            diagonal_readings_list[i], 
            linestyle='-', 
            color=(
                (i / (reading_list_index - 1)) * 1.0, 
                (i / (reading_list_index - 1)) * 0.8, 
                (i / (reading_list_index - 1)) * 0.6), 
            ms=1,
            label=(str(i))
        )
        plt.legend(loc='best')
    plt.show()

    # Run test for provided start/end distances and wall presence threshold
    logging.basicConfig(
        filename='diagonal_simulation_results.log', 
        level=logging.INFO, 
        format='%(message)s'
    )
    readings = []
    passed_items = []
    movement_divisions = 10
    movement_unit = \
        (move_forward_1_distance 
        * ((end_distance - start_distance) / 100) 
        / movement_divisions)
    start_offset = \
        (move_forward_1_distance * (start_distance / 100))
    test_summary = [
        [0, None, None], 
        [0, None, None], 
        [0, None, None], 
        [0, None, None], 
        [0, None, None], 
        [0, None, None], 
        [0, None, None], 
        [0, None, None], 
        [0, None, None]
    ]
    test_summary_index = 0
    for x_offset in mouse_x_offsets_list:
        for y_offset in mouse_y_offsets_list:
            for angle in range(-44, 45):
                test_maze.move_mouse(1, 2)
                test_maze.mouse.move_mouse(x_offset, y_offset)
                test_maze.mouse.rotate_mouse(angle)
                for i in range(movement_divisions):
                    test_maze.mouse.move_mouse(0, movement_unit)
                    left_diagonal_reading = test_maze.get_sensor_distances()[1]
                    if left_diagonal_reading is not None:
                        adc_reading = \
                            test_maze.mouse \
                            .convert_distance_to_adc(left_diagonal_reading)
                        readings.append(adc_reading)
                    else:
                        readings.append(1024)
                average_reading = sum(readings) / len(readings)
                if average_reading < threshold:
                    logging.info(
                        f"PASSED: x: {x_offset}, y: {y_offset}, ang: {angle} "
                        + f" readings: {readings}"
                    )
                    passed_items.append(
                        [x_offset, y_offset, angle]
                    )
                    test_summary[test_summary_index][0] += 1
                    if test_summary[test_summary_index][1] is None:
                        test_summary[test_summary_index][1] = angle
                        test_summary[test_summary_index][2] = angle
                    else:
                        if angle < test_summary[test_summary_index][1]:
                            test_summary[test_summary_index][1] = angle
                        if angle > test_summary[test_summary_index][2]:
                            test_summary[test_summary_index][2] = angle
                else:
                    logging.info(
                        f"FAILED: x: {x_offset}, y: {y_offset}, ang: {angle} "
                        f" readings: {readings}"
                    )
                test_maze.mouse.rotate_mouse(-angle)
                readings.clear()
            test_summary_index += 1
    
    logging.info("Summary of passed cases [x_offset, y_offset, angle]:")
    test_summary_index = 0
    for x_offset in mouse_x_offsets_list:
        for y_offset in mouse_y_offsets_list:
            logging.info(
                f"x: {x_offset}, y: {y_offset}- "
                f"{test_summary[test_summary_index][0]} angles passed, "
                f"min angle: {test_summary[test_summary_index][1]}, "
                f"max angle: {test_summary[test_summary_index][2]}"
            )
            test_summary_index += 1
    for item in passed_items:
        logging.info(f"{item}")
    print("completed diagonal threshold test")


def run_forward_threshold_test(wall_length, wall_width, post_length, 
    threshold
):
    """
    Run a test to determine the best thresholds for forward IR sensors.

    Args:
        wall_length  (float):  Length (long side) of micromouse maze wall
        wall_width   (float):  Width (short side) of micromouse maze wall
        post_length  (float):  Side length of micromouse maze post
        threshold      (int):  Threshold to determine forward wall presence
    """
    vertical_wall_matrix = [
        "||",
        "||"
    ]
    horizontal_wall_matrix = [
        "-",
        " ",
        "-"
    ]
    move_left_distance = 70
    
    # Initialize maze
    test_maze = Maze(
        len(vertical_wall_matrix), len(horizontal_wall_matrix[0]), 
        wall_length, wall_width, post_length,
        vertical_wall_matrix, horizontal_wall_matrix
    )
    distance_traveled = []
    forward_readings_list = []
    mouse_y_offsets_list = [0.0, -35.0, 35.0]
    movement_divisions = 100
    movement_unit = move_left_distance / movement_divisions

    # Move right across the square
    reading_list_index = 0
    for y_offset in mouse_y_offsets_list:
        for angle in range(-10, 10):
            forward_readings_list.append([])
            #plt.figure(figsize=(8, 8))
            #plt.gca().set_aspect('equal', adjustable='box')
            test_maze.move_mouse(0, 1)
            test_maze.mouse.move_mouse(-35, y_offset)
            test_maze.mouse.rotate_mouse(angle)
            #test_maze.plot_maze()
            
            for i in range(movement_divisions):
                test_maze.mouse.move_mouse(movement_unit, 0)
                left_forward_reading = test_maze.get_sensor_distances()[0]
                right_forward_reading = test_maze.get_sensor_distances()[3]
                if left_forward_reading is not None:
                    adc_reading = \
                        test_maze.mouse \
                        .convert_distance_to_adc(left_forward_reading)
                    forward_readings_list[reading_list_index] \
                        .append(adc_reading)
                    #test_maze.mouse \
                    #    .plot_line_from_left_forward_sensor(left_forward_reading)
                    #test_maze.mouse \
                    #    .plot_line_from_right_forward_sensor(right_forward_reading)
                else:
                    forward_readings_list[reading_list_index] \
                        .append(1024)
            reading_list_index += 1
            #test_maze.mouse.plot_mouse()
            test_maze.mouse.rotate_mouse(-angle)
    
    # Plot results
    distance_traveled = [i for i in range(1, 101)]
    for i in range(reading_list_index):
        if i == 0:
            plt.figure(figsize=(5,5))
            plt.xticks([i for i in range(0, 101, 2)])
            plt.yticks([i for i in range(0, 1024, 5)])
            plt.grid(True, which='both')
        plt.plot(
            distance_traveled, 
            forward_readings_list[i], 
            linestyle='-', 
            color=(
                (i / (reading_list_index - 1)) * 1.0, 
                (i / (reading_list_index - 1)) * 0.8, 
                (i / (reading_list_index - 1)) * 0.6), 
            ms=1,
            label=(str(i))
        )
        plt.legend(loc='best')
    plt.show()

    # Run test for provided wall presence threshold
    logging.basicConfig(
        filename='forward_simulation_results.log', 
        level=logging.INFO, 
        format='%(message)s'
    )
    readings = []
    passed_items = []
    test_summary = [
        [0, None, None],
        [0, None, None],
        [0, None, None]
    ]
    test_summary_index = 0
    for y_offset in mouse_y_offsets_list:
        for angle in range(-44, 45):
            test_maze.move_mouse(0, 1)
            test_maze.mouse.move_mouse(0, y_offset)
            test_maze.mouse.rotate_mouse(angle)
            
            left_forward_reading, _, _, right_forward_reading = \
                test_maze.get_sensor_distances()
            if ((left_forward_reading is not None) and 
                    (right_forward_reading is not None)):
                adc_reading_1 = test_maze.mouse \
                    .convert_distance_to_adc(left_forward_reading)
                adc_reading_2 = test_maze.mouse \
                    .convert_distance_to_adc(right_forward_reading)
                average_reading = (adc_reading_1 + adc_reading_2) // 2
                readings.append(average_reading)
            else:
                readings.append(1024)
            
            if average_reading < threshold:
                logging.info(
                    f"PASSED: y: {y_offset}, ang: {angle} "
                    f"average_reading: {average_reading}"
                )
                passed_items.append(
                    [y_offset, angle]
                )
                test_summary[test_summary_index][0] += 1
                if test_summary[test_summary_index][1] is None:
                    test_summary[test_summary_index][1] = angle
                    test_summary[test_summary_index][2] = angle
                else:
                    if angle < test_summary[test_summary_index][1]:
                        test_summary[test_summary_index][1] = angle
                    if angle > test_summary[test_summary_index][2]:
                        test_summary[test_summary_index][2] = angle
            else:
                logging.info(
                    f"FAILED: y: {y_offset}, ang: {angle} "
                    f"average_reading: {average_reading}"
                )
            test_maze.mouse.rotate_mouse(-angle)
        test_summary_index += 1
    
    logging.info("Summary of passed cases [y_offset, angle]:")
    test_summary_index = 0
    for y_offset in mouse_y_offsets_list:
        logging.info(
            f"y: {y_offset}- "
            f"{test_summary[test_summary_index][0]} angles passed, "
            f"min angle: {test_summary[test_summary_index][1]}, "
            f"max angle: {test_summary[test_summary_index][2]}"
        )
        test_summary_index += 1
    for item in passed_items:
        logging.info(f"{item}")
    print("completed forward threshold test")

def run_turn_90_deg_pid_test(motor_base_speed, pid_kp, pid_kd):
    """
    Run a test to determine the best PD constants and base speed for turning
    90 degrees.

    Args:
        motor_base_speed (int): Base speed to test
        pid_kp (float): kp value to test
        pid_kd (float): kd value to test
    """
    vertical_wall_matrix = [
        "  ",
    ]
    horizontal_wall_matrix = [
        " ",
        " ",
    ]
    
    # Initialize maze
    test_maze = Maze(
        len(vertical_wall_matrix), len(horizontal_wall_matrix[0]), 
        0, 0, 0,
        vertical_wall_matrix, horizontal_wall_matrix
    )

    # Simulate turning right on all possible values
    logging.basicConfig(
        filename='turn_90_deg_simulation_results.log', 
        level=logging.INFO, 
        format='%(message)s'
    )
    min_total_error = None
    min_center_shift = None
    min_angle_error = None
    max_total_error = None
    max_center_shift = None
    max_angle_error = None

    for speed in range(90, 230, 10):
        min_total_error = None
        min_center_shift = None
        min_angle_error = None
        max_total_error = None
        max_center_shift = None
        max_angle_error = None
        for kp in np.arange(0, 10.1, 0.1):
            for kd in np.arange(0, 1.1, 0.1):
                test_maze.move_mouse(0, 0)
                angle = test_maze.mouse.get_mouse_angle()
                test_maze.mouse.rotate_mouse(-angle)

                total_error, center_shift, angle_error = \
                    test_maze.mouse.simulate_turn_right_90_degrees_pid(
                        speed, 
                        kp, 
                        kd, 
                        0.1
                    )
                if min_total_error is None:
                    min_total_error = total_error
                elif total_error < min_total_error:
                    min_total_error = total_error
                
                if min_center_shift is None:
                    min_center_shift = center_shift
                elif center_shift < min_center_shift:
                    min_center_shift = center_shift

                if min_angle_error is None:
                    min_angle_error = abs(angle_error)
                elif abs(angle_error) < min_angle_error:
                    min_angle_error = abs(angle_error)

                if max_total_error is None:
                    max_total_error = total_error
                elif total_error > max_total_error:
                    max_total_error = total_error
                
                if max_center_shift is None:
                    max_center_shift = center_shift
                elif center_shift > max_center_shift:
                    max_center_shift = center_shift

                if max_angle_error is None:
                    max_angle_error = abs(angle_error)
                elif abs(angle_error) > max_angle_error:
                    max_angle_error = abs(angle_error)
        logging.info(
            f"base speed: {speed}- "
            f"min, max total error: {min_total_error}, {max_total_error}; "
            f"min, max center_shift: {min_center_shift}, {max_center_shift}; "
            f"min, max angle error: {min_angle_error}, {max_angle_error}; "
        )

    # Run test on provided base speed and PID constants
    results_list = np.empty((0,5))

    logging.info(f"testing base speed {motor_base_speed}:")
    for kp in np.arange(0, 10.1, 0.1):
        for kd in np.arange(0, 1.1, 0.1):
            test_maze.move_mouse(0, 0)
            angle = test_maze.mouse.get_mouse_angle()
            test_maze.mouse.rotate_mouse(-angle)

            total_error, center_shift, angle_error = \
                test_maze.mouse.simulate_turn_right_90_degrees_pid(
                    motor_base_speed, 
                    kp, 
                    kd, 
                    0.1
                )
            new_row = np.array([total_error, center_shift, abs(angle_error), kp, kd])
            results_list = np.vstack([results_list, new_row])

    lowest_total_error_rows = \
        results_list[np.argsort(results_list[:, 0])][:50]

    lowest_center_shift_rows = \
        results_list[np.argsort(results_list[:, 1])][:50]

    lowest_angle_error_rows = \
        results_list[np.argsort(results_list[:, 2])][:50]

    logging.info("\ntop 50 lowest total_error:")
    for row in lowest_total_error_rows:
        logging.info(f"{row.tolist()}")

    logging.info("\ntop 50 lowest center_shift:")
    for row in lowest_center_shift_rows:
        logging.info(f"{row.tolist()}")

    logging.info("\ntop 50 lowest angle_error:")
    for row in lowest_angle_error_rows:
        logging.info(f"{row.tolist()}")

    print("completed turn 90 deg test")

#------------------------------------------------------------------------------#
#                                     MAIN                                     #
#------------------------------------------------------------------------------#
def main():
    #run_diagonal_threshold_test(166.37, 12.065, 12.065, 30, 40, 120)
    #run_forward_threshold_test(166.37, 12.065, 12.065, 70)
    run_turn_90_deg_pid_test(90, 0, 0)

# Example usage
if __name__ == "__main__":
    main()
