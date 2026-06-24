import numpy as np
import vpython as vp
from time import sleep

OFFSETS = np.array([
    [ 0.0,  0.1,  0.0 ],
    [ 0.0, -0.1,  0.0 ],
    [ 0.1,  0.1,  0.05],
    [ 0.1, -0.1, -0.05],
    [ 0.0,  0.0,  0.1 ],
    [ 0.0,  0.0, -0.1 ],
    [ 0.1,  0.0,  0.1 ],
    [ 0.1,  0.0, -0.1 ],
    [ 0.1,  0.1,  0.3 ],
    [ 0.1, -0.1, -0.3 ],
    [ 0.1,  0.1, -0.3 ],
    [ 0.1, -0.1,  0.3 ],
    [ 0.1,  0.1, -0.05],
    [ 0.1, -0.1,  0.05],
    [ 0.1,  0.0,  0.0 ],
    [-0.1,  0.1,  0.05],
    [-0.1, -0.1, -0.05],
    [-0.1,  0.1, -0.05],
    [-0.1, -0.1,  0.05],
    [-0.1,  0.1,  0.3 ],
    [-0.1, -0.1, -0.3 ],
    [-0.1,  0.1, -0.3 ],
    [-0.1, -0.1,  0.3 ],
    [-0.1,  0.0,  0.1 ],
    [-0.1,  0.0, -0.1 ],
    [-0.1,  0.0,  0.0 ]
])

class Charge:
    def __init__(self, position: np.ndarray, charge: float, scale: float = 1.0):
        '''
        Initialize a Charge object.

        Parameters
        ----------
        position : np.ndarray
            A numpy array representing the (x, y, z) coordinates of the charge's position.
        charge   : float
            The magnitude of the charge. Positive for positive charges, negative for negative charges.
        scale    : float, optional
            A scaling factor for the visual representation of the charge. Default is 1.0.
        '''

        self.position = position
        self.charge   = charge
        self.scale    = scale

        self.q_ball = vp.sphere(
            pos    = vp.vector(*self.position),
            color  = vp.color.red if self.charge > 0 else vp.color.blue,
            radius = self.scale * abs(self.charge)
        )

        return;

    def __str__(self):
        color = 'Red' if self.charge > 0 else 'Blue'

        return f'{color} charge = {self.charge}C / Position = {self.position}';

    def calculate_electric_field(self, point: np.ndarray) -> np.ndarray:
        '''
        Calculate the electric field vector at a given point due to this charge.

        Parameters
        ----------
        point : np.ndarray
            A numpy array representing the (x, y, z) coordinates of the point where the electric field is calculated.

        Returns
        -------
        np.ndarray
            A numpy array representing the electric field vector at the given point.
        '''

        if self.charge > 0:
            distance_vector = point - self.position
        else:
            distance_vector = self.position - point
        distance_magnitude = np.linalg.norm(distance_vector)
        direction_unit     = distance_vector / distance_magnitude

        k           = 8.99e9 # Coulomb's constant
        E_magnitude = (k * abs(self.charge)) / (distance_magnitude * distance_magnitude)
        E_vector    = E_magnitude * direction_unit

        return E_vector;

class ChargeSystem:
    def __init__(self, charges: list):
        '''
        Initialize a ChargeSystem object.
        
        Parameters
        ----------
        charges : list
            A list of Charge objects.
        '''

        self.charges = charges

        return;

    def draw_electric_field(self, point: np.ndarray, farthest_distance: float = 300.0):
        '''
        Draw the electric field line starting from a given point.
        
        Parameters
        ----------
        point : np.ndarray
            A numpy array representing the (x, y, z) coordinates of the starting point for the electric field line.
        
        farthest_distance : float, optional
            The maximum distance the field line will extend from the starting point. Default is 300.0.
        '''

        ball = vp.sphere(
            pos        = vp.vector(*point),
            color      = vp.color.black,
            radius     = 0.1,
            make_trail = True,
            retain     = 300
        )

        starting_point  = point.copy()
        previous_E_unit = np.zeros(3)
        while True:
            vp.rate(200)

            E_total = np.zeros(3)
            for charge in self.charges:
                E_total += charge.calculate_electric_field(point)
            
            E_unit   = E_total / np.linalg.norm(E_total)
            point   += E_unit # Note: += modifies the original NumPy array in memory!
            ball.pos = vp.vector(*point)

            if np.linalg.norm(E_unit + previous_E_unit) < 0.5 or np.linalg.norm(point - starting_point) > farthest_distance:
                # The direction of the electric field has changed significantly (has done a 180 turn),
                # indicating that the ball/trail has reached the center of a charge!
                break;

            previous_E_unit = E_unit

        return;

def main():
    scene = vp.canvas(
        title = 'Τρισδιάστατες Ηλεκτρικές Δυναμικές Γραμμές',

        width  = 1000,
        height = 500,

        center     = vp.vector(0, 0, 0),
        background = vp.color.white
    )

    scale_factor = 0.5

    q1 = Charge(position = np.array([-100,  0, 0]), charge =  40.0, scale = scale_factor)
    q2 = Charge(position = np.array([ 60, -70, 0]), charge = -20.0, scale = scale_factor)
    q3 = Charge(position = np.array([ 60,  70, 0]), charge = -30.0, scale = scale_factor)

    charges_list  = [q1, q2, q3]
    system        = ChargeSystem(charges = charges_list)
    scene.caption = ' & '.join([str(charge) for charge in charges_list])

    starting_points = []
    for charge in charges_list:
        if charge.charge > 0:
            starting_points.extend(OFFSETS + np.array(charge.position)) # Broadcasting!
    
    for point in starting_points:
        system.draw_electric_field(point)

    return;

if __name__ == '__main__':
    main()
    sleep(20)
