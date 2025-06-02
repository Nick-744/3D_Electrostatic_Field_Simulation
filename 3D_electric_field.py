import vpython as vp
from time import sleep

def cal_e_and_d(xyz_E, xyz_q, q_charge):
	if q_charge > 0:
		x_Eq = xyz_E[0] - xyz_q[0] #x_E - x_q
		y_Eq = xyz_E[1] - xyz_q[1] #y_E - y_q
		z_Eq = xyz_E[2] - xyz_q[2] #z_E - z_q
	elif q_charge < 0:
		x_Eq = xyz_q[0] - xyz_E[0] #x_q - x_E
		y_Eq = xyz_q[1] - xyz_E[1] #y_q - y_E
		z_Eq = xyz_q[2] - xyz_E[2] #z_q - z_E
	d = (x_Eq * x_Eq + y_Eq * y_Eq + z_Eq * z_Eq) ** 0.5
	
	e = (x_Eq / d, y_Eq / d, z_Eq / d)
	
	return (e, d);

def cal_metro_E(q_metro, d):
	k = 8.99e9
	metro_E = (k * q_metro) / (d * d)
	
	return metro_E;

def cal_vector(metro_vector, e):
	vector = (metro_vector * e[0], metro_vector * e[1], metro_vector * e[2])
	
	return vector;

def cal_vector_E(xyz_E, xyz_q, q_charge, q_metro):
	e, d = cal_e_and_d(xyz_E, xyz_q, q_charge)
	metro_E = cal_metro_E(q_metro, d)
	E = cal_vector(metro_E, e)
	
	return E;
	
def add_vectors(v1, v2):
	vector_sum = (v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2])
	
	return vector_sum;

def cal_metro_from_vector(v):
	metro_v = (v[0] * v[0] + v[1] * v[1] + v[2] * v[2]) ** 0.5
	
	return metro_v;

def cal_e_from_vector(vector_v):
	metro_v = cal_metro_from_vector(vector_v)
	e = (vector_v[0] / metro_v, vector_v[1] / metro_v, vector_v[2] / metro_v)
	
	return e;

def cal_d(xyz1, xyz2):
        x = xyz1[0] - xyz2[0]
        y = xyz1[1] - xyz2[1]
        z = xyz1[2] - xyz2[2]
        d = (x * x + y * y + z * z) ** 0.5

        return d;
	
def draw_electric_field2(xyz_E, q1, q2):
        ball = vp.sphere(pos = vp.vector(xyz_E[0], xyz_E[1], xyz_E[2]), color = vp.color.black, radius = 0.1, make_trail = True, retain = 300)
        
        while cal_d(xyz_E, q2[0]) > 1 and cal_d(xyz_E, q1[0]) < 3 * cal_d(q1[0], q2[0]):
                vp.rate(200)
                E1 = cal_vector_E(xyz_E, q1[0], q1[1], q1[2])
                E2 = cal_vector_E(xyz_E, q2[0], q2[1], q2[2])
                E = add_vectors(E1, E2)
                
                e = cal_e_from_vector(E)
                xyz_E = (xyz_E[0] + e[0], xyz_E[1] + e[1], xyz_E[2] + e[2])
                ball.pos = vp.vector(xyz_E[0], xyz_E[1], xyz_E[2])

        return;

def draw_electric_field3(xyz_E, q1, q2, q3):
        ball = vp.sphere(pos = vp.vector(xyz_E[0], xyz_E[1], xyz_E[2]), color = vp.color.black, radius = 0.1, make_trail = True, retain = 300)
        
        while cal_d(xyz_E, q2[0]) > 1 and cal_d(xyz_E, q1[0]) < 3 * cal_d(q1[0], q2[0]) and cal_d(xyz_E, q3[0]) > 1 and cal_d(xyz_E, q1[0]) < 3 * cal_d(q1[0], q3[0]):
                vp.rate(200)
                E1 = cal_vector_E(xyz_E, q1[0], q1[1], q1[2])
                E2 = cal_vector_E(xyz_E, q2[0], q2[1], q2[2])
                E3 = cal_vector_E(xyz_E, q3[0], q3[1], q3[2])
                E = add_vectors(E1, E2)
                E = add_vectors(E, E3)
                
                e = cal_e_from_vector(E)
                xyz_E = (xyz_E[0] + e[0], xyz_E[1] + e[1], xyz_E[2] + e[2])
                ball.pos = vp.vector(xyz_E[0], xyz_E[1], xyz_E[2])

        return;

def draw_q(q):
        if q[1] > 0:
                color = vp.color.red
        else:
                color = vp.color.blue
        q_ball = vp.sphere(pos = vp.vector(q[0][0], q[0][1], q[0][2]), color = color, radius = q[2] / 2)

        return q_ball;

def main():
        scene = vp.canvas(title = 'Τρισδιάστατες Ηλεκτρικές Δυναμικές Γραμμές', width = 1200, height = 720, center = vp.vector(0,0,0), background = vp.color.white)
        
        q1 = ((-100, 0, 0), 1, 40)
        q2 = ((60, -70, 0), -1, 20)
        q3 = ((60, +71, 0), -1, 30)

        #scene.caption= "Θετικό φορτίο {}C (Κόκκινο) | Θέση = {}\nΑρτνητικό φορτίο {}C (Μπλε) | Θέση = {}"format(q1[2], q1[0], q2[2], q2[0])
        scene.caption= "Θετικό φορτίο {}C (Κόκκινο) | Θέση = {}\nΑρτνητικό φορτίο {}C (Μπλε) | Θέση = {}\nΑρτνητικό φορτίο {}C (Μπλε) | Θέση = {}".format(q1[2], q1[0], q2[2], q2[0], q3[2], q3[0])
        q1_ball = draw_q(q1)
        q2_ball = draw_q(q2)
        q3_ball = draw_q(q3)
        
        xyz_E = [(q1[0][0] + 0, +0.1, 0), (q1[0][0] + 0, -0.1, 0),
                 (q1[0][0] + 0.1, +0.1, +0.05), (q1[0][0] + 0.1, -0.1, -0.05),
                 (q1[0][0] + 0, 0, +0.1), (q1[0][0] + 0, 0, -0.1),
                 (q1[0][0] + 0.1, 0, +0.1), (q1[0][0] + 0.1, 0, -0.1),
                 (q1[0][0] + 0.1, +0.1, +0.3), (q1[0][0] + 0.1, -0.1, -0.3),
                 (q1[0][0] + 0.1, +0.1, -0.3), (q1[0][0] + 0.1, -0.1, +0.3),
                 (q1[0][0] + 0.1, +0.1, -0.05), (q1[0][0] + 0.1, -0.1, +0.05),
                 (q1[0][0] + 0, +0.1, +0.1), (q1[0][0] + 0, -0.1, -0.1),
                 (q1[0][0] + 0, +0.1, -0.1), (q1[0][0] + 0, -0.1, +0.1),
                 (q1[0][0] - 0.1, +0.1, +0.2), (q1[0][0] - 0.1, -0.1, -0.2),
                 (q1[0][0] - 0.1, +0.1, -0.2), (q1[0][0] - 0.1, -0.1, +0.2)]
        for xyz in xyz_E:
                draw_electric_field3(xyz, q1, q2, q3)
                                
main()
sleep(10)
