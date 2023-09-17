import argparse

import terminaltexteffects.utils.argtypes as argtypes
from terminaltexteffects import base_effect
from terminaltexteffects.utils.terminal import Terminal


def add_arguments(subparsers: argparse._SubParsersAction) -> None:
    """Adds arguments to the subparser.

    Args:
        subparser (argparse._SubParsersAction): subparser to add arguments to
    """
    effect_parser = subparsers.add_parser(
        "expand",
        help="Expands the text from a single point.",
        description="expand | Expands the text from a single point.",
        epilog="Example: terminaltexteffects expand -a 0.01",
    )
    effect_parser.set_defaults(effect_class=ExpandEffect)
    effect_parser.add_argument(
        "-a",
        "--animation-rate",
        type=argtypes.valid_animationrate,
        default=0.01,
        help="Time between animation steps. Defaults to 0.01 seconds.",
    )


class ExpandEffect(base_effect.Effect):
    """Effect that draws the characters expanding from a single point."""

    def __init__(self, terminal: Terminal, args: argparse.Namespace):
        super().__init__(terminal)

    def prepare_data(self) -> None:
        """Prepares the data for the effect by starting all of the characters from a point in the middle of the input data."""

        for character in self.terminal.characters:
            character.motion.set_coordinate(self.terminal.output_area.right // 2, self.terminal.output_area.top // 2)
            character.motion.new_waypoint(
                character.input_coord.column,
                character.input_coord.row,
                speed=0.5,
                ease=character.motion.ease.IN_OUT_QUART,
            )
            self.animating_chars.append(character)

    def run(self) -> None:
        """Runs the effect."""
        self.prepare_data()
        self.terminal.print()
        while self.animating_chars:
            self.animate_chars()
            self.animating_chars = [
                animating for animating in self.animating_chars if not animating.motion.movement_complete()
            ]
            self.terminal.print()

    def animate_chars(self) -> None:
        for animating_char in self.animating_chars:
            animating_char.motion.move()
