#---------------------------------- FILE INFO ---------------------------------#
#                                                                              #
# Project       : Micromouse Simulation                                        #
# Filename      : maze.py                                                      #
# Author        : Team Kirbo                                                   #
# Revision      : 1.0                                                          #
# Updated       : 2024-10-6                                                   #
#                                                                              #
# Contains class and method definitions for the maze class.                    #
#                                                                              #
#-------------------------------- END FILE INFO -------------------------------#

#----------------------------- SPHINX FILE HEADER -----------------------------#
"""
maze.py

This file contains class and method definitions for the maze class.
"""
#--------------------------- END SPHINX FILE HEADER ---------------------------#

#------------------------------------------------------------------------------#
#                                Import Files                                  #
#------------------------------------------------------------------------------#
from mouse import *
from obstacle import *

#------------------------------------------------------------------------------#
#                                  Definitions                                 #
#------------------------------------------------------------------------------#
__all__ = ['Maze']

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
class MazeSquare:
    """
    Maze sqaure class to fill a maze.

    Attributes:
        post_lower_left  (Post): Lower left post of the maze square
        post_upper_left  (Post): Upper left post of the maze square
        post_upper_right (Post): Upper right post of the maze square
        post_lower_right (Post): Lower right post of the maze square
        wall_left   (Wall): Left wall of the maze square
        wall_top    (Wall): Top wall of the maze square
        wall_right  (Wall): Right wall of the maze square
        wall_bottom (Wall): Bottom wall of the maze square
        row (int): row coordinate assigned to square
        col (int): col coordinate assigned to square
    """
    def __init__(
        self, 
        post_lower_left, post_upper_left, post_upper_right, post_lower_right,
        wall_left, wall_top, wall_right, wall_bottom,
        row, col
    ):
        """
        Initializes the MazeSquare instance.

        Args:
            post_lower_left  (Post): Lower left post of the maze square
            post_upper_left  (Post): Upper left post of the maze square
            post_upper_right (Post): Upper right post of the maze square
            post_lower_right (Post): Lower right post of the maze square
            wall_left   (Wall): Left wall of the maze square
            wall_top    (Wall): Top wall of the maze square
            wall_right  (Wall): Right wall of the maze square
            wall_bottom (Wall): Bottom wall of the maze square
            row (int): row coordinate assigned to square
            col (int): col coordinate assigned to square
        """
        self.post_lower_left = post_lower_left
        self.post_upper_left = post_upper_left
        self.post_upper_right = post_upper_right
        self.post_lower_right = post_lower_right
        self.wall_left = wall_left
        self.wall_top = wall_top
        self.wall_right = wall_right
        self.wall_bottom = wall_bottom
        self.row = row
        self.col = col

    def plot_maze_square(self):
        """
        Display maze square on xy plane w/ matplotlib.

        Adds to the current figure if there's already a figure.
        """
        self.post_lower_left.plot_obstacle()
        self.post_upper_left.plot_obstacle()
        self.post_upper_right.plot_obstacle()
        self.post_lower_right.plot_obstacle()
        self.wall_left.plot_obstacle()
        self.wall_top.plot_obstacle()
        self.wall_right.plot_obstacle()
        self.wall_bottom.plot_obstacle()

    def check_overlap(self, x, y) -> bool:
        """
        Check whether a point x,y overlaps with the square.

        Args:
            x (float): x coordinate of point to check for overlap
            y (float): y coordinate of point to check for overlap

        Returns:
            (bool): Result of overlap check
        """
        return_result = False

        if ((x >= self.post_upper_left.upper_left_corner[0]) 
                and (x <= self.post_upper_right.upper_right_corner[0])
                and (y >= self.post_lower_left.lower_left_corner[1]) 
                and (y <= self.post_upper_left.upper_left_corner[1])):
            return_result = True

        return return_result

    def get_shortest_sensor_distances(self, mouse):
        """
        Check every obstacle line segment and return shortest sensor distances.

        Args:
            mouse (Mouse): Mouse to check sensor distances
        
        Returns:
            (Tuple(float)): Distances for left forward, left diagonal, right 
            diagonal, and right forward sensors.
        """
        shortest_left_forward = None
        shortest_left_diagonal = None
        shortest_right_diagonal = None
        shortest_right_forward = None
        
        visibility_list = [
            self.post_lower_left.visible,
            self.post_upper_left.visible,
            self.post_upper_right.visible,
            self.post_lower_right.visible,
            self.wall_left.visible,
            self.wall_top.visible,
            self.wall_right.visible,
            self.wall_bottom.visible 
        ]

        obstacle_list = [
            self.post_lower_left,
            self.post_upper_left,
            self.post_upper_right,
            self.post_lower_right,
            self.wall_left,
            self.wall_top,
            self.wall_right,
            self.wall_bottom
        ]

        obstacle_side_list = []
        for obstacle in obstacle_list:
            obstacle_side_list.append(
                [
                    [obstacle.lower_left_corner, obstacle.upper_left_corner], 
                    [obstacle.upper_left_corner, obstacle.upper_right_corner],
                    [obstacle.upper_right_corner, obstacle.lower_right_corner],
                    [obstacle.lower_right_corner, obstacle.lower_left_corner]
                ]
            )

        s1_distance_list = []
        s2_distance_list = []
        s3_distance_list = []
        s4_distance_list = []
        for obstacle_index in range(8):
            if visibility_list[obstacle_index] is True:
                for side in obstacle_side_list[obstacle_index]:
                    s1_distance_list.append(
                        mouse.get_left_forward_sensor_distance(
                            side[0], side[1]
                        )
                    )
                    s2_distance_list.append(
                        mouse.get_left_diagonal_sensor_distance(
                            side[0], side[1]
                        )
                    )
                    s3_distance_list.append(
                        mouse.get_right_diagonal_sensor_distance(
                            side[0], side[1]
                        )
                    )
                    s4_distance_list.append(
                        mouse.get_right_forward_sensor_distance(
                            side[0], side[1]
                        )
                    )
        s1_cleaned_list = [x for x in s1_distance_list if x is not None]
        s2_cleaned_list = [x for x in s2_distance_list if x is not None]
        s3_cleaned_list = [x for x in s3_distance_list if x is not None]
        s4_cleaned_list = [x for x in s4_distance_list if x is not None]

        if len(s1_cleaned_list) != 0:
            shortest_left_forward = min(s1_cleaned_list)
        if len(s2_cleaned_list) != 0:
            shortest_left_diagonal = min(s2_cleaned_list)
        if len(s3_cleaned_list) != 0:
            shortest_right_diagonal = min(s3_cleaned_list)
        if len(s4_cleaned_list) != 0:
            shortest_right_forward = min(s4_cleaned_list)

        return (
            shortest_left_forward, 
            shortest_left_diagonal, 
            shortest_right_diagonal,
            shortest_right_forward
        )

class Maze:
    """
    Maze class including posts, walls, and a micromouse.

    Allows user to simulate a maze of any post/wall dimension.

    Attributes:
        row_count    (int): Number of rows in the maze
        column_count (int): Number of columns in the maze
        wall_length  (float): Long side of wall in mm
        wall_width   (float): Short side of wall in mm
        post_size    (float): Side length of post in mm
        squares_matrix (List(Square)): Matrix of maze squares
        mouse        (Mouse): Micromouse robot in the maze
    """

    def __init__(
        self,
        row_count, column_count, 
        wall_length, wall_width, post_size, 
        vertical_wall_matrix, horizontal_wall_matrix, 
    ):
        """
        Initializes the Maze instance.

        Args:
            row_count    (int): Number of rows in the maze
            column_count (int): Number of columns in the maze
            wall_length  (float): Long side of wall in mm
            wall_width   (float): Short side of wall in mm
            post_size    (float): Side length of post in mm
            vertical_wall_matrix (List(str)): Matrix of vertical walls
            horizontal_wall_matrix (List(str)): Matrix of horizontal walls 
        """
        self.row_count = row_count
        self.column_count = column_count
        self.wall_length = wall_length
        self.wall_width = wall_width
        self.post_size = post_size
        self.squares_matrix = \
            [[None for _ in range(column_count)] for _ in range(row_count)]
        self.mouse = Mouse(
            post_size + (wall_length / 2),
            post_size + (wall_length / 2)
        )
        
        # Fill squares_matrix
        current_row = 0
        current_column = 0
        for row in self.squares_matrix:
            for column in row:
                # Coordinates of posts
                x_coord_post_lower_left = \
                    ((current_column * (post_size + wall_length))
                    + (post_size / 2))
                y_coord_post_lower_left = \
                    (((row_count - current_row - 1) * (post_size + wall_length))
                    + (post_size / 2))
                
                x_coord_post_upper_left = \
                    ((current_column * (post_size + wall_length))
                    + (post_size / 2))
                y_coord_post_upper_left = \
                    (((row_count - current_row) * (post_size + wall_length))
                    + (post_size / 2))
                
                x_coord_post_upper_right = \
                    (((current_column + 1) * (post_size + wall_length))
                    + (post_size / 2))
                y_coord_post_upper_right = \
                    (((row_count - current_row) * (post_size + wall_length))
                    + (post_size / 2))
                
                x_coord_post_lower_right = \
                    (((current_column + 1) * (post_size + wall_length))
                    + (post_size / 2))
                y_coord_post_lower_right = \
                    (((row_count - current_row - 1) * (post_size + wall_length))
                    + (post_size / 2))
                
                # Coordinates of walls
                x_coord_wall_top = \
                    (post_size + ((current_column) * (post_size + wall_length))
                    + (wall_length / 2))
                y_coord_wall_top = \
                    (((row_count - current_row) * (post_size + wall_length))
                    + (wall_width / 2))

                x_coord_wall_left = \
                    ((current_column * (post_size + wall_length))
                    + (wall_width / 2))
                y_coord_wall_left = \
                    (post_size + ((row_count - current_row - 1) * (post_size + wall_length))
                    + (wall_length / 2))
                
                x_coord_wall_right = \
                    (((current_column + 1) * (post_size + wall_length))
                    + (wall_width / 2))
                y_coord_wall_right = \
                    (post_size + ((row_count - current_row - 1) * (post_size + wall_length))
                    + (wall_length / 2))
                
                x_coord_wall_bottom = \
                    (post_size + (current_column * (post_size + wall_length))
                    + (wall_length / 2))
                y_coord_wall_bottom = \
                    ((row_count - current_row - 1) * (post_size + wall_length)
                    + (wall_width / 2))
                
                # New walls and posts for new maze square
                post_lower_left = None
                post_upper_left = None
                post_upper_right = None
                wall_top = None
                wall_left = None

                # Squares are generated left -> right and top -> down,
                # so "lower right post", "right wall", and "bottom wall" are 
                # never shared between maze squares
                post_lower_right = Post(
                    x_coord_post_lower_right, y_coord_post_lower_right,
                    post_size, post_size
                )
                
                wall_right = Wall(
                    x_coord_wall_right, y_coord_wall_right,
                    wall_width, wall_length
                )

                wall_bottom = Wall(
                    x_coord_wall_bottom, y_coord_wall_bottom,
                    wall_length, wall_width
                )

                # Reference wall and posts to the left if present
                if current_column > 0:
                    post_lower_left = \
                        (self.squares_matrix[current_row][current_column - 1]
                        .post_lower_right)
                    post_upper_left = \
                        (self.squares_matrix[current_row][current_column - 1]
                        .post_upper_right)
                    wall_left = \
                        (self.squares_matrix[current_row][current_column - 1]
                        .wall_right)
                else:
                    post_lower_left = Post(
                        x_coord_post_lower_left, y_coord_post_lower_left,
                        post_size, post_size
                    )
                    post_upper_left = Post(
                        x_coord_post_upper_left, y_coord_post_upper_left,
                        post_size, post_size
                    )
                    wall_left = Wall(
                        x_coord_wall_left, y_coord_wall_left,
                        wall_width, wall_length
                    )
                    
                # Reference wall and posts above if present
                if current_row > 0:
                    post_upper_right = \
                        (self.squares_matrix[current_row - 1][current_column]
                        .post_lower_right)
                    post_upper_left = \
                        (self.squares_matrix[current_row - 1][current_column]
                        .post_lower_left)
                    wall_top = \
                        (self.squares_matrix[current_row - 1][current_column]
                        .wall_bottom)
                else:
                    post_upper_right = Post(
                        x_coord_post_upper_right, y_coord_post_upper_right,
                        post_size, post_size
                    )
                    post_upper_left = Post(
                        x_coord_post_upper_left, y_coord_post_upper_left,
                        post_size, post_size
                    )
                    wall_top = Wall(
                        x_coord_wall_top, y_coord_wall_top,
                        wall_length, wall_width
                    )

                # Update visibility of walls and posts
                post_lower_left.set_visible()
                post_upper_left.set_visible()
                post_upper_right.set_visible()
                post_lower_right.set_visible()

                if horizontal_wall_matrix[current_row][current_column] != ' ':
                    wall_top.set_visible()
                if horizontal_wall_matrix[current_row + 1][current_column] != ' ':
                    wall_bottom.set_visible()
                if vertical_wall_matrix[current_row][current_column] != ' ':
                    wall_left.set_visible()
                if vertical_wall_matrix[current_row][current_column + 1] != ' ':
                    wall_right.set_visible()

                new_maze_square = MazeSquare(
                    post_lower_left, post_upper_left, 
                    post_upper_right, post_lower_right,
                    wall_left, wall_top, wall_right, wall_bottom, 
                    current_row, current_column
                )

                self.squares_matrix[current_row][current_column] = new_maze_square

                # Finished column
                current_column += 1
            
            # Finished row
            current_row += 1
            current_column = 0

    def plot_maze(self):
        """
        Display the maze and mouse on xy plane w/ matplotlib
        """
        for row in range(self.row_count):
            for col in range(self.column_count):
                self.squares_matrix[row][col].plot_maze_square()

        self.mouse.plot_mouse()

    def move_mouse(self, column, row):
        """
        Move mouse to the center of the specified maze square.

        Args:
            column (int): Column to move mouse to
            row    (int): Row to move mouse to
        """
        new_center_x = \
            (self.post_size 
            + (column * (self.post_size + self.wall_length)) 
            + (self.wall_length / 2))
        new_center_y = \
            (self.post_size 
            + (((self.row_count - 1) - row) * (self.post_size + self.wall_length)) 
            + (self.wall_length / 2))
        self.mouse = Mouse(
            new_center_x,
            new_center_y
            )

    def find_mouse(self):
        """
        Find the coordinates of the mouse in the maze.

        Returns:
            (Tuple(int)): Row & column of mouse in the maze; None if not found 
        """
        for row in range(self.row_count):
            for col in range(self.column_count):
                x = self.mouse.center_x
                y = self.mouse.center_y
                if self.squares_matrix[row][col].check_overlap(x, y):
                    return row, col

        return None, None
        
    def get_sensor_distances(self):
        """
        Find the distance detected by all mouse IR sensors.

        Returns:
            (Tuple(float)): All sensor distances; None if no obstacle in view 
        """
        left_forward_distance = None
        left_diagonal_distance = None
        right_diagonal_distance = None
        right_forward_distance = None
        s1_distance_list = []
        s2_distance_list = []
        s3_distance_list = []
        s4_distance_list = []

        no_top_squares = False
        no_left_squares = False
        no_right_squares = False
        no_bottom_squares = False
        mouse_row, mouse_col = self.find_mouse()

        if (mouse_row is None) or (mouse_col is None):
            left_forward_distance = None
            left_diagonal_distance = None
            right_diagonal_distance = None
            right_forward_distance = None
        else:
            # Scan all squares around mouse square:
            for row in range(mouse_row - 1, mouse_row + 2):
                for col in range(mouse_col - 1, mouse_col + 2):
                    if ((row >= 0) and 
                        (row <= (self.row_count - 1)) and
                        (col >= 0) and 
                        (col <= (self.column_count - 1))):
                        left_forward_distance,   \
                        left_diagonal_distance,  \
                        right_diagonal_distance, \
                        right_forward_distance = \
                            (self.squares_matrix[row][col]
                            .get_shortest_sensor_distances(self.mouse))
                        s1_distance_list.append(left_forward_distance)
                        s2_distance_list.append(left_diagonal_distance)
                        s3_distance_list.append(right_diagonal_distance)
                        s4_distance_list.append(right_forward_distance)

        s1_distance_list = [x for x in s1_distance_list if x is not None]
        s2_distance_list = [x for x in s2_distance_list if x is not None]
        s3_distance_list = [x for x in s3_distance_list if x is not None]
        s4_distance_list = [x for x in s4_distance_list if x is not None]

        if len(s1_distance_list) != 0:
            left_forward_distance = min(s1_distance_list)
        if len(s2_distance_list) != 0:
            left_diagonal_distance = min(s2_distance_list)
        if len(s3_distance_list) != 0:
            right_diagonal_distance = min(s3_distance_list)
        if len(s4_distance_list) != 0:
            right_forward_distance = min(s4_distance_list)

        return (
            left_forward_distance, 
            left_diagonal_distance, 
            right_diagonal_distance,
            right_forward_distance
        )

#------------------------------------------------------------------------------#
#                                Public Functions                              #
#------------------------------------------------------------------------------#
# None

#------------------------------------------------------------------------------#
#                       Private Functions (DO NOT EXPORT)                      #
#------------------------------------------------------------------------------#
# None

#------------------------------------------------------------------------------#
#                                     MAIN                                     #
#------------------------------------------------------------------------------#
def main():
    # <Insert code here>
    pass

# Example usage
if __name__ == "__main__":
    main()
