from crypto.attack import Attack

attacker = Attack()

print "Running benchmark..."

attacker.benchmark('brute', algorithm='otp', min=1, max=8, key="howdy")

print "Benchmark complete."