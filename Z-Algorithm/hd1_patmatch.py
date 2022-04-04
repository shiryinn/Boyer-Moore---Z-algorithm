"""
Name: Lim Shir Yin
StudentID: 31059546
FIT3155 Assignment 1 Question 2 2022
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


def reversed_str(string):
    """
    Function: Returns a string in reversed order.
    """
    flip_str = ""
    for i in range(len(string)-1, -1, -1):
        flip_str += string[i]

    return flip_str


def hd1_patmatch(txt, pat):
    """
    Function: Returns tuple(s) in an array with the identified positions within txt[1..n] that matches the pat[1..m] and a hamming distance of <= 1.
    """

    # handle empty pattern or empty text
    if len(txt) == 0 or len(pat) == 0:
        return []

    concat_txt = pat + "$" + txt

    # run z algo for normal concat text
    z_arr = z_algo(concat_txt)

    # flip the pattern
    flip_pat = reversed_str(pat)

    # flip the text
    flip_txt = reversed_str(txt)

    flip_concat_txt = flip_pat + "$" + flip_txt

    # run z algo for flip concat text
    flip_z_arr = z_algo(flip_concat_txt)

    m = len(pat) + 1  # length of pattern + $
    output = []  # store result
    i = m  # range start after len(pat) + 1 (including $)

    while i < len(concat_txt):

        offset = 1  # offset
        j = len(concat_txt) - i + len(pat)  # track the index of flip z array
        remaining_txt = len(concat_txt) - i

        # match with hamming distance of 0
        if len(pat) - z_arr[i] == 0 or len(pat) - flip_z_arr[j - len(pat) + 1] == 0:
            hamming_distance = 0
            output.append((i - m + offset, hamming_distance))

        # match with hamming distance of 1
        else:
            # break the loop once the length of remaining text < length of pat
            if remaining_txt >= len(pat):
                if len(pat) - (z_arr[i] + flip_z_arr[j - len(pat) + 1]) == 1:
                    hamming_distance = 1
                    output.append((i - m + offset, hamming_distance))
            else:
                break

        i += 1

    return output


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
    output_filename = open("output_hd1_patmatch.txt", "w")
    # iterate through the result list and write results
    if len(result) > 0:
        output_filename.write("{: <5} {: <5}".format(
            str(result[0][0]), str(result[0][1])))
        for i in range(1, len(result)):
            output_filename.write("\n")
            output_filename.write("{: <5} {: <5}".format(
                str(result[i][0]), str(result[i][1])))
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
    result = hd1_patmatch(txt, pat)
    write_output(result)
