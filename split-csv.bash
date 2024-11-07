#!/usr/bin/env bash
# Script Name: split-every-two.bash
# Purpose: Splits a comma-separated list into pairs and outputs each pair on a new line
# Created Date: Nov 07, 2024
# Author: [Your Name]
# Required Packages: None
# Powered by: [HomeSetup](https://github.com/yorevs/homesetup)
# GPT: [HHS-Script-Generator](https://chatgpt.com/g/g-ra0RVB9Jo-homesetup-script-generator)

################################################################################
# AIs CAN MAKE MISTAKES.
# For your safety, verify important information and code before executing it.
#
# This program comes with NO WARRANTY, to the extent permitted by law.
################################################################################

VERSION="0.0.1" # https://semver.org/ ; major.minor.patch

# @purpose: Display version information
version() {
    echo "split-every-two.bash version ${VERSION}"
}

# @purpose: Display usage information
usage() {
    echo "Usage: split-every-two.bash <comma-separated-list>"
    echo "Example: split-every-two.bash 'item1,item2,item3,item4,item5,item6'"
}

# Check if the user needs help
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    usage
    exit 0
fi

# Check if the user needs version information
if [[ "$1" == "-v" || "$1" == "--version" ]]; then
    version
    exit 0
fi

# @purpose: Splits a comma-separated list into pairs and prints each pair on a new line.
# @param $1 [Req] : Comma-separated list.
split_every_two() {
    local input_list=$1
    local -a items
    IFS=',' read -r -a items <<< "$input_list"

    for ((i=0; i<${#items[@]}; i+=2)); do
        if [[ $((i+1)) -lt ${#items[@]} ]]; then
            echo "${items[i]},${items[i+1]}"
        else
            echo "${items[i]}"
        fi
    done
}

# Check if an argument was provided
if [[ -z "$1" ]]; then
    echo -e "\033[31mERROR\033[m: No comma-separated list provided."
    usage
    exit 1
fi

# Run the main function
split_every_two "$1"

