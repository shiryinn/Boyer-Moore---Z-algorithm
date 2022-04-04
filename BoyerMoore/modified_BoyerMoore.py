"""
Name: Lim Shir Yin
StudentID: 31059546
FIT3155 Assignment 1 Question 1 2022
"""

import sys


def z_algo(txt):
    """
    Function: To find all occurrences of pat within a txt.
    """
    index = 0

    # initialise z-array
    z_array = []
    while index < len(txt):
        # first index of z array is the length of txt
        if index == 0:
            z_array.append(len(txt))
        else:
            z_array.append(None)
        index += 1

    # index of zbox
    left = 0
    right = 0
    i = 1

    while i < len(txt):
        k = i - left
        remaining = right - i + 1

        # case 1: i is outside of the zbox
        if i > right:
            left, right = i, i
            while right < len(txt) and txt[right] == txt[right - i]:
                right += 1

            z_array[i] = right - i
            right -= 1

        # case 2: i is inside of the zbox
        else:
            # case 2a: z[k] < remaining
            if z_array[k] < remaining:
                z_array[i] = z_array[k]

            # case 2c: z[k] == remaining
            elif z_array[k] == remaining:
                # comparison starts from right onwards
                temp_remaining = remaining
                while (temp_remaining + i) < len(txt) and txt[temp_remaining] == txt[temp_remaining + i]:
                    temp_remaining += 1
                    right += 1

                z_array[i] = temp_remaining
                left = i   # set left to the new z box
                right -= 1

            # case 2b: z[k] > remaining
            else:
                z_array[i] = remaining

        i += 1
    return z_array


def unique_char_ord(char):
    """
    Function: Returns the unicode of a single character.
    """
    return ord(char)-32


def get_bc_table(pat):
    """
    Function: Returns a bad char table with the given pat.
    """
    bc_info = []
    count_arr = [0 for _ in range(96)]

    # get unique characters for the pattern
    for i in range(len(pat)):
        unique_code = unique_char_ord(pat[i])
        count_arr[unique_code] += 1

    unique_char_index = 0
    unique_char_arr = []

    while unique_char_index < len(count_arr):
        if count_arr[unique_char_index] > 0:
            unique_char_arr.append(unique_char_index)
        unique_char_index += 1

    for i in range(len(unique_char_arr)):
        # replace count with unique char index in array
        count_arr[unique_char_arr[i]] = i

    bc_info.append(count_arr)

    # create bc table with the number of unique character of the pattern
    bc_table = [[0]*len(pat) for _ in range(len(unique_char_arr))]

    # fill in bc table from RIGHT to LEFT
    m = len(pat)
    for i in range(m-1, -1, -1):
        table_idx = count_arr[unique_char_ord(pat[i])]
        bc_table[table_idx][i] = i + 1
        k = i + 1
        while k < len(pat) and bc_table[table_idx][k] == 0:
            bc_table[table_idx][k] = bc_table[table_idx][i]
            k += 1

    # append count array for bm purpose
    bc_info.append(bc_table)

    return bc_info


def get_gs_arr(pat):
    """
    Function: Returns a good suffix array with the given pat.
    """
    # flip the pattern
    flip_pat = ""
    for i in range(len(pat)-1, -1, -1):
        flip_pat += pat[i]

    # run z-algo
    flip_gs_z_arr = z_algo(flip_pat)

    # flip back the z array
    gs_z_arr = []
    for i in range(len(flip_gs_z_arr)-1, -1, -1):
        gs_z_arr.append(flip_gs_z_arr[i])

    # initialise good suffix array of len(pat) + 1 with 0
    m = len(pat)
    gs_arr = [0] * (m+1)

    # p loop from 1 to m - 1 (last index will be len(pat))
    p = 0
    while p < m - 1:   # 0-indexing
        # j = M - Z-suffix + 1 (z-array)
        z_suff = gs_z_arr[p]
        j = m - z_suff
        # fill in gs array[j] = p
        gs_arr[j] = p + 1
        p += 1

    return gs_arr


def get_mp_arr(pat):
    """
    Function: Returns a matched prefix array with the given pat.
    """
    # run z-algo for pat
    mp_z_arr = z_algo(pat)

    # initialise a len array
    mp_len_arr = []
    index_arr = 0
    while index_arr < len(pat):
        mp_len_arr.append(0)
        index_arr += 1

    # use formula if z[i] + 1 = len(pat) + 1; copy val from z array
    # from right to left
    for i in range(len(pat)-1, -1, -1):   # 0-indexing
        if (mp_z_arr[i] + (i + 1)) == (len(pat) + 1):
            mp_len_arr[i] = mp_z_arr[i]

        # if z[i] + 1 != len(pat) + 1; copy val from right
        else:
            if (i+1) < len(pat):
                mp_len_arr[i] = mp_len_arr[i+1]

    return mp_len_arr


def modified_BoyerMoore(txt, pat):
    """
    Function: Returns an array of positions of all occurrences of pat in txt.
    """

    # handle empty txt/pat and len(pat) > len(txt
    if len(pat) > len(txt) or len(pat) == 0 or len(txt) == 0:
        return []

    # pre-processing
    bad_char_table = get_bc_table(pat)
    good_suffix_arr = get_gs_arr(pat)
    matched_prefix_arr = get_mp_arr(pat)

    # to get index of mismatch letter in bc table
    char_count_arr = bad_char_table[0]
    # bad char table
    bc_table = bad_char_table[1]

    matches = []
    m = len(pat)
    n = len(txt)
    var_resume, var_break = 0, 0  # galil's variable
    alpha_txt = 0
    bc_shift_jump, gs_shift_jump, mp_shift_jump = 0, 0, 0  # initialise shift jumps
    offset = 1

    j = 0
    while j + m <= n:
        k = m - 1  # track the index of pat
        shift_jump = 1

        while k >= 0 and k < m:

            var_resume = k  # set resume to be the current index of pat
            var_break = var_resume + alpha_txt  # set break to resume index + matched pat
            k = var_resume  # set current index of pat with the current resume variable

            # apply galil's optimisation (avoid repeat comparison)
            if k > var_break or k <= var_resume:
                x = j + k  # current position of text
                alpha_txt = m - k   # get the text after the index of mismatch char

                # mismatch occurs
                if txt[x] != pat[k]:
                    bad_char = txt[x]
                    # get index of bad char in count array
                    unique_index = char_count_arr[unique_char_ord(bad_char)]

                    # bc shift
                    bc_shift_jump = k - (bc_table[unique_index][k])

                    # gs shift
                    # ensure gs is preceded by a bc (modified spec)
                    if good_suffix_arr[k+1] > 0 and bad_char == pat[m - good_suffix_arr[k+1] - 1]:
                        gs_shift_jump = m - good_suffix_arr[k+1]

                    elif good_suffix_arr[k+1] == 0:
                        # perform mp
                        if k + 1 < len(pat):
                            gs_shift_jump = m - matched_prefix_arr[k+1]
                        else:
                            gs_shift_jump = 0

                    # avoid shift jump to be 0
                    shift_jump = max(shift_jump, bc_shift_jump, gs_shift_jump)
                    break

                else:
                    # pat matches the entire txt
                    if k == 0:
                        matches.append(j + offset)
                        # mp shift
                        if len(pat) <= 1:  # handle pat with length of 1
                            mp_shift_jump = matched_prefix_arr[0]
                        else:
                            mp_shift_jump = m - matched_prefix_arr[1]  # offset

                    shift_jump = mp_shift_jump

                k -= 1  # comparison starts from right to left
        j += shift_jump  # increment by shift jump

    return matches


# cite from the tutorial video under assessment in moodle
def read_input(txt_filename, pat_filename):
    """
    Function: Reads input files. 
    """
    # open and read the text file
    txt_file = open(txt_filename, "r")
    txt = txt_file.read()
    # close text file
    txt_file.close()

    # open and read the pat file
    pat_file = open(pat_filename, "r")
    pat = pat_file.read()
    # close pat file
    pat_file.close()

    return txt, pat


# cite from the tutorial video under assessment in moodle
def write_output(result):
    """
    Function: Writes the output result in a file.
    """
    output_filename = open("output_modified_BoyerMoore.txt", "w")
    # iterate through the result list and write results
    if len(result) > 0:
        output_filename.write(str(result[0]))
        for i in range(1, len(result)):
            output_filename.write("\n")
            output_filename.write(str(result[i]))
    else:
        output_filename.write("")
    # close file
    output_filename.close()


if __name__ == '__main__':
    # put arguments in
    python_file_name = sys.argv[0]
    txt_file_name = sys.argv[1]
    pat_file_name = sys.argv[2]
    # read text and pat inputs
    txt, pat = read_input(txt_file_name, pat_file_name)
    # write result output
    result = modified_BoyerMoore(txt, pat)
    write_output(result)
