import logging
import os
from constants import PSA_CODE_BOUNDARY_BYTESTRING
from utils import add_to_hex_string_length, convert_int_to_hex_string


class Moveset(object):
    """
    Class to handle moveset file manipulation
    """
    def __init__(self, original_moveset_file_path):
        """
        :param original_moveset_file_path: moveset file path
        """
        self.file_path = original_moveset_file_path

        # open up moveset file as binary
        with open(original_moveset_file_path, "rb") as binary_file:
            # create bytearray from binary file (hex)
            self.bytearray = bytearray(binary_file.read())

        # get boundary offsets for where PSA code starts and ends
        # this assures nothing gets messed up that isn't PSA code
        self.psa_start_boundary_offset, self.psa_end_boundary_offset = self.get_psa_code_boundary_offsets()

    def get_psa_code_boundary_offsets(self):
        """
        gets boundary offset indexes in moveset bytearray for where PSA code starts and ends
        this assures nothing gets messed up that isn't PSA code
        :return: psa start boundary offset index, psa end boundary offset index
        """
        # look from start of moveset file to end for the first occurrence, which will be the start offset
        psa_start_boundary_offset = self.bytearray.find(PSA_CODE_BOUNDARY_BYTESTRING)
        # look from right after the first occurence to the end for the second occurence, which will be the end offset
        psa_end_boundary_offset = self.bytearray.find(PSA_CODE_BOUNDARY_BYTESTRING, psa_start_boundary_offset + len(PSA_CODE_BOUNDARY_BYTESTRING))
        return psa_start_boundary_offset, psa_end_boundary_offset

    def get_file_size(self):
        """
        gets size of moveset file
        :return: size of moveset file (in bytes
        """
        return os.path.getsize(self.file_path)

    def remap_sound(self, sound_command_bytestring, sound_map):
        """
        Remaps the given sound command's sound id param
        Sound Map dictates which sound id params should be changed and to what value they should be changed to
        :param sound_command_bytestring: sound command to map (look in PSA for the bytestring)
        :param sound_map: Maps existing sound ids to what they should be replaced with -- both key and value should be hex strings (dictionary)
        :return: how many instances of the command were successfully remapped in the moveset bytestring
        """
        current_offset = 0
        remap_counter = 0
        # loops until every single sound command of the specified type found in the moveset's bytestring has been remapped
        while True:
            # find next Sound Effect command starting from current offset
            next_sound_command = self.__get_sound_command(sound_command_bytestring, current_offset)
            # update current offset -- this causes the next loop iteration to look for the next sound command directly after the one that was just found in this iteration
            current_offset = next_sound_command + len(hex(next_sound_command))

            # if sound command is not found, all sound commands of that type have been replaced
            if next_sound_command == -1:
                break
            # if sound command is found, remap it
            else:
                logging.info(f"Found command at {next_sound_command:X}")
                is_remap_success = self.__change_sound_id_param_value(next_sound_command, sound_map)
                if is_remap_success:
                    remap_counter += 1
        return remap_counter

    def __change_sound_id_param_value(self, sound_command_index, sound_map):
        """
        changes specific sound id param in moveset bytestring to new value according to the sound map
        :param sound_command_index: the sound command index in moveset bytestring to have its sound id param changed
        :param sound_map: Maps existing sound ids to what they should be replaced with -- both key and value should be hex strings (dictionary)
        :return: if changing the sound id param was successful or not (boolean)
        """
        # get location where params for sound command exist
        command_param_index = self.__get_param_offset_for_sound_command(sound_command_index)

        logging.debug(f"Param offset for command: {command_param_index:X}")
        # get actual sound id param (this is the value that will be remapped!)
        sound_id_param = self.__get_sound_id_param_offset(command_param_index)

        logging.debug(f"Current Sound Id param offset for command: {sound_id_param:X}")

        # if current sound id param is found in sound map, remap it to new_sound_value it is associated with
        sound_id_param_hex_string = convert_int_to_hex_string(sound_id_param)
        if sound_id_param_hex_string in sound_map.keys():
            old_sound_value = sound_id_param_hex_string
            new_sound_value = sound_map[old_sound_value]

            logging.debug(f"Sound Id param for command will be remapped from {old_sound_value} to {new_sound_value}")

            # format new sound value so that it is at least 8 characters in order for the replace to go smoothly
            new_sound_value = add_to_hex_string_length(new_sound_value, 8, "0")
            # replace sound id param -- this will replace four bytes in the moveset bytestring with our new value
            self.bytearray[command_param_index: command_param_index + 4] = bytearray.fromhex(new_sound_value)
            is_remap_success = True
        # if current sound id param is not found in sound map, no remap can be done :(
        else:
            logging.warning(f"Unable to remap Sound Id param for command at {command_param_index:X} from sound id param {int(sound_id_param):X} to a new value")
            logging.warning(f"Make sure {int(sound_id_param):X} is listed in your sound mapping file with a new value associated with it!")
            is_remap_success = False

        return is_remap_success

    def __get_sound_command(self, sound_command_bytestring, offset):
        """
        gets next sound command in moveset bytestring
        :param sound_command_bytestring: sound command bytestring to look for
        :param offset: how far from the start of the moveset bytestring should be looked through to find the sound command
        :return: index of sound command
        """
        return self.bytearray.find(sound_command_bytestring, self.psa_start_boundary_offset + offset)

    def __get_param_offset_for_sound_command(self, sound_command_index):
        """
        given a sound command index, get its param's location index in the moveset bytestring
        :param sound_command_index: index of sound command to get param's location index of
        :return: index of params for sound command
        """
        return int.from_bytes(self.bytearray[sound_command_index + 4: sound_command_index + 8], byteorder='big', signed=False) + 132

    def __get_sound_id_param_offset(self, command_param_index):
        """
        given a command's param location index, get the value of the sound id param
        :param command_param_index: command's param location index
        :return: sound id param value
        """
        return int.from_bytes(self.bytearray[command_param_index: command_param_index + 4], byteorder='big', signed=False)
