import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.animation as animation
from main import *

from matplotlib.path import Path
import matplotlib.patches as patches


#Homogeneous point we want to convert
point_3d = np.array([2, 2, -10, 1])

#Coordinates of the view volume
left = -3
right = 3
bottom = -3
top = 3
near = 5
far = 20
nx = 600
ny = 600

#Camera is at the origin of world coordinate system, looking towards -z axis
#Projection Matrix
#Creating camera matrix
rotation_matrix = np.array([[1, 0, 0, 0],
                            [0, 1, 0, 0],
                            [0, 0, 1, 0],
                            [0, 0, 0, 1]])

#To change the z coordinate, top array element 1
translation_matrix = np.array([[1, 0, 0, 0],
                                [0, 1, 0, 0],
                                [0, 0, 1, 0],
                                [0, 0, 0, 1]])

# [x, y, z, ]
cube_vertices = np.array([[4, -1, -18, 1], # Vertex 0 (back bottom left)
                            [2, -1, -18, 1], # Vertex 1 (back bottom right)
                            [2, 1, -18, 1], # Vertex 2 (front bottom right)
                            [4, 1, -18, 1], # Vertex 3 (front bottom left)
                            [4, -1, -12, 1], # Vertex 4 (front top left)
                            [2, -1, -12, 1], # Vertex 5 (front top right)
                            [2, 1, -12, 1], # Vertex 6 (back top right)
                            [4, 1, -12, 1] # Vertex 7 (back top left)
                            ])

#Type of the projection we want
projection_type = "perspective"

def orthographic_projection(left, right, bottom, top, near, far):
    op_matrix = np.array([[2/(right-left), 0, 0, -(right+left) / (right-left)], 
                            [0, 2 / (top-bottom), 0, -(top+bottom) / (top-bottom)],
                            [0, 0, -2 / (far-near), -(far+near) / (far-near)],
                            [0, 0, 0, 1]])
    return op_matrix

def perspective_projection(left, right, bottom, top, near, far):
    pp_matrix = np.array([[(2*near) / (right-left), 0, (right+left) / (right-left), 0],
                            [0, (2*near) / (top-bottom), (top+bottom) / (top-bottom), 0],
                            [0, 0, -(far+near) / (far-near), -(2*far*near) / (far-near)],
                            [0, 0, -1, 0]])
    return pp_matrix

#Choosing projection matrix associated with projection type
if(projection_type == "orthographic"):
    projection_matrix = orthographic_projection(left, right, bottom, top, near, far)
elif (projection_type == "perspective"):
    projection_matrix = perspective_projection(left, right, bottom, top, near, far)

# Translate cube vertices to center at (0, 0, -10)
translation_vector = np.array([0, 0, -10, 0])
cube_vertices = cube_vertices + translation_vector
cube_edges = [[0, 1], [1, 2], [2, 3], [3, 0],
                [4, 5], [5, 6], [6, 7], [7, 4],
                [0, 4], [1, 5], [2, 6], [3, 7]]


# Create a figure
fig = plt.figure(figsize=(15, 6))
ax2d = fig.add_subplot(121)
axUp = fig.add_subplot(122)


# Set labels and title
ax2d.set_xlabel('X')
ax2d.set_ylabel('Y')
ax2d.set_xlim(0, nx)
ax2d.set_ylim(0, ny)
ax2d.set_title('2D Projection on Screen')

axUp.set_xlabel('X')
axUp.set_ylabel('Z')
axUp.set_xlim(0, 10)
axUp.set_ylim(0, 10)
axUp.set_title('Bird-Eye View')

plt.tight_layout()

# Number of frame
numFrames = 20

# Arrays containing results
angles = [None] * numFrames
theta = [None] * numFrames
time_to_contact = [None] * numFrames
clearance_invariant = [None] * numFrames

deritive = [None] * numFrames
actualTTC = [None] * numFrames

# Time between frames (ms)
time = 200

def update(frame):
    ax2d.cla()
    axUp.cla()
    axUp.grid()
    
    ax2d.set_xlim(0, nx)
    ax2d.set_ylim(0, ny)

    center_x = (0 + nx) / 2
    center_y = (0 + ny) / 2
    # Horizon with no rotation
    ax2d.plot([0, nx], [center_y, center_y], label="Horizon", color='black', linewidth=1, linestyle="--")

    axUp.set_xlim(-30, 30)
    axUp.set_ylim(0, -50)

    # Horizontal Top
    axUp.plot( [cube_vertices[2, 0], cube_vertices[3, 0]] , [cube_vertices[2, 2]+frame, cube_vertices[3, 2]+frame], color='red')
    axUp.plot( [cube_vertices[4, 0], cube_vertices[5, 0]] , [cube_vertices[4, 2]+frame, cube_vertices[5, 2]+frame], color='red')

    axUp.plot( [cube_vertices[2, 0], cube_vertices[5, 0]] , [cube_vertices[2, 2]+frame, cube_vertices[5, 2]+frame], color='red')
    axUp.plot( [cube_vertices[4, 0], cube_vertices[3, 0]] , [cube_vertices[4, 2]+frame, cube_vertices[3, 2]+frame], color='red')

    # The line below changes the position of the cube. By multiplying the frame variable, one can increase the speed
    translation_matrix[2, 3] = frame

    camera_matrix = rotation_matrix @ translation_matrix

    #ViewPort Matrix
    viewport_matrix = np.array([[nx/2, 0, 0, (nx-1) / 2],
                                [0, ny/2, 0, (ny-1) / 2],
                                [0, 0, 0.5, 0.5]])

    #Applying the matrices in the described order.
    point_after_CM = camera_matrix @ point_3d
    point_after_PM = projection_matrix @ point_after_CM

    #Normalization of the projected point
    point_after_PM /= point_after_PM[3]
    point_after_VP = viewport_matrix @ point_after_PM

    # Transformed cube vertices after camera and projection matrices
    cube_after_CM = camera_matrix @ cube_vertices.T
    cube_after_PM = projection_matrix @ cube_after_CM
    cube_after_PM /= cube_after_PM[3]
    cube_after_VP = viewport_matrix @ cube_after_PM

    # Find Actual in the Z
    list = []
    actualTTC[frame] = ( -cube_vertices[0,2] - translation_matrix[2, 3] ) / ( 1 / (time / 1000) )

    # Plot the projected cube in 2D
    for edge in cube_edges:
        start_idx, end_idx = edge
        start_point = cube_after_VP[:2, start_idx]
        end_point = cube_after_VP[:2, end_idx]
        list.append([start_point, end_point])
        ax2d.plot([start_point[0], end_point[0]], [start_point[1], end_point[1]], color='red')

    # Colors and hatches the sides of the cube
    front_x_corners = [list[10][0][0], list[10][1][0], list[9][1][0], list[9][0][0]]
    front_y_corners = [list[10][0][1], list[10][1][1], list[9][1][1], list[9][0][1]]
    ax2d.fill(front_x_corners, front_y_corners, color="blue", alpha=0.3)

    back_x_corners = [list[11][0][0], list[11][1][0], list[8][1][0], list[8][0][0]]
    back_y_corners = [list[11][0][1], list[11][1][1], list[8][1][1], list[8][0][1]]
    ax2d.fill(back_x_corners, back_y_corners, color="red", alpha=0.3, hatch="|")

    # Calculate values
    angles[frame] = findAngle(list[10][0], list[10][1], list[9][0], list[9][1])
    theta[frame] = findAngle([center_x,center_y], [center_x,0], list[9][1], [center_x,0])
    if( frame > 0):
        deritive[frame] = (angles[frame] - angles[frame-1] ) / (time/1000)

        if (angles[frame]-angles[frame-1]) < 0.5:
            time_to_contact[frame] = 0
        else:
            time_to_contact[frame] = TTC(angles[frame], angles[frame-1], (time/1000) )

        clearance_invariant[frame] = TTC(theta[frame], theta[frame-1], (time/1000) ) # Time to contact invariant with theta (viewer's angle)
    else:
        time_to_contact[frame] = 0
        deritive[frame] = 0


ani = animation.FuncAnimation(fig=fig, func=update, frames=numFrames, interval=time)
plt.show()

plt.plot( range(numFrames), angles, 'ro')
plt.xlabel("Frame")
plt.ylabel("Angle")
plt.show()

plt.plot( range(numFrames), theta, 'ro')
plt.xlabel("Frame")
plt.ylabel("Theta")
plt.show()

plt.plot( range(numFrames), time_to_contact, 'ro')
plt.xlabel("Frame")
plt.ylabel("Contact in the X-Plane")
plt.show()

plt.plot( range(numFrames), clearance_invariant, 'ro')
plt.xlabel("Frame")
plt.ylabel("Contact in Z-Plane")
plt.show()