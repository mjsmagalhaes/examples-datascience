from typing import Tuple
from datetime import date


class Mask:
    def __init__(self, flags):
        self.flags = self.hex_to_binary(flags)

    def hex_to_binary(self, hex_number: str, num_digits: int = 64) -> str:
        """
        Converts a hexadecimal value into a string representation
        of the corresponding binary value.

        Args:
          hex_number: str hexadecimal value
          num_digits: integer value for length of binary value.
                        defaults to 8

        Returns:
          string representation of a binary number 0-padded
          to a minimum length of <num_digits>
        """
        return bin(int(hex_number, 16))[2:].zfill(num_digits)[::-1]

    @property
    def hostile(self):
        return self.flags[6] == '1'


class Record:
    """
    Represents a line in the log file.
    """

    def __init__(self, log: Tuple[int, str]):
        self.idx = log[0]
        self.timestamp, self.rawdata = log[1].split('  ')

        # if(self.event in [
        #     'COMBAT_LOG_VERSION', 'ZONE_CHANGE', 'MAP_CHANGE',
        #     'COMBATANT_INFO',
        #     'UNIT_DIED', 'PARTY_KILL',
        #     'ENCOUNTER_START', 'ENCOUNTER_END',
        #     'WORLD_MARKER_PLACED', 'WORLD_MARKER_REMOVED',
        #     'EMOTE'
        # ]):

    # def __str__(self) -> str:
    #   return '{timestamp}: {event}'.format(**self.__dict__)

    def __repr__(self) -> str:
        return f'{self.idx} - {self.timestamp}: {self.rawdata}'

    def __getitem__(self, idx):
        if type(idx) is str:
            return self.__dict__.get(idx, None)
        if type(idx) is int:
            try:
                return self.data[idx]
            except IndexError:
                return None
        else:
            return None

    @property
    def data(self):
        return self.rawdata.split(',')

    @property
    def event(self):
        return self[0]

    @property
    def actor_id(self):
        return self[1]

    @property
    def actor(self):
        return self[2]

    @property
    def actor_flags(self):
        return self[3]

    @property
    def actor_tag(self) -> Mask:
        return self.actor_id.split('-')[0]

    @property
    def actor_mask(self) -> Mask:
        return Mask(self.actor_flags)

    @property
    def target_id(self):
        return self[5]

    @property
    def target(self):
        return self[6]

    @property
    def target_flags(self):
        return self[7]

    @property
    def target_tag(self) -> Mask:
        return self.target_id.split('-')[0]

    @property
    def target_mask(self) -> Mask:
        return Mask(self.target_flags)

    @property
    def action_id(self) -> int:
        r = self[9]
        if r:
            return int(r)
        else:
            return None

    @property
    def action(self) -> str:
        return self[10]

    def getTimestamp(self) -> data.datetime:
        return date.datetime.strptime(
            self.timestamp, '%m/%d %H:%M:%S.%f'
        ).replace(year=2022)

    def getTimestampString(self) -> str:
        return self.getTimestamp().isoformat()
