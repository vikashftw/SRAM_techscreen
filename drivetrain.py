"""
SRAM Tech Screen Solution (Python 3.12.6)

We define a Drivetrain class that:
  1. Stores front and rear cogs tooth counts as a list of integers.
  2. Includes a method (get_gear_combination) that determines the gear combination
     providing the closest ratio that is less than or equal to the target ratio.
  3. Includes  a method (get_shift_sequence) that returns a shift sequence to traverse
     from an initial gear combination to a gear combination with the closest ratio that
     is less than or equal to the target ratio. First shifts the front to the target gear,
     then shifts the rear step-by-step to the target gear.
  4. Includes a method (format_shift_sequence) that produces a formatted shift sequence for
     a given target ratio and initial gear combination.

There's also a small unittest suite at the bottom to verify that
the functionality behaves as expected.
"""


class GearRatioNotFoundError(Exception):
    """Raised when no gear combination is <= a specified target ratio."""
    pass


class Drivetrain:
    """
    This class models a bicycle drivetrain with a set of front cogs and rear cogs. It's designed
    to find a gear combination that approximates a desired ratio and to generate a step-by-step
    shift sequence to get there.
    """
    def __init__(self, front_cogs, rear_cogs):
        """
        Initializes the Drivetrain with sorted front and rear cogs. Sorting them
        makes it easier to shift up or down in the correct order.
        
        :param front_cogs: A list of integers representing the tooth counts
                           of the front cogs.
        :param rear_cogs: A list of integers representing the tooth counts
                          of the rear cogs.
        """
        self.front_cogs = sorted(front_cogs)
        self.rear_cogs = sorted(rear_cogs)

    @staticmethod
    def gear_ratio(front_teeth, rear_teeth):
        """
        This is a helper method that calculates the gear ratio and returns it as a float.
        
        :param front_teeth: Tooth count on selected front cog.
        :param rear_teeth: Tooth count on selected rear cog.
        :return: Floating-point gear ratio.
        """
        return front_teeth / rear_teeth
    
    def get_gear_combination(self, target_ratio):
        """
        Determines the gear combination providing the closest ratio that is less than or
        equal to the target ratio.
        
        :param target_ratio: The maximum allowed gear ratio.
        :return: (front_teeth, rear_teeth, ratio)
        :raises GearRatioNotFoundError: If no combination is <= target_ratio.
        """
        valid_combinations = []
        for f in self.front_cogs:        # f-> 30, 38
            for r in self.rear_cogs:     # r -> 16, 19, 23, 28
                ratio = self.gear_ratio(f, r)
                if ratio <= target_ratio:
                    valid_combinations.append((f, r, ratio))

        if not valid_combinations:
            raise GearRatioNotFoundError(
                f"No gear ratio found that is <= {target_ratio}."
            )

        valid_combinations.sort(key=lambda combo: combo[2], reverse=True)
        return valid_combinations[0]
    
    def get_shift_sequence(self, target_ratio, initial_gear):
        """
        Generates a list of (front, rear, ratio) steps that start from the
        initial_gear (a list of [front_teeth, rear_teeth]) and end at the
        combination that best matches (but doesn't exceed) the target_ratio.
        
        The shifting approach is:
          1) Jump directly to the final front cog.
          2) Step through the rear cogs one at a time until reaching the final rear cog.
        
        :param target_ratio: The maximum allowed gear ratio.
        :param initial_gear: List [front_teeth, rear_teeth] describing the starting gears.
        :return: A list of (front_teeth, rear_teeth, ratio) for each shift step.
        """
        best_combo = self.get_gear_combination(target_ratio)
        final_front, final_rear, _ = best_combo
        current_front, current_rear = initial_gear

        shift_sequence = []

        def record_step(f, r):
            shift_sequence.append((f, r, self.gear_ratio(f, r)))

        # Record initial gear
        record_step(current_front, current_rear)

        # Switch front cog directly
        if current_front != final_front:
            current_front = final_front
            record_step(current_front, current_rear)

        # Step through rear cogs
        if current_rear != final_rear:
            #if final rear cog is greater than current rear cog, move up in rear cogs
            if final_rear > current_rear:
                # Ascending through the rear cogs
                candidate_rears = [r for r in self.rear_cogs if r >= current_rear]
            #if final rear cog is smaller than current rear cog, move down in rear cogs
            else:
                # Descending through the rear cogs
                candidate_rears = [r for r in reversed(self.rear_cogs) if r <= current_rear]

            
            #candidate_rears = All possible rear cogs we can shift through
            step_index = candidate_rears.index(current_rear)   #find index of current rear
            final_index = candidate_rears.index(final_rear)    #find index of final rear

            if final_index >= step_index: #shifting to larger cog -> move forward in list
                step_range = range(step_index, final_index + 1)
            else:
                step_range = range(step_index, final_index - 1, -1)

            for i in step_range:
                new_rear = candidate_rears[i]
                if new_rear != current_rear:
                    current_rear = new_rear
                    record_step(current_front, current_rear)

        return shift_sequence
    
    def format_shift_sequence(self, shift_sequence):
        """
        Returns a multiline string describing each step in the shift sequence.
        
        :param shift_sequence: List of (front_teeth, rear_teeth, ratio).
        :return: A multiline string with each step on its own line.
        """
        lines = []
        for (f, r, ratio) in shift_sequence:
            lines.append(f"Front: {f}, Rear: {r}, Ratio: {ratio:.3f}")
        return "\n".join(lines)
    

if __name__ == "__main__":
    drivetrain = Drivetrain(front_cogs=[38, 30], rear_cogs=[28, 23, 19, 16])
    initial_gear = [38, 28]
    target_ratio = 1.6

    best_combo = drivetrain.get_gear_combination(target_ratio)
    print(f"Best gear combination: {best_combo}")

    shift_sequence = drivetrain.get_shift_sequence(target_ratio, initial_gear)
    print("\nShift sequence:")
    print(drivetrain.format_shift_sequence(shift_sequence))