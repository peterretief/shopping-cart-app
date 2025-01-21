#!/bin/bash

# Check if both arguments are provided
if [ $# -ne 2 ]; then
    echo "Usage: $0 <input_image> <output_image>"
    exit 1
fi

input_image="$1"
output_image="$2"
icon_size=32  # Default icon size

# Check if input file exists
if [ ! -f "$input_image" ]; then
    echo "Error: Input file does not exist."
    exit 1
fi

# Use FFmpeg to scale the image with single frame output
ffmpeg -i "$input_image" \
    -vf "scale=${icon_size}:${icon_size}:force_original_aspect_ratio=decrease" \
    -frames:v 1 \
    -f image2 \
    -quality 90 \
    "$output_image"

if [ $? -eq 0 ]; then
    echo "Image successfully resized to ${icon_size}x${icon_size}"
    echo "Saved to: $output_image"
else
    echo "Error resizing image"
    exit 1
fi