import unittest
from drivetrain import Drivetrain, GearRatioNotFoundError


class TestDrivetrain(unittest.TestCase):
    """
    Tests the Drivetrain class for:
      - Correctness of gear ratios
      - Valid gear combinations under a target ratio
      - Error handling for invalid ratios
      - Shift sequence generation
      - Output formatting
    """

    def setUp(self):
        """Default drivetrain setup."""
        self.drivetrain = Drivetrain(front_cogs=[30, 38], rear_cogs=[16, 19, 23, 28])

    def test_gear_ratio_calculation(self):
        """Test the gear ratio calculation for various inputs."""
        self.assertAlmostEqual(
            self.drivetrain.gear_ratio(38, 19),
            2.0,
            msg="Gear ratio for (38, 19) should be 2.0, but it isn't.",
        )
        self.assertAlmostEqual(
            self.drivetrain.gear_ratio(30, 15),
            2.0,
            msg="Gear ratio for (30, 15) should be 2.0, but it isn't.",
        )
        self.assertAlmostEqual(
            self.drivetrain.gear_ratio(38, 23),
            1.652,
            places=3,
            msg="Gear ratio for (38, 23) should be approximately 1.652.",
        )

    def test_find_valid_gear_combination(self):
        """Test finding a valid gear combination within a target ratio."""
        target_ratio = 1.6
        combo = self.drivetrain.get_gear_combination(target_ratio)
        front, rear, ratio = combo
        self.assertLessEqual(
            ratio,
            target_ratio,
            f"Ratio exceeds the target. Expected <= {target_ratio}, but got {ratio}.",
        )
        self.assertIn(
            front,
            self.drivetrain.front_cogs,
            f"Front cog {front} is not in the drivetrain front cogs {self.drivetrain.front_cogs}.",
        )
        self.assertIn(
            rear,
            self.drivetrain.rear_cogs,
            f"Rear cog {rear} is not in the drivetrain rear cogs {self.drivetrain.rear_cogs}.",
        )

    def test_no_valid_gear_combination(self):
        """Test handling of cases where no valid combination exists."""
        target_ratio = 0.3
        with self.assertRaises(GearRatioNotFoundError, msg=f"No combination should exist for target ratio {target_ratio}."):
            self.drivetrain.get_gear_combination(target_ratio)

    def test_generate_shift_sequence(self):
        """Test generating the shift sequence to match a target ratio."""
        initial_gear = [38, 28]
        target_ratio = 1.6
        sequence = self.drivetrain.get_shift_sequence(target_ratio, initial_gear)

        # Validate the sequence
        self.assertTrue(len(sequence) > 0, "Shift sequence is empty.")
        for step in sequence:
            front, rear, ratio = step
            self.assertIn(
                front,
                self.drivetrain.front_cogs,
                f"Invalid front cog {front} in sequence. Expected one of {self.drivetrain.front_cogs}.",
            )
            self.assertIn(
                rear,
                self.drivetrain.rear_cogs,
                f"Invalid rear cog {rear} in sequence. Expected one of {self.drivetrain.rear_cogs}.",
            )
        self.assertLessEqual(
            sequence[-1][2],
            target_ratio,
            f"Final ratio in sequence exceeds target. Expected <= {target_ratio}, but got {sequence[-1][2]}.",
        )

    def test_format_shift_sequence_output(self):
        """Test the formatting of the shift sequence output."""
        sequence = [(30, 19, 1.5789), (30, 16, 1.875)]
        formatted = self.drivetrain.format_shift_sequence(sequence)
        self.assertIn(
            "Front: 30, Rear: 19, Ratio: 1.579",
            formatted,
            "Formatted output missing expected entry for Front: 30, Rear: 19.",
        )
        self.assertIn(
            "Front: 30, Rear: 16, Ratio: 1.875",
            formatted,
            "Formatted output missing expected entry for Front: 30, Rear: 16.",
        )

    def test_empty_drivetrain(self):
        """Test behavior with empty front or rear cogs."""
        empty_drivetrain = Drivetrain(front_cogs=[], rear_cogs=[16, 19])
        with self.assertRaises(
            GearRatioNotFoundError, msg="Expected error for empty front cogs."
        ):
            empty_drivetrain.get_gear_combination(1.5)

        empty_drivetrain = Drivetrain(front_cogs=[30], rear_cogs=[])
        with self.assertRaises(
            GearRatioNotFoundError, msg="Expected error for empty rear cogs."
        ):
            empty_drivetrain.get_gear_combination(1.5)

    def test_invalid_initial_gear(self):
        """Test behavior when initial gear is not valid."""
        initial_gear = [40, 30]  # Not in drivetrain
        target_ratio = 1.5
        with self.assertRaises(ValueError, msg=f"Expected ValueError for invalid initial gear {initial_gear}."):
            self.drivetrain.get_shift_sequence(target_ratio, initial_gear)


if __name__ == "__main__":
    unittest.main()
