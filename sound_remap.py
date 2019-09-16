import argparse
import logging
import os
from moveset import Moveset
from constants import SOUND_COMMANDS

"""
SOUND REMAPPER!!!
Uses Python3.7 or greater!
"""

def parse_args():
    """
    Parse command line arguments
    :return: parsed args
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("moveset_file_path", metavar="MOVESET_FILE_PATH", help="File path to your moveset.pac file")
    parser.add_argument("-o", "--output_remapped_moveset_file_path", metavar="OUTPUT_FILE_PATH", help="File path to your new sound remapped moveset.pac")
    parser.add_argument("-s", "--sound_map_file_path", default="sound_mapping.txt", metavar="SOUND_MAP_FILE_PATH", help="File path to your sound map text file")
    parser.add_argument("-v", "--verbose", action='store_true', help="More verbose logging (useful when debugging)")
    return parser.parse_args()


def main():
    """
    Runs Sound Remapper on a moveset file
    Check README file for instructions
    :return: exit code
    """

    '''
    Set Up
    '''
    # parse command line arguments
    args = parse_args()

    # Set up logging
    if args.verbose:
        logging_level = logging.DEBUG
    else:
        logging_level = logging.INFO

    logging.basicConfig(
        level=logging_level,
        format='[%(asctime)s] %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )

    '''
    Sound Map
    '''
    # Construct sound map from sound mapping text file
    logging.info(f"Constructing Sound Map from Sound Map File: {args.sound_map_file_path}")
    try:
        with open(args.sound_map_file_path) as sound_mapping_file:
            # Create dictionary of:
            #   - key: old sound
            #   - value: new sound
            sound_map = {}
            for sound_pairing in sound_mapping_file.read().strip("\n").split("\n"):
                sounds = sound_pairing.split(",")
                old_sound = sounds[0].strip()
                new_sound = sounds[1].strip()
                logging.debug(f"Mapping sound {old_sound} to {new_sound}")
                sound_map[old_sound] = new_sound
    except (IOError, ValueError) as e:
        # Program doesn't really work if the sound map can't be properly read in, so bail out in the case of any errors doing so
        logging.error(e)
        if IOError:
            logging.error(f"Unable to find Sound Map file {args.sound_map_file_path}! Double check your file path!")
        elif ValueError:
            logging.error(f"Found Sound Map file {args.sound_map_file_path} but unable to parse it properly! Make sure your sound map file is in the format:\n'old_sound,new_sound'")
        return -1

    logging.debug(f"Sound Map:\n{sound_map}")

    '''
    Moveset
    '''
    # create Moveset object
    try:
        moveset = Moveset(args.moveset_file_path)  # Moveset object defined in moveset.py
    except IOError as e:
        # Program doesn't really work if the moveset can't be properly read in, so bail out in the case of any errors doing so
        logging.error(e)
        logging.error(f"Unable to read in moveset file {args.moveset_file_path}! :(")
        return -1

    '''
    Remap Sounds
    '''
    # loops through each PSA Sound Command (defined in constants.py) and remaps each one's Sound Id param according to the Sound Map
    for sound_command_name, sound_command_bytestring in SOUND_COMMANDS.items():
        logging.info(f"Remapping command '{sound_command_name}'")
        remap_counter = moveset.remap_sound(sound_command_bytestring, sound_map)
        logging.info(f"Finished remapping {remap_counter} sounds for command {sound_command_name}")

    '''
    Export file
    '''
    # set up default output file if nothing entered (nobody ever does...)
    if not args.output_remapped_moveset_file_path:
        output_remapped_moveset_file_path = f"remapped/{args.moveset_file_path}"
        if not os.path.exists("remapped"):
            os.mkdir("remapped")
    else:
        output_remapped_moveset_file_path = args.output_remapped_moveset_file_path

    # in the case that the output file already exists in the given directory, add a unique identifying number so it will not replace the old file
    counter = 1
    filename, file_extension = os.path.splitext(output_remapped_moveset_file_path)
    while os.path.exists(output_remapped_moveset_file_path):
        output_remapped_moveset_file_path = f"{filename}_{counter}{file_extension}"
        counter += 1

    # create the output moveset file with remapped sounds
    with open(output_remapped_moveset_file_path, 'wb') as output_file:
        output_file.write(moveset.bytearray)

    return 0


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)



