#---------------------------------- FILE INFO ---------------------------------#
#                                                                              #
# Project       : Micromouse Simulation                                        #
# Filename      : obstacle.py                                                  #
# Author        : Team Kirbo                                                   #
# Revision      : 1.0                                                          #
# Updated       : 2024-10-6                                                    #
#                                                                              #
# Contains class and method definitions for micromouse maze wall and post      #
# classes                                                                      #
#-------------------------------- END FILE INFO -------------------------------#

#----------------------------- SPHINX FILE HEADER -----------------------------#
"""
obstacle.py

This file contains class and method definitions for the micromouse wall and
post classes.
"""
#--------------------------- END SPHINX FILE HEADER ---------------------------#

#------------------------------------------------------------------------------#
#                                Import Files                                  #
#------------------------------------------------------------------------------#
import matplotlib.pyplot as plt

#------------------------------------------------------------------------------#
#                                  Definitions                                 #
#------------------------------------------------------------------------------#
__all__ = ['Wall', 'Post']

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
class _Obstacle:
    """
    Parent class of Post and Wall classes.

    Serves as an attribute and method template for Post and Wall classes.
    Defines a rectangular obstacle class to be placed in a micromouse maze.

    Attributes:
        center_x (float): X coordinate of obstacle center
        center_y (float): Y coordinate of obstacle center
        horizontal_size (float): h. side of the obstacle in millimeters
        vertical_size   (float): v. side of the obstacle in millimeters
        upper_left_corner   (List[float]): Coordinates of upper left corner
        upper_right_corner: (List[float]): Coordinates of upper right corner
        lower_left_corner:  (List[float]): Coordinates of lower left corner
        lower_right_corner: (List[float]): Coordinates of lower right corner
        visible (bool): Whether obstacle is present or not
    """
    def __init__(self, center_x, center_y, horizontal_size, vertical_size):
        """
        Initializes Obstacle instance.

        Args:
            center_x (float): X coordinate for obstacle center
            center_y (float): Y coordinate for obstacle center
            horizontal_size (float): h. side of the obstacle in millimeters
            vertical_size   (float): v. side of the obstacle in millimeters
        """
        self.center_x = center_x
        self.center_y = center_y
        self.horizontal_size = horizontal_size
        self.vertical_size = vertical_size
        self.upper_left_corner = [
            center_x - (horizontal_size / 2), 
            center_y + (vertical_size / 2) 
        ]
        self.upper_right_corner = [
            center_x + (horizontal_size / 2),
            center_y + (vertical_size / 2)
        ]
        self.lower_left_corner = [
            center_x - (horizontal_size / 2),
            center_y - (vertical_size / 2)
        ]
        self.lower_right_corner = [
            center_x + (horizontal_size / 2),
            center_y - (vertical_size / 2)
        ]
        self.visible = False

    def _set_visible(self):
        """
        Make the obstacle visible (present) on the maze.
        """
        self.visible = True

    def _plot_obstacle(self):
        """
        Displays obstacle on xy plane w/ matplotlib.

        Adds to the current figure if there's already a figure.
        """
        rectangle_coordinates = [
            tuple(self.upper_left_corner),
            tuple(self.upper_right_corner),
            tuple(self.lower_right_corner),
            tuple(self.lower_left_corner)
        ]

        # Extract x and y coordinates
        x_values, y_values = zip(*rectangle_coordinates)

        # Repeat first coordinate to close rectangle
        x_values += (x_values[0],)
        y_values += (y_values[0],)

        # Change rectangle visuals here
        plt.plot(x_values, y_values, marker='o', linestyle='-', color='b', ms=1)

    def _set_center(self, center_x, center_y):
        """
        Change the obstacle's center coordinates.

        Updates obstacle corners to match the new center as well.

        Args:
            center_x (float): New x coordinate of obstacle center
            center_y (float): New y coordinate of obstacle center
        """
        self.center_x = center_x
        self.center_y = center_y
        self.upper_left_corner = [
            center_x - (self.horizontal_size / 2), 
            center_y + (self.vertical_size / 2) 
        ]
        self.upper_right_corner = [
            center_x + (self.horizontal_size / 2),
            center_y + (self.vertical_size / 2)
        ]
        self.lower_left_corner = [
            center_x - (self.horizontal_size / 2),
            center_y - (self.vertical_size / 2)
        ]
        self.lower_right_corner = [
            center_x + (self.horizontal_size / 2),
            center_y - (self.vertical_size / 2)
        ]
        
    def _check_overlap(self, x, y) -> bool:
        """
        Check whether a point x,y overlaps with the obstacle.

        Args:
            x (float): x coordinate of point to check for overlap
            y (float): y coordinate of point to check for overlap

        Returns:
            (bool): Result of overlap check
        """
        return_result = False

        # Each corner has coordinates (x, y)
        if ((x >= self.upper_left_corner[0]) 
                and (x <= self.upper_right_corner[0])
                and (y >= self.lower_left_corner[1]) 
                and (y <= self.upper_left_corner[1])):
            return_result = True

        return return_result

#------------------------------------------------------------------------------#
#                                Public Classes                                #
#------------------------------------------------------------------------------#
class Wall(_Obstacle):
    """
    Wall class to create a maze.

    Defines additional method to switch side lengths.

    Attributes:
        center_x (float): X coordinate of wall center
        center_y (float): Y coordinate of wall center
        horizontal_size (float): h. side of the wall in millimeters
        vertical_size   (float): v. side of the wall in millimeters
        upper_left_corner   (List[float]): Coordinates of upper left corner
        upper_right_corner: (List[float]): Coordinates of upper right corner
        lower_left_corner:  (List[float]): Coordinates of lower left corner
        lower_right_corner: (List[float]): Coordinates of lower right corner
    """
    def set_visible(self):
        """
        Make the wall visible (present) on the maze.
        """
        self.visible = True

    def plot_obstacle(self):
        """
        Display wall on xy plane w/ matplotlib.

        Adds to the current figure if there's already a figure.
        """
        if self.visible is True:
            super()._plot_obstacle()
    
    def set_center(self, center_x, center_y):
        """
        Change the wall's center coordinates.

        Updates wall corners to match the new center as well.

        Args:
            center_x (float): New x coordinate of wall center
            center_y (float): New y coordinate of wall center
        """
        super()._set_center(center_x, center_y)

    def check_overlap(self, x, y) -> bool:
        """
        Check whether a point x,y overlaps with the wall.

        Args:
            x (float): x coordinate of point to check for overlap
            y (float): y coordinate of point to check for overlap

        Returns:
            (bool): Result of overlap check
        """
        return_result = False

        return_result = super()._check_overlap(x, y)

        return return_result

    def switch_wall_sides(self):
        """
        Switch the horizontal and vertical side lengths.

        Updates wall corner coordinates accordingly.
        """
        new_horizontal_size = self.vertical_size
        new_vertical_size = self.horizontal_size

        self.horizontal_size = new_horizontal_size
        self.vertical_size = new_vertical_size
        self.upper_left_corner = [
            center_x - (new_horizontal_size / 2), 
            center_y + (new_vertical_size / 2) 
        ]
        self.upper_right_corner = [
            center_x + (new_horizontal_size / 2),
            center_y + (new_vertical_size / 2)
        ]
        self.lower_left_corner = [
            center_x - (new_horizontal_size / 2),
            center_y - (new_vertical_size / 2)
        ]
        self.lower_right_corner = [
            center_x + (new_horizontal_size / 2),
            center_y - (new_vertical_size / 2)
        ]


class Post(_Obstacle):
    """
    Post class to create a maze.

    Attributes:
        center_x (float): X coordinate of post center
        center_y (float): Y coordinate of post center
        horizontal_size (float): h. side of the post in millimeters
        vertical_size   (float): v. side of the post in millimeters
        upper_left_corner   (List[float]): Coordinates of upper left corner
        upper_right_corner: (List[float]): Coordinates of upper right corner
        lower_left_corner:  (List[float]): Coordinates of lower left corner
        lower_right_corner: (List[float]): Coordinates of lower right corner
    """
    def set_visible(self):
        """
        Make the post visible (present) on the maze.
        """
        self.visible = True

    def plot_obstacle(self):
        """
        Displays post on xy plane w/ matplotlib.

        Adds to the current figure if there's already a figure.
        """
        if self.visible is True:
            super()._plot_obstacle()
    
    def set_center(self, center_x, center_y):
        """
        Change the post's center coordinates.

        Updates post corners to match the new center as well.

        Args:
            center_x (float): New x coordinate of post center
            center_y (float): New y coordinate of post center
        """
        super()._set_center(center_x, center_y)

    def check_overlap(self, x, y) -> bool:
        """
        Check whether a point x,y overlaps with the post.

        Args:
            x (float): x coordinate of point to check for overlap
            y (float): y coordinate of point to check for overlap

        Returns:
            (bool): Result of overlap check
        """
        return_result = False

        return_result = super()._check_overlap(x, y)

        return return_result

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

    test_post = Post(100, 100, 12.065, 12.065)
    test_post.plot_obstacle()

    test_wall = Wall(200, 200, 166.37, 12.065)
    test_wall.plot_obstacle()

    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

# Example usage
if __name__ == "__main__":
    main()
