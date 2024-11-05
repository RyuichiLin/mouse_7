#---------------------------------- FILE INFO ---------------------------------#
#                                                                              #
# Project       : Micromouse Simulation                                        #
# Filename      : mouse.py                                                     #
# Author        : Team Kirbo                                                   #
# Revision      : 1.0                                                          #
# Updated       : 2024-10-6                                                    #
#                                                                              #
# Contains class and method definitions for mouse class.                       #
#                                                                              #
#-------------------------------- END FILE INFO -------------------------------#

#----------------------------- SPHINX FILE HEADER -----------------------------#
"""
mouse.py

This file contains class and method definitions for the mouse class.
"""
#--------------------------- END SPHINX FILE HEADER ---------------------------#

#------------------------------------------------------------------------------#
#                                Import Files                                  #
#------------------------------------------------------------------------------#
import matplotlib.pyplot as plt
import numpy as np
import math

#------------------------------------------------------------------------------#
#                                  Definitions                                 #
#------------------------------------------------------------------------------#
__all__ = ['Mouse']

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
class Mouse:
    """
    Mouse class to simulate a micromouse.

    Includes movement and sensor reading methods to simulate a mouse in a maze.

    Attributes:
        center_x  (float): Center of mouse movement x coordinate
        center_y  (float): Center of mouse movement y coordinate
        
        hitbox_bottom_left  (List[float]): Bottom left corner of mouse hitbox
        hitbox_top_left     (List[float]): Top left corner of mouse hitbox
        hitbox_top_right    (List[float]): Top right corner of mouse hitbox
        hitbox_bottom_right (List[float]): Bottom right corner of mouse hitbox
        
        wheel_left_back     (List[float]): Left back wheel of mouse
        wheel_left_front    (List[float]): Left front wheel of mouse
        wheel_right_back    (List[float]): Right back wheel of mouse
        wheel_right_front   (List[float]): Right front wheel of mouse
        
        sensor_forward_left_tip    (List[float]): Left forward sensor tip
        sensor_forward_left_back   (List[float]): Left forward sensor back
        sensor_diagonal_left_tip   (List[float]): Left diagonal sensor tip
        sensor_diagonal_left_back  (List[float]): Left diagonal sensor back
        sensor_diagonal_right_tip  (List[float]): Right diagonal sensor tip
        sensor_diagonal_right_back (List[float]): Right diagonal sensor back
        sensor_forward_right_tip   (List[float]): Right forward sensor tip
        sensor_forward_right_back  (List[float]): Right forward sensor back

        all_points_list (List[List[float]]): List of all points

        encoder_count_per_turn (int): Edges observed per 90 deg turn
    """
    def __init__(self, center_x, center_y):
        """
        Initializes Mouse instance.

        Args:
            center_x (float): Mouse center of movement x coordinate
            center_y (float): Mouse center of movement y coordinate
        """
        self.center_x = center_x
        self.center_y = center_y

        # Below are coordinates calculated specifically for mouse 7
        self.hitbox_bottom_left = [center_x - 45.2, center_y - 32.03]
        self.hitbox_top_left = [center_x - 45.2, center_y + 56.97]
        self.hitbox_top_right = [center_x + 45.2, center_y + 56.97]
        self.hitbox_bottom_right = [center_x + 45.2, center_y - 32.03]
        self.wheel_left_back = [center_x - 43.3, center_y - 17.5]
        self.wheel_left_front = [center_x - 43.3, center_y + 17.5]
        self.wheel_right_back = [center_x + 43.3, center_y - 17.5]
        self.wheel_right_front = [center_x + 43.3, center_y + 17.5]
        self.sensor_forward_left_tip = [center_x - 27.58, center_y + 37.92]
        self.sensor_forward_left_back = [center_x - 27.58, center_y + 30.42]
        self.sensor_diagonal_left_tip = [center_x - 17.67, center_y + 51.46]
        self.sensor_diagonal_left_back = [center_x - 12.36, center_y + 46.15]
        self.sensor_diagonal_right_tip = [center_x + 17.67, center_y + 51.46]
        self.sensor_diagonal_right_back = [center_x + 12.36, center_y + 46.15]
        self.sensor_forward_right_tip = [center_x + 27.58, center_y + 37.92]
        self.sensor_forward_right_back = [center_x  + 27.58, center_y + 30.42]

        self.all_points_list = [
            self.hitbox_bottom_left,
            self.hitbox_top_left,
            self.hitbox_top_right,
            self.hitbox_bottom_right,
            self.wheel_left_back,
            self.wheel_left_front,
            self.wheel_right_back,
            self.wheel_right_front,
            self.sensor_forward_left_tip,
            self.sensor_forward_left_back,
            self.sensor_diagonal_left_tip,
            self.sensor_diagonal_left_back,
            self.sensor_diagonal_right_tip,
            self.sensor_diagonal_right_back,
            self.sensor_forward_right_tip,
            self.sensor_forward_right_back
        ]

        # Below encoder calculation is specific to mouse 7

        # ServoCity N20 4900 RPM motor: 60.8077 countable events per revolution
        # 3D printed gear ratio: 44:13
        # Wheel circumference = 103mm
        # Wheel to Wheel distance = 86.6mm
        # [Rising edges / revolution] = (60.8077*44:13)/4 = 51.453
        # [Rising edges / mm] = 51.453/103 = 0.4995
        # [Rising edges / 90 deg turn] = ((pi*86.6)/4)*(0.4995) = 33
        self.encoder_count_per_turn = 33

    def get_encoder_count_per_move_forward(
        self, wall_length, post_length
    ) -> int:
        """
        Calculate encoder rising edges observed per move forward.

        Args:
            wall_length  (float):  Length (long side) of micromouse maze wall
            post_length  (float):  Side length of micromouse maze post
        """
        return_result = int((wall_length + post_length) * (0.49954))

        return return_result

    def _simulate_get_encoder_count(self, motor_speed, time_elapsed) -> float:
        """
        Calculate encoder counts observed on a motor after time_elapsed.

        Args:
            motor_speed  (int): Motor speed from 0-255
            time_elapsed (float): Time elapsed in ms at motor_speed

        Returns:
            (float): Number of encoder edges observed.
        """
        # 4900RPM w/ 13:44 added gear ratio -> 2.4129 revolutions per ms
        # [revolutions / ms] = 2.4129*(motor_speed/255)
        # [encoder count / ms] = (2.4129*(motor_speed/255))*51.453
        return_result = (2.4129*(motor_speed/255))*51.453 * time_elapsed

        return return_result

    def plot_mouse(self):
        """
        Display mouse on xy plane w/ matplotlib
        """
        rectangle_coordinates = [
            tuple(self.hitbox_bottom_left),
            tuple(self.hitbox_top_left),
            tuple(self.hitbox_top_right),
            tuple(self.hitbox_bottom_right)
        ]

        # Hitbox
        x_values, y_values = zip(*rectangle_coordinates)
        x_values += (x_values[0],)
        y_values += (y_values[0],)
        plt.plot(x_values, y_values, marker='o', linestyle='-', color='b', ms=1)

        # All other lines
        line_coordinates_list = [
            [tuple(self.wheel_left_back), 
            tuple(self.wheel_left_front)],

            [tuple(self.wheel_right_back), 
            tuple(self.wheel_right_front)],

            [tuple(self.sensor_forward_left_back), 
            tuple(self.sensor_forward_left_tip)],

            [tuple(self.sensor_diagonal_left_back), 
            tuple(self.sensor_diagonal_left_tip)],

            [tuple(self.sensor_diagonal_right_back), 
            tuple(self.sensor_diagonal_right_tip)],

            [tuple(self.sensor_forward_right_back), 
            tuple(self.sensor_forward_right_tip)]
        ]

        for coordinates in line_coordinates_list:
            x_values, y_values = zip(*coordinates)
            plt.plot(x_values, y_values, linestyle='-', color='b', ms=1)

    def move_mouse(self, shift_x, shift_y):
        """
        Shift mouse by shift_x and shift_y amount.

        Args:
            shift_x (float): Amount to shift mouse x coordinate
            shift_y (float): Amount to shift mouse y coordinate
        """
        self.center_x += shift_x
        self.center_y += shift_y

        # Works because lists are mutable- each list item points to 
        # each class attribute
        for coordinate in self.all_points_list:
            coordinate[0] += shift_x
            coordinate[1] += shift_y

    def rotate_mouse(self, angle_degrees):
        """
        Rotate mouse counter-clockwise by angle amount in degrees.

        Negative values rotates the mouse clockwise.

        Args:
            angle_degrees (int): Degrees to rotate mouse
        """
        angle_radians = np.radians(angle_degrees)

        rotation_matrix = \
            np.array([[np.cos(angle_radians), -np.sin(angle_radians)],
                      [np.sin(angle_radians), np.cos(angle_radians)]])

        for coordinate in self.all_points_list:
            new_coordinate = \
                np.array(coordinate) - np.array([self.center_x, self.center_y])
            new_coordinate = \
                (new_coordinate @ rotation_matrix.T 
                + np.array([self.center_x, self.center_y]))
            coordinate[0] = new_coordinate[0]
            coordinate[1] = new_coordinate[1]

    def get_mouse_angle(self):
        """
        Calculate the angle of the mouse relative to the x-axis.

        Returns negative angle if below x-axis, and positive if above x-axis.

        Returns:
            (int): Angle of mouse in degrees.
        """
        x1, y1 = self.hitbox_bottom_left
        x2, y2 = self.hitbox_bottom_right

        angle_radians = math.atan2(y2 - y1, x2 - x1)
        angle_degrees = math.degrees(angle_radians)

        return angle_degrees

    def _calculate_intersection_distance(
        self, sensor_tip_coordinates, direction_vector,
        line_coordinates_1, line_coordinates_2
    ) -> float:
        """
        Calculate distance between a line segment and IR sensor if the IR
        sensor is facing the line segment.

        Internal helper method used in sensor specific method definitions.

        Args:
            sensor_tip_coordinates (List[float]): IR sensor tip coordinates
            direction_vector       (List[float]): IR sensor direction vector
            line_coordinates_1     (List[float]): Line segment coordinates 1
            line_coordinates_2     (List[float]): Line segment coordinates 2

        Returns:
            (float): Distance to line segment; None if not facing line segment
        """
        return_result = None

        ray_dir = np.array(direction_vector)
        segment_dir = \
            np.array(line_coordinates_2) - np.array(line_coordinates_1)

        A = np.array([[ray_dir[0], -segment_dir[0]],
                      [ray_dir[1], -segment_dir[1]]])
        B = np.array([line_coordinates_1[0] - sensor_tip_coordinates[0], 
                      line_coordinates_1[1] - sensor_tip_coordinates[1]])

        try:
            # Solve the system A * [t, u] = B
            t, u = np.linalg.solve(A, B)
            
            # Check if the solution is within valid range
            if t >= 0 and 0 <= u <= 1:
                intersection_point = sensor_tip_coordinates + t * ray_dir
                
                # Calculate distance between sensor tip and intersection point
                return_result = \
                    np.linalg.norm(intersection_point - sensor_tip_coordinates)

                # Plot intersection for debug
                # plt.scatter(intersection_point[0], intersection_point[1], 
                #    s=5, c='red', marker='x')

        except np.linalg.LinAlgError:
            return_result = None

        return return_result

    def _plot_line_from_sensor(self, sensor_tip_coordinates, direction_vector, 
            distance):
        """
        Plot a line of length "distance" from sensor tip.

        Internal helper method to draw line from sensor after finding minimum
        obstacle distance.

        Args:
            sensor_tip_coordinates (List[float]): IR sensor tip coordinates
            direction_vector       (List[float]): IR sensor direction vector
            distance               (float): Distance from sensor to plot line
        """
        ray_dir = np.array(direction_vector)
        dir_unit = ray_dir / np.linalg.norm(ray_dir)

        end_point = sensor_tip_coordinates + (distance * dir_unit)

        plt.plot(
            [sensor_tip_coordinates[0], end_point[0]], 
            [sensor_tip_coordinates[1], end_point[1]], 
            linestyle=':', color='r', ms=1
        )
    
    def get_left_forward_sensor_distance(
        self, 
        line_coordinates_1, line_coordinates_2):
        """
        Calculate distance between a line segment and left forward facing IR 
        sensor if the IR sensor is facing the line segment.

        Args:
            line_coordinates_1 (List[float]): Line segment coordinates 1
            line_coordinates_2 (List[float]): Line segment coordinates 2

        Returns:
            (float): Distance to line segment; None if not facing line segment
        """
        return_result = None

        direction_vector = [
            self.sensor_forward_left_tip[0] - self.sensor_forward_left_back[0],
            self.sensor_forward_left_tip[1] - self.sensor_forward_left_back[1]
        ]

        return_result = self._calculate_intersection_distance(
            self.sensor_forward_left_tip, direction_vector, 
            line_coordinates_1, line_coordinates_2
        )

        return return_result

    def get_left_diagonal_sensor_distance(
        self, 
        line_coordinates_1, line_coordinates_2):
        """
        Calculate distance between a line segment and left diagonal facing IR 
        sensor if the IR sensor is facing the line segment.

        Args:
            line_coordinates_1 (List[float]): Line segment coordinates 1
            line_coordinates_2 (List[float]): Line segment coordinates 2

        Returns:
            (float): Distance to line segment; None if not facing line segment
        """
        return_result = None

        direction_vector = [
            self.sensor_diagonal_left_tip[0] - self.sensor_diagonal_left_back[0],
            self.sensor_diagonal_left_tip[1] - self.sensor_diagonal_left_back[1]
        ]

        return_result = self._calculate_intersection_distance(
            self.sensor_diagonal_left_tip, direction_vector, 
            line_coordinates_1, line_coordinates_2
        )

        return return_result

    def get_right_forward_sensor_distance(
        self, 
        line_coordinates_1, line_coordinates_2):
        """
        Calculate distance between a line segment and right forward facing IR 
        sensor if the IR sensor is facing the line segment.

        Args:
            line_coordinates_1 (List[float]): Line segment coordinates 1
            line_coordinates_2 (List[float]): Line segment coordinates 2

        Returns:
            (float): Distance to line segment; None if not facing line segment
        """
        return_result = None

        direction_vector = [
            self.sensor_forward_right_tip[0] - self.sensor_forward_right_back[0],
            self.sensor_forward_right_tip[1] - self.sensor_forward_right_back[1]
        ]

        return_result = self._calculate_intersection_distance(
            self.sensor_forward_right_tip, direction_vector, 
            line_coordinates_1, line_coordinates_2
        )

        return return_result

    def get_right_diagonal_sensor_distance(
        self, 
        line_coordinates_1, line_coordinates_2):
        """
        Calculate distance between a line segment and right diagonal facing IR 
        sensor if the IR sensor is facing the line segment.

        Args:
            line_coordinates_1 (List[float]): Line segment coordinates 1
            line_coordinates_2 (List[float]): Line segment coordinates 2

        Returns:
            (float): Distance to line segment; None if not facing line segment
        """
        return_result = None

        direction_vector = [
            self.sensor_diagonal_right_tip[0] 
                - self.sensor_diagonal_right_back[0],
            self.sensor_diagonal_right_tip[1] 
                - self.sensor_diagonal_right_back[1]
        ]

        return_result = self._calculate_intersection_distance(
            self.sensor_diagonal_right_tip, direction_vector, 
            line_coordinates_1, line_coordinates_2
        )

        return return_result

    def plot_line_from_left_forward_sensor(self, distance):
        """
        Plot a line of length "distance" from left forward sensor tip.

        Args:
            distance (float): Distance from sensor to plot line
        """
        direction_vector = [
            self.sensor_forward_left_tip[0] - self.sensor_forward_left_back[0],
            self.sensor_forward_left_tip[1] - self.sensor_forward_left_back[1]
        ]

        self._plot_line_from_sensor(
            self.sensor_forward_left_tip, 
            direction_vector, 
            distance)

    def plot_line_from_left_diagonal_sensor(self, distance):
        """
        Plot a line of length "distance" from left diagonal sensor tip.

        Args:
            distance (float): Distance from sensor to plot line
        """
        direction_vector = [
            self.sensor_diagonal_left_tip[0] - self.sensor_diagonal_left_back[0],
            self.sensor_diagonal_left_tip[1] - self.sensor_diagonal_left_back[1]
        ]

        self._plot_line_from_sensor(
            self.sensor_diagonal_left_tip, 
            direction_vector,
            distance)

    def plot_line_from_right_diagonal_sensor(self, distance):
        """
        Plot a line of length "distance" from right diagonal sensor tip.

        Args:
            distance (float): Distance from sensor to plot line
        """
        direction_vector = [
            self.sensor_diagonal_right_tip[0] - self.sensor_diagonal_right_back[0],
            self.sensor_diagonal_right_tip[1] - self.sensor_diagonal_right_back[1]
        ]

        self._plot_line_from_sensor(
            self.sensor_diagonal_right_tip, 
            direction_vector, 
            distance)

    def plot_line_from_right_forward_sensor(self, distance):
        """
        Plot a line of length "distance" from right forward sensor tip.

        Args:
            distance (float): Distance from sensor to plot line
        """
        direction_vector = [
            self.sensor_forward_right_tip[0] - self.sensor_forward_right_back[0],
            self.sensor_forward_right_tip[1] - self.sensor_forward_right_back[1]
        ]

        self._plot_line_from_sensor(
            self.sensor_forward_right_tip,
            direction_vector,
            distance)
    
    def convert_distance_to_adc(self, distance) -> int:
        """
        Convert distance between IR sensor and obstacle to ADC reading

        Args:
            distance (float): Distance between IR sensor and obstacle in mm

        Returns:
            (int): ADC reading corresponding to distance
        """
        return_result = 0

        # Equation below found via exponential regression fit of SHARP sensor
        # The equation takes distance in cm
        output_voltage = (2.71272) * (0.858585 ** (distance / 10))
        return_result = ((output_voltage * (2.2 / (1 + 2.2))) / 1.8) * 1024

        # Constrain result to 0-1024
        return_result = max(0, min(int(return_result), 1024))

        return return_result

    def _simulate_mouse_movement(self, motor_1_speed, motor_2_speed, time):
        """
        Simulate the mouse being driven by two motors.

        Update mouse position and orientation after "time" provided two motor
        speeds. Internal helper method for simulate PID movement methods.

        Args:
            motor_1_speed (float): Speed of left motor in PWM (0-255)
            motor_2_speed (float): Speed of right motor in PWM (0-255)
            time (float): Time spent moving in milliseconds
        """
        wheel_to_wheel_distance = math.sqrt(
            ((self.wheel_right_front[0] - self.wheel_left_front[0]) ** 2)
            + ((self.wheel_right_front[1] - self.wheel_left_front[1]) ** 2)
        )

        # Wheel circumference = 103mm
        # [revolutions / ms] = 2.4129*(motor_speed/255)
        # [mm / ms] = (103*2.4129)*(motor_speed/255)
        motor_1_velocity = (103*2.4129)*(motor_1_speed/255)
        motor_2_velocity = (103*2.4129)*(motor_2_speed/255)

        velocity = (motor_1_velocity + motor_2_velocity) / 2
        omega = (motor_2_speed - motor_1_speed) / wheel_to_wheel_distance

        angle_radians = omega * time
        angle_degrees = np.degrees(angle_radians)

        self.rotate_mouse(angle_degrees)

        shift_x = velocity * np.cos(angle_radians) * time
        shift_y = velocity * np.sin(angle_radians) * time
        self.move_mouse(shift_x, shift_y)

    def simulate_turn_right_90_degrees_pid(self, 
        motor_base_speed, pid_kp, pid_kd, update_interval):
        """
        Simulate turning right 90 degrees w/ PID.

        Args:
            motor_base_speed (int): Base speed of two motors from 0 to 255
            pid_kp (float): Proportional constant for feedback control
            pid_kd (float): Derivative constant for feedback control
            update_interval (float): Time in ms to update motor speeds

        Returns:
            Tuple(float, float, int): errors including:
                Total error observed from feedback control
                Mouse center movement distance
                Angle error in degrees
        """
        right_done = False
        left_done = False
        kp = pid_kp
        kd = pid_kd
        target_angle = 0
        prev_error_left = 0
        prev_error_right = 0
        p_error_left = 0
        d_error_left = 0
        p_error_right = 0
        d_error_right = 0
        output_left = 0
        output_right = 0
        left_encoder_count = 0.0
        right_encoder_count = 0.0

        total_error = 0
        original_center = [self.center_x, self.center_y]

        while (not right_done) or (not left_done):
            p_error_right = self.encoder_count_per_turn - (-int(right_encoder_count))
            p_error_left = self.encoder_count_per_turn - int(left_encoder_count)
            d_error_right = p_error_right - prev_error_right
            d_error_left = p_error_left - prev_error_left
            prev_error_right = p_error_right
            prev_error_left = p_error_left

            total_error += (
                abs(p_error_right) 
                + abs(p_error_left)
                + abs(d_error_right)
                + abs(d_error_left)
            )

            output_right = (kp * p_error_right) + (kd * d_error_right)
            output_left = (kp * p_error_left) + (kd * d_error_left)
            new_right_speed = motor_base_speed + output_right
            new_left_speed = motor_base_speed + output_left
            new_right_speed = max(0, min(int(new_right_speed), 255))
            new_left_speed = max(0, min(int(new_left_speed), 255))

            if (not left_done) and (not right_done):
                self._simulate_mouse_movement(
                    new_left_speed, 
                    -new_right_speed, 
                    update_interval
                )
                right_encoder_count -= \
                    self._simulate_get_encoder_count(new_right_speed, update_interval)
                left_encoder_count += \
                    self._simulate_get_encoder_count(new_left_speed, update_interval)
            elif not right_done:
                self._simulate_mouse_movement(
                    new_left_speed, 
                    0, 
                    update_interval
                )
                right_encoder_count -= \
                    self._simulate_get_encoder_count(new_right_speed, update_interval)
            elif not left_done:
                self._simulate_mouse_movement(
                    0, 
                    -new_right_speed, 
                    update_interval
                )
                left_encoder_count += \
                    self._simulate_get_encoder_count(new_left_speed, update_interval)

            self.move_mouse(100, 0)
            self.plot_mouse()

            if ((not left_done) and \
                (left_encoder_count >= self.encoder_count_per_turn)
            ):
                left_done = True

            if ((not right_done) and \
                (right_encoder_count <= -self.encoder_count_per_turn)
            ):
                right_done = True

        center_shift = math.sqrt(
            ((self.center_x - original_center[0]) ** 2)
            + ((self.center_y - original_center[1]) ** 2)
        )

        angle_error = self.get_mouse_angle() + 90

        return total_error, center_shift, angle_error

#------------------------------------------------------------------------------#
#                       Private Functions (DO NOT EXPORT)                      #
#------------------------------------------------------------------------------#
# None

#------------------------------------------------------------------------------#
#                                Public Functions                              #
#------------------------------------------------------------------------------#
# None

#------------------------------------------------------------------------------#
#                                     MAIN                                     #
#------------------------------------------------------------------------------#
def main():
    plt.figure(figsize=(8, 8))

    test_mouse = Mouse(0, 0)
    test_mouse.plot_mouse()
    total_error, center_shift, angle_error = \
        test_mouse.simulate_turn_right_90_degrees_pid(90, 0.4, 0.3, 0.1)
    #test_mouse.plot_mouse()
    print(f"total error: {total_error}, "
          f"center_shift: {center_shift}, "
          f"angle_error: {abs(angle_error)}"
    )

    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

# Example usage
if __name__ == "__main__":
    main()
