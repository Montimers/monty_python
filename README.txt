What does this do?
- Automated remapping sound id params in a moveset file so you don't have to do it yourself

Requirements:
- Python3.7 or higher
- Download it here if you don't have it: https://www.python.org/downloads/
    - If you're on Windows PLEASE check off the box for "add Python to PATH" otherwise you have to do it yourself and it's annoying
    - Run `python --version` in your terminal to assure you have 3.7

How to run:
- In your terminal, cd into this directory (which contains "sound_remap.py" and all dependency files)
- Fill out the "sound_mapping.txt" file and specify the sounds id to be replaced and the sound id to be replaced by
    - It needs to be formatted like this: old_value,new_value
    - The provided "sound_mapping.txt" comes with some example ids, so follow that structure to make yours
- Run in your terminal: python3 sound_remap.py moveset_file_path
    - if you place the moveset in this directory, you can just specify the moveset file's name
    - currently there is a file "test_moveset.pac" which is there as an example if you wanted to test successfully running this script
    - If successful, it will place the resulting sound remapped moveset file in the "remapped" directory
    - pay attention to the log output! it will tell you if anything goes wrong!
    - optional parameters (you can add as many as you want:
        - specify sound mapping file location: -s sound_mapping_file_path
        - specify output movest file directory: -o output_moveset_file_path
        - see more logging in case something went wrong and you can't figure it out: -v
        - example: python3 sound_remap.py test_moveset.pac -s sound_mapping.txt -o remapped/output.pac -v