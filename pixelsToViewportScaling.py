
# v1.0 --- copyright under MIT License --- developed by turboscient https://github.com/Turboscient

# PURPOSE: pixelsToViewportScaling has three main target audiences. 1) it is for beginners who feel more comfortable
# coding in pixels than percentages or css flexbox or viewport dimensions; they can code their entire site in
# non-responsive css, then do a quick conversion using PVS. 2) It can be used to improve previously made css files with
# otherwise too many lines to update manually. 3) It is for people who prefer not to work with decimals when writing css
# as pixels are usually discrete whereas viewport accuracy often requires additional precision.

from shutil import copyfile

# Accepts your viewport dimensions to provide pixel-equivalent scaling in vw or vh; first parameter accepts
# a file path, second parameter accepts either 'vw' or 'vh', third parameter should be a tuple of
# (window.innerWidth, window.innerHeight) from your development or otherwise-acceptable-looking browser implementation,
# and the optional fourth parameter sets the decimal places to round the vw/vh value to.

#EXAMPLE: I use pixelsToViewportScaling('style.css', 'vw', (1536, 500))

def pixelsToViewportScaling(filePath, viewportWidthOrHeight, dimensions, decimalPlacesRoundTo = 4):

    # Function will test file path to see if it's correct; will return error otherwise
    checkFilePath(filePath)

    # Copies file and writes to new location; we copy the file to minimize interaction with the
    # original file in case of accidental overwrite; metadata is not preserved
    copyfile(filePath, 'viewportEnhancedStyle.css')

    # Assigning file to a variable
    with open('viewportEnhancedStyle.css', 'r+') as vEStyle:

        # Before substituting px with vw/vh, we get a list of the lines in the CSS file
        lines_list = vEStyle.readlines()

        # We use prepare an empty list to store modified lines
        enhanced_lines_list = []

        for line in lines_list:

            # We ignore lines from the CSS file unless they have 'px' in them
            if 'px' in line:

                # Split the line into pieces, if done correctly containing a substring '***px' where *** are numbers
                space_separated_substrings = line.split()

                # Index for list splicing; we now have to separate *** from the unneeded 'px'
                substring_index = 0
                for substring in space_separated_substrings:
                    if 'px' in substring:
                        if len(substring) > 3:
                            value_of_substring = substring[:(len(substring)-3)]
                        if len(substring) == 3:
                            value_of_substring = substring[:(len(substring) - 2)]

                        # Check if we are converting to viewport width
                        if viewportWidthOrHeight == 'vw':

                            # window.innerWidth
                            viewport = dimensions[0]

                            # Can't convert empty string to float; can't divide by zero
                            if value_of_substring != '' and viewport != 0:

                                # Convert *** to a float and divide it by window.innerWidth, round the result to 12 decimal places
                                # and multiply by 100 to get the ratio as a number from 0 to 100.
                                space_separated_substrings[substring_index] = str(
                                    round((float(value_of_substring) / viewport * 100), decimalPlacesRoundTo)
                                    ) + viewportWidthOrHeight

                        # Check if we are converting to viewport height
                        elif viewportWidthOrHeight == 'vh':

                            # window.innerHeight
                            viewport = dimensions[1]

                            # Can't convert empty string to float; can't divide by zero
                            if value_of_substring != '' and viewport != 0:

                                # Convert *** to a float and divide it by window.innerHeight, round the result to 12 decimal places
                                # and multiply by 100 to get the ratio as a number from 0 to 100.
                                space_separated_substrings[substring_index] = str(
                                    round((float(value_of_substring) / viewport * 100), decimalPlacesRoundTo)
                                    ) + viewportWidthOrHeight

                    else:
                        # Prevents double semi-colon bug by removing all semi-colons and then appending a new one
                        if substring.endswith(';'):
                            space_separated_substrings[substring_index] = substring.replace(';', '')
                    substring_index += 1

                # Finalize the new viewport-modified css line
                line = '\t' + ' '.join(space_separated_substrings) + ';' + '\n'

            # Append this line to our new list of modified lines
            enhanced_lines_list.append(line)

        # Set pointer to beginning of the copied file and clear the lines in the file; substitute the new lines into the
        # file's copy
        vEStyle.seek(0)
        vEStyle.truncate(0)
        vEStyle.writelines(enhanced_lines_list)

        # Set the pointer to the beginning of the file again
        vEStyle.seek(0)

# Confirms if the user's path is valid
def checkFilePath(filePath):
   try:
       path_check = open(filePath, 'r')
   except OSError:
       print('The file\'s path is incorrect')


# RUN THE SCRIPT

# EXAMPLE: I use pixelsToViewportScaling('style.css', 'vw', (1536, 500))

# Uncomment below with your custom arguments to run the script
#pixelsToViewportScaling('', '', ( , ))

