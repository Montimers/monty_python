# in moveset file, PSA code starts and ends with this byte string
PSA_CODE_BOUNDARY_BYTESTRING = b'\x41\x52\x43'

# the PSA sound commands that will be remapped
SOUND_COMMANDS = {
    "Sound Effect": b'\x0A\x00\x01\x00',
    "Sound Effect 2": b'\x0A\x01\x01\x00',
    "Stop Sound Effect": b'\x0A\x03\x01\x00',
    "Sound Effect (Transient)": b'\x0A\x02\x01\x00',
    "Other Sound Effect (landing)": b'\x0A\x09\x01\x00',
    "Other Sound Effect (impact)": b'\x0A\x0A\x01\x00',
    "Victory": b'\x0A\x05\x01\x00',
    "Stepping Sound Effect": b'\x0A\x01\x01\x00'
}
