max_distance = 100

for current_distance in range(max_distance+1):
    strength = 1 - current_distance / max_distance
    # Strength will be maxed and equal to 1 if current_distance/max_distance = 0.5 or lower
    strength = 2 * strength if strength < 0.5 else 1

    print(current_distance, strength)
