import numpy as np


# Written by chatgpt
def remove_full_rows(gameBoard):  # python is being annoying
    # Find rows that contain the number 7
    mask = np.any(gameBoard == 7, axis=1)

    # Keep only those rows
    filtered_matrix = gameBoard[mask]

    # Calculate the number of rows to be filled with 7s
    num_rows_to_fill = gameBoard.shape[0] - filtered_matrix.shape[0]

    # Create rows filled with 7s
    rows_of_7s = np.full((num_rows_to_fill, gameBoard.shape[1]), 7)

    # Concatenate the rows of 7s and the filtered matrix
    gameBoard = np.vstack((rows_of_7s, filtered_matrix))
