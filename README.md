# Privacy-Preserving Data Aggregation using Paillier Homomorphic Encryption

A Python implementation demonstrating a privacy-preserving secure aggregation protocol. This project uses the **Paillier Cryptosystem** to allow a central aggregator to compute the exact sum of individual private inputs from multiple clients without ever seeing or decrypting the raw data.

## Features

* **Additive Homomorphic Encryption:** Encrypted ciphertexts can be multiplied together to compute the sum of their underlying plaintexts.
* **Data Confidentiality:** The central aggregator has zero access to individual client data, ensuring complete user privacy.
* **Pure Python Implementation:** Built using standard Python libraries (`random`, `math`) without external heavy cryptographic dependencies.

## How It Works

1. **Key Generation:** A public key $(n, g)$ and a private key $(\lambda, \mu)$ are generated.
2. **Client Encryption:** Each participant encrypts their private integer value locally using the public key and a random blinding factor.
3. **Secure Aggregation:** The untrusted aggregator multiplies all received ciphertexts modulo $n^2$. Due to homomorphic properties, this results in an encryption of the total sum.
4. **Decryption:** The authorized entity uses the private key to decrypt the final aggregated ciphertext, revealing only the total sum.

## Project Structure

```text
├── paillier_aggregation.py    # Main script containing key generation, encryption, and simulation
└── README.md                  # Project documentation
