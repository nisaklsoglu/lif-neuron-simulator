import numpy as np

class LIFNeuron:
    def __init__(self, v_rest=-70.0, v_reset=-65.0, v_thresh=-50.0, tau_m=10.0, r_m=10.0):
        self.v_rest = v_rest    # Resting membrane potential (mV)
        self.v_reset = v_reset  # Reset potential after a spike (mV)
        self.v_thresh = v_thresh  # Firing threshold (mV)
        self.tau_m = tau_m      # Membrane time constant (ms)
        self.r_m = r_m          # Membrane resistance (MOhm)

    def simulate(self, i_inj, dt, v_init=None):
        """
        Simulates the Leaky Integrate-and-Fire (LIF) neuron model using the Euler method.
        
        Parameters:
        - i_inj: 1D numpy array of injected input current (nA)
        - dt: Time step size (ms)
        - v_init: Initial membrane potential (mV)
        
        Returns:
        - v: Membrane potential time series (numpy array)
        - spikes: Array of spike timestamps (ms)
        """

        steps = len(i_inj)
        v = np.zeros(steps)
        v[0] = self.v_rest if v_init is None else v_init
        spikes = []

        for t in range(steps - 1):
            if v[t] >= self.v_thresh:
                # Threshold reached so record spike and reset voltage
                v[t] = self.v_thresh  # Hold at threshold for visual plotting
                v[t+1] = self.v_reset
                spikes.append(t * dt)  # Record the time spike occured
            else:
                # Euler integration: tau_m * dV/dt = -(V - V_rest) + R * I
                dv = (-(v[t] - self.v_rest) + self.r_m * i_inj[t]) / self.tau_m
                v[t+1] = v[t] + dv * dt

        return v, np.array(spikes)