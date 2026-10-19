import pandas as pd
from typing import Any, Optional


class GuildMember:
    """A concise one-line summary of the class's purpose.

    Detailed description of the class, its responsibilities, and how it
    should be used within the application.

    Attributes:
        instance_var (str): Purpose of this instance-level variable.
        _private_var (int): Purpose of this internal/private variable.
    """

    def __init__(self, ally_code: int, name: str = None, discord_tag: str = None) -> None:
        """Initializes the class attributes upon instantiation."""
        # Public instance variables
        self.ally_code: int = ally_code
        self.name: str = name
        self.discord_tag: str = name

        # Protected/Private instance variable (indicated by a leading underscore)
        self._tb_actions: pd.DataFrame = pd.DataFrame(columns=["CurrentRoundEndTime", "Instance", "MapStatId", "Score", "SpecialResults"])
        self._tw_actions: pd.DataFrame = pd.DataFrame(columns=["CurrentRoundEndTime", "Instance", "MapStatId", "Score"])
        self._raid_actions: pd.DataFrame = pd.DataFrame(columns=["ExpireTime", "RaidId", "Score", "Rank"])
        # This starts blank. As ticket files are processed, this will build out.
        # Days in guild as keys.
        self._ticket_actions: dict = {}

    def __repr__(self) -> str:
        """Returns an unambiguous string representation for developers and debugging."""
        return (
            f"{self.__class__.__name__}("
            f"required_param={self.instance_var!r}, "
            f"optional_param={self.optional_param!r})"
        )

    def __str__(self) -> str:
        """Returns a user-friendly string representation of the object."""
        return f"Custom Class with value: {self.instance_var}"

    def public_method(self, data: Any) -> bool:
        """Performs a primary operation for the class.

        Args:
            data (Any): Description of the input parameter.

        Returns:
            bool: Description of the return value.
        """
        if not data:
            return False
        self._private_method(data)
        return True

    def _private_method(self, data: Any) -> None:
        """Internal helper method. Not intended to be called directly by clients."""
        self._private_var += 1


# ==========================================
# Example Usage
# ==========================================
if __name__ == "__main__":
    # Instantiating the object
    obj = GuildMember(ally_code=123456789)

    # Accessing methods and attributes
    print(obj)  # Triggers __str__
    print(f"Debug info: {obj!r}")  # Triggers __repr__

    success = obj.public_method("Process this data")
    print(f"Operation status: {success}")
