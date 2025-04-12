#!/usr/bin/perl

# this is a comment 4
use strict;
use warnings;

# Specify the input file and output directory
my $input_file = "large_file.txt";
my $output_dir = "output/";

# Specify the maximum part size in bytes (5 GB)
my $max_part_size = 5 * 1024 * 1024 * 1024;

# Open the input file for reading
open(my $fh_in, "<", $input_file) or die "Failed to open input file: $!";

# Create the output directory if it does not exist
if (!-d $output_dir) {
    mkdir $output_dir or die "Failed to create output directory: $!";
}

# Initialize the part number and current file size
my $part_number = 1;
my $current_file_size = 0;

# Initialize a buffer to store the current part's contents
my $part_buffer = "";

# Loop through the input file
while (my $line = <$fh_in>) {
    # Add the current line to the part buffer
    $part_buffer .= $line;

    # If the part buffer exceeds the maximum part size, write it to a new output file
    if (length($part_buffer) > $max_part_size) {
        # Remove the last incomplete record from the part buffer
        $part_buffer =~ s/(.*?\n)//s;
        my $incomplete_record = $1;

        # Construct the output file name
        my $output_file = sprintf("%s/part_%03d.txt", $output_dir, $part_number);

        # Open the current output file for writing if it does not exist
        if (!-e $output_file) {
            open(my $fh_out, ">", $output_file) or die "Failed to create output file: $!";

            # Write the complete records from the part buffer to the output file
            print $fh_out $part_buffer;

            # Close the output file
            close $fh_out;

            # Reset the part buffer and update the current file size
            $part_buffer = $incomplete_record;
            $current_file_size = length($incomplete_record);

            # Increment the part number
            $part_number++;
        }
    }
}

# Write the remaining contents in the part buffer to the last output file
my $output_file = sprintf("%s/part_%03d.txt", $output_dir, $part_number);
open(my $fh_out, ">", $output_file) or die "Failed to create output file: $!";
print $fh_out $part_buffer;
close $fh_out;

# Close the input file
close $fh_in;

print "Splitting of large file completed successfully!\n";
