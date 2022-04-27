def threshold_matrix(mat_file=None, threshold=None, direction='both'):
    import numpy as np

    A = np.loadtxt(mat_file, delimiter=',')  #adjacency matrix text file

    if threshold:
        if direction == 'both':
            direction_vals = "abs(A)"
        elif direction == 'negative':
            direction_vals = 'A * -1'
        elif direction == 'positive':
            direction_vals = 'A'
        if threshold[0] == 'proportional':
            A_sort = np.sort(
                abs(
                    A[np.triu(A, k = 1) != 0]
                )
            )
            thresh_pct = threshold[1]/100
            thresh = int(thresh_pct*A_sort.size)
            exec(f"A[{direction_vals} < A_sort[-thresh]] = 0")
        elif threshold[0] == 'absolute':
            exec(f"A[{direction_vals} < threshold[1]] = 0")
        else:
            return
    
    thresh_mat = np.triu(A, k = 1)

    return thresh_mat