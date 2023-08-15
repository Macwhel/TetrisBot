import numpy as np
import pprint as pp

from Renders.Grid import draw_grid


# Written by chatgpt
def remove_full_rows(gameBoard):
    # Filter out rows that contain the number 7
    filtered_arr = gameBoard[np.any(gameBoard == 7, axis=1)]

    # Calculate the number of removed rows
    num_removed_rows = gameBoard.shape[0] - filtered_arr.shape[0]

    # Create new rows of 7s
    new_rows = np.full((num_removed_rows, gameBoard.shape[1]), 7)

    # Add the new rows to the top of the filtered array
    return np.vstack((new_rows, filtered_arr))
