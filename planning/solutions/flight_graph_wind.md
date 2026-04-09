We first need to compute the coordinates of the direction vector, i.e. the vector linking two successive waypoints, by using [trigonometric formulas](https://en.wikipedia.org/wiki/Local_tangent_plane_coordinates) in the Earth sphere.

We note:
- $\mathbf{W}$ the wind speed vector
- $\mathbf{V}$ the true aircraft speed vector in the air
- $\mathbf{D}$ the direction vector (obtained with the trigonometric formulas above)
- $\mathbf{U}$ the projected speed of the aircraft on the direction vector
- $\mathbf{u}=\frac{\mathbf{U}}{\Vert \mathbf{U} \Vert} = \frac{\mathbf{D}}{\Vert \mathbf{D} \Vert}$ the unitary direction vector

We known $\mathbf{D}$, $\mathbf{W}$ and $\mathbf{\Vert \mathbf{V} \Vert}$, but we don't known $\mathbf{V}$.

We have: $\mathbf{V} = \mathbf{U} - \mathbf{W}$

Thus: $\Vert \mathbf{V} \Vert^2 = \Vert \mathbf{U} \Vert \; \mathbf{u} \cdot \mathbf{V} - \mathbf{W} \cdot \mathbf{V}$

But also: $\mathbf{V} \cdot \mathbf{u} = \Vert \mathbf{U} \Vert - \mathbf{W} \cdot {u}$

As well as: $\mathbf{V} \cdot \mathbf{W} = \Vert \mathbf{U} \Vert \; \mathbf{u} \cdot \mathbf{W} - \Vert \mathbf{W} \Vert^2$

Therefore: $\Vert \mathbf{U} \Vert^2 - 2 \; \mathbf{u} \cdot \mathbf{W} \; \Vert \mathbf{U} \Vert + \Vert \mathbf{W} \Vert^2 - \Vert \mathbf{V} \Vert^2 = 0$

Finally: $\Vert \mathbf{U} \Vert = \mathbf{W} \cdot \mathbf{u} + \sqrt{(\mathbf{W} \cdot \mathbf{u})^2 + \Vert \mathbf{V} \Vert^2 - \Vert \mathbf{W} \Vert^2}$

Now, if we note $t$ the flying time between the 2 successive waypoints, we can compute the flown distance in the air, i.e. in the direction of $\mathbf{V}$ as: $\Vert \mathbf{V} \Vert \times t = \Vert \mathbf{V} \Vert \times \frac{\Vert \mathbf{D} \Vert}{\Vert \mathbf{U} \Vert} = \frac{\Vert \mathbf{V} \Vert}{\Vert \mathbf{U} \Vert} \Vert \mathbf{D} \Vert$

With headwind, the flown distance will be greater than the direct distance. With tailwind, it is the contrary.