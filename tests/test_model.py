import numpy as np
from lif.model import LIFNeuron


def test_subthreshold_passive_response():
    """Verify numerical Euler integration against the exact exponential analytical solution."""
    tau_m = 10.0
    r_m = 10.0
    v_rest = -70.0

    # Set threshold high (0.0 mV) to prevent spiking and isolate passive RC dynamics
    neuron = LIFNeuron(v_rest=v_rest, v_thresh=0.0, tau_m=tau_m, r_m=r_m)

    # Configure time grid and constant subthreshold input current (0.5 nA)
    dt = 0.05
    t_max = 50.0
    t = np.arange(0, t_max, dt)
    i_inj = np.ones_like(t) * 0.5

    # Run numerical simulation
    v_sim, spikes = neuron.simulate(i_inj, dt)

    # Compute exact analytical solution: V(t) = V_rest + R * I * (1 - exp(-t / tau_m))
    v_analytic = v_rest + r_m * 0.5 * (1 - np.exp(-t / tau_m))

    # Ensure no action potentials were fired
    assert len(spikes) == 0
    # Verify simulation matches analytical curve within tight numerical tolerance
    np.testing.assert_allclose(v_sim, v_analytic, atol=0.01)


def test_rheobase_threshold():
    """Verify that the neuron only fires above the theoretical rheobase current."""
    # Theoretical rheobase: I_rh = (v_thresh - v_rest) / r_m = (-50 - (-70)) / 10 = 2.0 nA
    neuron = LIFNeuron()
    dt, steps = 0.01, 20000  # 200 ms total simulation time

    # Simulate with current slightly below rheobase (1.9 nA) and well above (3.0 nA)
    _, spikes_below = neuron.simulate(np.full(steps, 1.9), dt)
    _, spikes_above = neuron.simulate(np.full(steps, 3.0), dt)

    # Neuron must remain silent below rheobase and fire continuously above it
    assert len(spikes_below) == 0
    assert len(spikes_above) > 0


def test_isi_matches_analytical():
    """Verify simulated Inter-Spike Interval (ISI) against the exact analytical formula."""
    neuron = LIFNeuron()
    dt, steps = 0.01, 40000  # 400 ms total simulation time
    i_const = 3.0  # Constant suprathreshold current (nA)

    # Run simulation and collect spike timestamps
    _, spikes = neuron.simulate(np.full(steps, i_const), dt)
    r_i = neuron.r_m * i_const

    # Exact analytical ISI for LIF neuron without refractory period:
    # T_isi = tau_m * ln((R*I - (V_reset - V_rest)) / (R*I - (V_thresh - V_rest)))
    isi_exact = neuron.tau_m * np.log(
        (r_i - (neuron.v_reset - neuron.v_rest))
        / (r_i - (neuron.v_thresh - neuron.v_rest))
    )

    # Compare mean simulated ISI with analytical value (~9.16 ms)
    mean_isi = np.mean(np.diff(spikes))
    assert abs(mean_isi - isi_exact) < 0.1


if __name__ == "__main__":
    # Run all unit tests sequentially when executed directly as a script
    test_subthreshold_passive_response()
    print("[PASS] Subthreshold passive response (atol=0.01)")

    test_rheobase_threshold()
    print("[PASS] Rheobase threshold verification (1.9 nA vs 3.0 nA)")

    test_isi_matches_analytical()
    print("[PASS] Analytical ISI match (~9.16 ms)")