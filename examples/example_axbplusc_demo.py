"""
Example 3: Complete ASIC computing a*b+c (64-bit)
Demonstrates multi-stage pipeline with inter-module communication.
"""

from assassyn.frontend import *
from assassyn.backend import elaborate
from assassyn import utils


class PlusC(Module):
    """Stage 2: Adds the product (a*b) with c"""
    def __init__(self):
        super().__init__(
            ports={
                'a': Port(Int(32)),
                'b': Port(Int(32)),
                'c': Port(Int(64)),
                'axb': Port(Int(64)),  # Product from multiplier
            }
        )

    @module.combinational
    def build(self, result_reg: Array):
        a, b, c, axb = self.pop_all_ports(True)
        result_reg[0] = axb + c  # Final result: a*b + c
        log("Result: {} * {} + {} = {}", a, b, c, result_reg[0])


class Driver(Module):
    """Stage 1: Driver that provides inputs and computes a*b"""
    def __init__(self):
        super().__init__(ports={})

    @module.combinational
    def build(self, plusc: PlusC):
        cnt = RegArray(Int(32), 1)
        (cnt & self)[0] <= cnt[0] + Int(32)(1)

        # Test with different values each cycle
        input_a = cnt[0] + Int(32)(1)  # a = cnt + 1
        input_b = cnt[0] + Int(32)(2)  # b = cnt + 2
        input_c = cnt[0].sext(64) + Int(64)(10)  # c = cnt + 10

        # Compute a*b (sign-extend to 64-bit first)
        axb = input_a.sext(64) * input_b.sext(64)

        # Only run for 10 cycles
        cond = cnt[0] < Int(32)(10)
        with Condition(cond):
            plusc.async_called(
                a=input_a,
                b=input_b,
                c=input_c,
                axb=axb
            )


def test_axbplusc():
    """Build and run the a*b+c ASIC"""
    print("=" * 60)
    print("Example 3: ASIC computing a*b+c")
    print("=" * 60)

    # Build the system
    sys = SysBuilder('axbplusc_demo')
    with sys:
        result = RegArray(Int(64), 1)

        plusc = PlusC()
        plusc.build(result)

        driver = Driver()
        driver.build(plusc)

    print("\n[System Structure]")
    print(sys)

    # Generate simulator
    print("\n[Generating Simulator...]")
    simulator_path, verilator_path = elaborate(sys, verilog=utils.has_verilator())
    print(f"Simulator path: {simulator_path}")

    # Run simulation
    print("\n[Running Simulation...]")
    raw = utils.run_simulator(simulator_path)

    # Display results
    print("\n[Simulation Output]")
    print("-" * 60)
    for line in raw.split('\n'):
        if 'Result:' in line:
            print(line.strip())
    print("-" * 60)

    # Verify results
    print("\n[Verification]")
    errors = 0
    for line in raw.split('\n'):
        if 'Result:' in line:
            tokens = line.split()
            # Parse: "Result: a * b + c = result"
            a = int(tokens[-7])
            b = int(tokens[-5])
            c = int(tokens[-3])
            result = int(tokens[-1])
            expected = a * b + c
            if result != expected:
                print(f"ERROR: {a} * {b} + {c} = {result}, expected {expected}")
                errors += 1

    if errors == 0:
        print("✅ All calculations verified correct!")
    else:
        print(f"❌ Found {errors} errors")

    # Run Verilator if available
    if verilator_path:
        print("\n[Running Verilator Verification...]")
        raw_verilog = utils.run_verilator(verilator_path)
        print("Verilator output:")
        for line in raw_verilog.split('\n'):
            if 'Result:' in line:
                print(line.strip())
        print("✅ Verilator simulation completed!")

    return raw


if __name__ == '__main__':
    test_axbplusc()
