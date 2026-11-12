# Biology Notes: Membrane Potential and the LIF Model

## Basic concepts

**Membrane potential:** The electrical potential difference between the inside and the outside of a neuron. The inside is negative compared to the outside.

**Ion gradients:** Inside the cell the K+ concentration is high, outside the Na+ and Cl- concentrations are high. The Na+/K+ pump uses ATP to keep this difference going all the time.

**Resting potential:** The potential of the neuron when it is not being stimulated. Leak channels (mostly K+ channels) let some ions flow slowly through the membrane. The pump and the leak currents balance each other, and the membrane potential stays at about -70 mV.

**Action potential (spike):** When the input pushes the membrane potential up to the threshold (about -50 mV), voltage-gated Na+ channels open. Na+ flows into the cell and the potential rises quickly (up to about +30 mV). Right after that the Na+ channels inactivate, and voltage-gated K+ channels open. K+ flows out of the cell and pulls the potential back down.

- **Depolarization:** The membrane potential becomes less negative (moves up). Na+ channels open, Na+ enters the cell.
- **Repolarization:** Na+ channels are inactivated, K+ channels are open. K+ leaves the cell and the potential goes back down toward rest.
- **Polarization:** The resting state. No input has arrived yet.
- **Refractory period:** Right after a spike, the neuron cannot fire again (or it is very hard) because the Na+ channels are still inactivated. I will need this later when I add it to the model.

## Modeling the membrane as a circuit (LIF)

- I(t) or I_inj = stimulating (injected) current
- The cell membrane is modeled as a capacitor (C)
- The ion channels (K+, Na+ etc.) are modeled as a resistor (R). In the simple LIF model all the leak channels are lumped into one resistor.
- The injected current splits between the capacitor and the resistor, so:

  I(t) = I_C(t) + I_R(t)

  - I_C = charging current (the current that charges the capacitor)
  - I_R = current flowing through the resistor
  - U_R = voltage across the resistor

Useful relations:

- C = Q / U, so dQ/dt = C * dU/dt = I_C
- U_R = R * I_R
- U = U_rest + U_R, so U - U_rest = R * I_R

Put these into I(t) = I_C(t) + I_R(t):

  I(t) = C * dU/dt + (1/R) * (U - U_rest)

  C * dU/dt = -(1/R) * (U - U_rest) + I(t)

Multiply both sides by R:

  R*C * dU/dt = -(U - U_rest) + R * I(t)

R*C = tau (the membrane time constant).

Now define V = U - U_rest (how far the potential is from rest). Since U_rest is a constant, dV/dt = dU/dt. So:

  **tau * dV/dt = -V + R * I(t)**

This equation helps predict the membrane potential using an equivalent circuit.

## Notes for the code

- With no input (I = 0), V decays back to 0 (the rest) exponentially with time constant tau. That is the "leaky" part.
- With a constant input, V moves toward R*I exponentially.
- This equation alone does not make spikes. For the "integrate-and-fire" part we add a rule: when V reaches the threshold, we record a spike and reset V to a reset value. (Threshold of -50 mV with rest at -70 mV means V_threshold = 20 mV above rest.)

 

## Fire mechanism (integrate-and-fire rule)

The equation tau * dV/dt = -V + R * I(t) alone cannot make a spike, it only
charges the membrane up toward R*I. So in the code I add a rule:

- When V reaches the threshold (-50 mV), I record a spike at that time.
- Then V is reset to V_reset (-65 mV) and the integration continues.

This is a big simplification. In a real neuron the spike shape comes from Na+
and K+ channels opening and closing (about +30 mV peak, then going below rest).
In the LIF model I skip all of this and only keep the timing of the spike.

Also: with threshold at -50 and rest at -70, the neuron only fires if the steady
state R*I is more than 20 mV, which with R = 10 MOhm means I > 2 nA.