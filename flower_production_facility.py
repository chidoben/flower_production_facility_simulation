"""
This module simulates a flower production facility.
It takes as input bouquet designs and a stream of flowers
and prints a bouquet to the screen every time one can be
created from the available flowers according to one of the provided bouquet designs.
"""

import re
from collections import Counter, defaultdict
from typing import List, Dict, DefaultDict


def production_facility(input_file: str) -> None:
    """
    Simulates a flower production facility. It takes as input a file containing bouquet designs and flowers. It extracts
    the bouquets designs from the file and adds them to container structures depending on whether they are composed of
    large or Small flowers.
    It extracts the flowers from the input file. For each flower in the stream of flowers from the input file it first
    determines whether the flower is a large or small flower and then examines the correct bouquet designs container to
    see if there is a bouquet that can be made using that flower and all the previous flowers that have been retrieved
    from the stream of flowers. As soon as it finds a match it prints the output to the console. If a match is not found
    it saves the flower, then picks another flower from the stream of input flowers and repeats the same process.
    Parameters:
       input_file(str): The name of the input file to be read
    Returns:
       None
    """
    input_stream = get_input_stream(input_file)

    bouquet_designs = extract_bouquet_designs_from_input_stream(input_stream)
    stream_of_flowers = extract_flowers_from_input_stream(input_stream)

    small_bouquet_designs = {}
    large_bouquet_designs = {}

    for bouquet_design in bouquet_designs:
        if 'L' in bouquet_design:
            create_bouquet_designs_matching_structure(bouquet_design, large_bouquet_designs)
        else:
            create_bouquet_designs_matching_structure(bouquet_design, small_bouquet_designs)

    large_flowers_counter = defaultdict(int)
    small_flowers_counter = defaultdict(int)

    for flower in stream_of_flowers:
        if flower[1] == 'L':
            match_flower_streams_with_bouquet_design_structures(flower, large_bouquet_designs, large_flowers_counter)
        else:
            match_flower_streams_with_bouquet_design_structures(flower, small_bouquet_designs, small_flowers_counter)


def match_flower_streams_with_bouquet_design_structures(flower: str, bouquet_designs: Dict,
                                                        flowers_counter: DefaultDict) -> None:
    """
    Takes as input a flower that has been taken from the stream of flowers. It increments the counter for that
    flower type and then tries to see if a bouquet can be created. For each bouquet design it does this by examining
    the type of flowers in them and the number of each flower type. It then examines the flower counter to see if there
    are enough flowers of each flower type to make a bouquet. We then check the total number of flowers needed to make a
    bouquet from that bouquet design and compare it to the total number of flowers that have currently been picked from
    the flower stream to see if the flower ty.

    Parameters:
       flower(str): The flower from the stream of flowers
       bouquet_designs(Dict): The container of bouquet designs
       flowers_counter(DefaultDict): A counter that holds the total number of streamed flowers for each flower type
    Returns:
       None
    """
    flowers_counter[flower[0]] += 1

    for bouquet_name in bouquet_designs.keys():
        matching_flower_numbers = {key: flowers_counter[key] for key in flowers_counter if
                                   key in bouquet_designs[bouquet_name]['flowers'] and flowers_counter[key] >= int(
                                       bouquet_designs[bouquet_name]['flowers'][key])}
        # Check if we have enough flowers in the flowers counter to make a bouquet from this bouquet design
        if len(matching_flower_numbers) == len(bouquet_designs[bouquet_name]['flowers']):
            number_of_additional_flowers = int(bouquet_designs[bouquet_name]['total_number_of_flowers']) - sum(
                [int(value) for value in bouquet_designs[bouquet_name]['flowers'].values()])
            # Subtract the flowers used for making this bouquet from the flowers we have taken from the flower stream
            # so far
            for key in flowers_counter:
                if key in bouquet_designs[bouquet_name]['flowers']:
                    flowers_counter[key] = flowers_counter[key] - int(bouquet_designs[bouquet_name]['flowers'][key])
            # If from the bouquet design the total number of flowers is greater than the sum of the individual flowers
            # then we need to subtract those additional flowers as well from the flowers we have taken from the flower
            # stream
            if number_of_additional_flowers > 0:
                for key in flowers_counter:
                    if flowers_counter[key] >= number_of_additional_flowers:
                        flowers_counter[key] = flowers_counter[key] - number_of_additional_flowers
                        break

            print(bouquet_designs[bouquet_name]['bouquet'])


def create_bouquet_designs_matching_structure(bouquet_design: str, bouquet_designs_container: Dict) -> None:
    """
    Creates a dictionary structure of bouquet designs. This structure will be used to match flower streams with bouquet
    designs that can be created using the available stream of flowers. The structure being created is just for our own
    convenience to make the matching between flowers and bouquet designs easier.
    An example bouquet design matching structure is given below:
    {'A': {'total_number_of_flowers': '25', 'flowers': {'a': '10', 'b': '10'}, 'bouquet': 'AS10a10b'},
    'B': {'total_number_of_flowers': '16', 'flowers': {'b': '10', 'c': '5'}, 'bouquet': 'BS10b5c'}}

    Parameters:
        bouquet_design(str): The bouquet design to be added to the container.
        bouquet_designs_container(Dict): The dictionary to add the bouquet design to. There are 2 different dictionaries
                                         depending on whether the bouquet design is composed of large or small flowers
    Returns:
        None
    """
    bouquet_designs_container[bouquet_design[0]] = {}
    number_of_flowers = re.findall(r'\d+', bouquet_design[2:])
    flower_names = re.findall(r'[a-z]', bouquet_design[2:])
    total_number_of_flowers = number_of_flowers.pop()
    bouquet_designs_container[bouquet_design[0]]['total_number_of_flowers'] = total_number_of_flowers
    bouquet_designs_container[bouquet_design[0]]['flowers'] = dict(zip(flower_names, number_of_flowers))
    bouquet_designs_container[bouquet_design[0]]['bouquet'] = bouquet_design.replace(total_number_of_flowers, '')


def get_input_stream(input_file: str) -> str:
    """
    Takes the name of the input file as an input, reads and returns the
    contents of the file
    Parameters:
        input_file(str): The name of the input file to be read
    Returns:
        A string containing the contents of the file
    Return type:
        str
    """
    with open(input_file) as file_handle:
        input_stream = file_handle.read()
    return input_stream


def extract_bouquet_designs_from_input_stream(input_stream: str) -> List:
    """
    Takes as input a string containing the contents of the input file and uses
    regular expressions to extract bouquet designs from the contents of the input file.
    Parameters:
        input_stream(str): The contents of the input file
    Returns:
        A list containing all the bouquet designs extracted from the input string
    Return type:
        List
    """
    return re.findall(r'[A-Z][LS][\d+a-z]+\d+', input_stream)


def extract_flowers_from_input_stream(input_stream: str) -> List:
    """
    Takes as input a string containing the contents of the input file and uses
    regular expressions to extract flowers from the contents of the input file.
    Parameters:
        input_stream(str): The contents of the input file
    Returns:
        A list containing all the flowers extracted from the input string
    Return type:
        List
    """
    return re.findall(r'[a-z][LS]', input_stream)


if __name__ == '__main__':
    input_file_name = "sample.txt"
    production_facility(input_file_name)
