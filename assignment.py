import random
import math

# --- Helper Functions ---

def gcd(a, b):
    return math.gcd(a, b)

def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)

def is_prime(n, k=5):
    """Miller-Rabin primality test for demonstration."""
    if n < 2:
        return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]:
        if n % p == 0:
            return n == p
    s, d = 0, n - 1
    while d % 2 == 0:
        s += 1
        d //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits=512):
    """Generates a random prime number of specified bits."""
    while True:
        p = random.getrandbits(bits)
        # Ensure it has the correct bit length and is odd
        p |= (1 << bits - 1) | 1
        if is_prime(p):
            return p


# --- Paillier Cryptosystem Implementation ---

class Paillier:
    def __init__(self, bits=256):
        # Using smaller bits (256-bit primes -> 512-bit n) for fast demo execution
        print("Generating keys (this may take a few seconds)...")
        p = generate_prime(bits)
        q = generate_prime(bits)
        while p == q:
            q = generate_prime(bits)

        self.n = p * q
        self.n_sq = self.n * self.n
        self.lmbda = lcm(p - 1, q - 1)

        # Choose g = n + 1, which is a standard and efficient choice for Paillier
        self.g = self.n + 1

        # Compute mu = (L(g^lmbda mod n^2))^(-1) mod n
        # L(x) = (x - 1) / n
        u = pow(self.g, self.lmbda, self.n_sq)
        L = (u - 1) // self.n
        self.mu = pow(L, -1, self.n)
        print("Key generation complete!\n")

    def encrypt(self, m):
        """Encrypts a plaintext integer m using public key (n, g)."""
        r = random.randrange(1, self.n)
        # c = g^m * r^n mod n^2
        term1 = pow(self.g, m, self.n_sq)
        term2 = pow(r, self.n, self.n_sq)
        c = (term1 * term2) % self.n_sq
        return c

    def decrypt(self, c):
        """Decrypts a ciphertext c using private key (lmbda, mu)."""
        u = pow(c, self.lmbda, self.n_sq)
        L = (u - 1) // self.n
        m = (L * self.mu) % self.n
        return m


# --- Secure Aggregation Simulation ---

if __name__ == "__main__":
    # 1. Initialize Paillier cryptosystem (trusted authority / key generator)
    paillier = Paillier(bits=256)

    # 2. Simulate individual client data (e.g., private measurements or salaries)
    client_data = [1500, 2300, 4100, 850, 3200]
    print(f"Original Client Inputs (Private): {client_data}")
    print(f"Actual True Sum: {sum(client_data)}\n")

    # 3. Client-Side Encryption
    print("Clients encrypting their data...")
    ciphertexts = []
    for i, m in enumerate(client_data):
        c = paillier.encrypt(m)
        ciphertexts.append(c)
        print(f"  Client {i+1}: input {m} -> ciphertext {str(c)[:25]}...")

    # 4. Aggregator-Side Computation (Homomorphic Addition)
    # The aggregator has NO private key, only ciphertexts.
    print("\nCentral Aggregator performing secure aggregation (multiplying ciphertexts)...")
    aggregated_ciphertext = 1
    for c in ciphertexts:
        aggregated_ciphertext = (aggregated_ciphertext * c) % paillier.n_sq

    print(f"Aggregated Ciphertext: {str(aggregated_ciphertext)[:25]}...")

    # 5. Decryption of the Final Aggregate
    print("\nDecrypting the aggregated result...")
    recovered_sum = paillier.decrypt(aggregated_ciphertext)

    print(f"Successfully Recovered Sum: {recovered_sum}")