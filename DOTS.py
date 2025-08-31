from termcolor import colored

class DOTEffect:
    def __init__(self, name, damage_per_turn, duration, source = None):
        self.name = name
        self.damage_per_turn = damage_per_turn
        self.duration = duration
        self.source = source 

    def apply(self, target):
        if self.duration <= 0:
            return 0

        damage = max(1, self.damage_per_turn - (target.armor * 0.1))
        self.duration -= 1
        
        if self.duration <= 0:
            print(f"{colored(self.name, 'yellow')} effect has worn off {target.name}.")
            
        return damage
    
    def is_expired(self):
        return self.duration <= 0
    
class BleedDOT(DOTEffect):
    def __init__(self, damage_per_turn, duration, source=None):
        super().__init__("Bleeding", damage_per_turn, duration, source)

class InfectionDOT(DOTEffect):
    def __init__(self, damage_per_turn, duration, source=None):
        super().__init__("Infection", damage_per_turn, duration, source)

class DOTManager:
    def __init__(self):
        self.active_dots = []

    def add_dot(self, dot_effect):
        for i, existing_dot in enumerate(self.active_dots):
            if existing_dot.name == dot_effect.name:
                if dot_effect.damage_per_turn > existing_dot.damage_per_turn:
                    self.active_dots[i] = dot_effect
                    print(f"{colored(dot_effect.name, 'magenta')} effect refreshed!")
                    return
                else:
                    print(f"{colored(dot_effect.name, 'yellow')} resisted - stronger effect already active!")
                    return
                
        self.active_dots.append(dot_effect)
        print(f"{colored(dot_effect.name, 'magenta')} effect applied!")

    def process_dots(self, target):
        total_damage = 0

        for dot in self.active_dots[:]:
            damage = dot.apply(target)
            if damage > 0:
                print(f"{target.name} takes {colored(round(damage, 2), 'red')} {dot.name} damage!")
            total_damage += damage

        # Remove expired DOTs
        self.active_dots = [dot for dot in self.active_dots if not dot.is_expired()]
        
        return total_damage

    def has_dot(self, dot_name):
        return any(dot.name == dot_name for dot in self.active_dots)
        
    def get_dot_info(self):
        if not self.active_dots:
            return ""
        
        dot_info = []
        for dot in self.active_dots:
            dot_info.append(f"{dot.name}({dot.duration})")
        return " | ".join(dot_info)