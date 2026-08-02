# Awesome PQC [![Follow @AppliedPQC on X](https://img.shields.io/badge/X-%40AppliedPQC-000000?logo=x&logoColor=white)](https://x.com/AppliedPQC)

> A curated, **link-verified** list of post-quantum cryptography resources for
> people who have to *build* and *ship* it.

Every entry below was checked on **2026-07-31**: each GitHub project resolved
through the API and was confirmed not archived; every other link returned
HTTP 200. Entries that could not be verified were removed rather than shipped
as decoration. See [Verification](#verification) for the method, what it
caught, and where it falls short.

## Why this list

[`veorq/awesome-post-quantum`](https://github.com/veorq/awesome-post-quantum) is
the canonical general PQC list and is actively maintained — **start there** for
breadth, papers, and policy. This list is deliberately narrower and focuses on
three things: **implementation** (code, test vectors, conformance),
**industry deployment** (what is actually shipping in TLS, SSH, browsers, and
hardware), and **migration** (inventory, hybrid rollout, and timelines).

## Contents

- [Standards](#standards)
- [Test vectors and conformance](#test-vectors-and-conformance)
- [Reference implementations](#reference-implementations)
- [Libraries](#libraries)
- [Protocol integration and deployment](#protocol-integration-and-deployment)
- [Blockchain and consensus](#blockchain-and-consensus)
- [Learning](#learning)
- [Other curated lists](#other-curated-lists)
- [Verification](#verification)
- [Contributing](#contributing)

## Standards

### NIST

- [Post-Quantum Cryptography project](https://csrc.nist.gov/Projects/post-quantum-cryptography) — the authoritative status page for the whole programme.
- [FIPS 203: ML-KEM](https://csrc.nist.gov/pubs/fips/203/final) ([PDF](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)) — module-lattice KEM, from CRYSTALS-Kyber. Final, August 2024.
- [FIPS 204: ML-DSA](https://csrc.nist.gov/pubs/fips/204/final) ([PDF](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)) — module-lattice signatures, from CRYSTALS-Dilithium. Final, August 2024.
- [FIPS 205: SLH-DSA](https://csrc.nist.gov/pubs/fips/205/final) ([PDF](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf)) — stateless hash-based signatures, from SPHINCS+. Final, August 2024.
- **FIPS 206: FN-DSA** (Falcon) — **not yet published.** NIST lists it as *in development*; as of 2026-07-31 there is no initial public draft and no ACVP vectors. Until it appears, the [round-3 Falcon submission](https://falcon-sign.info/) is the authoritative specification. Several lists describe FIPS 206 as a released draft; it is not.
- [SP 800-208: Stateful Hash-Based Signatures](https://csrc.nist.gov/pubs/sp/800/208/final) — approves LMS and XMSS for narrow use (firmware signing). Stateful: key reuse is catastrophic.
- [Additional Digital Signature Schemes](https://csrc.nist.gov/projects/pqc-dig-sig) — the signature "on-ramp", seeking non-lattice diversity.

### IETF

- [PQUIP working group](https://datatracker.ietf.org/wg/pquip/about/) — post-quantum use in protocols.
- [`ietf-wg-pquip/state-of-protocols-and-pqc`](https://github.com/ietf-wg-pquip/state-of-protocols-and-pqc) — a map of which IETF protocols have PQC stories. Useful, but last updated June 2025, so check dates against the drafts themselves.
- [RFC 9881](https://www.rfc-editor.org/rfc/rfc9881.html) — X.509 algorithm identifiers for **ML-DSA** (October 2025).
- [RFC 9935](https://www.rfc-editor.org/rfc/rfc9935.html) — X.509 algorithm identifiers for **ML-KEM** (March 2026).
- [RFC 8554](https://www.rfc-editor.org/rfc/rfc8554.html) — LMS hash-based signatures.
- [RFC 8391](https://www.rfc-editor.org/rfc/rfc8391.html) — XMSS, eXtended Merkle Signature Scheme.
- [draft-ietf-tls-ecdhe-mlkem](https://datatracker.ietf.org/doc/draft-ietf-tls-ecdhe-mlkem/) — the hybrid TLS 1.3 groups actually deployed today (X25519MLKEM768 and friends).
- [draft-ietf-tls-mlkem](https://datatracker.ietf.org/doc/draft-ietf-tls-mlkem/) — standalone ML-KEM in the TLS 1.3 key schedule.

### National and regional guidance

- [BSI (Germany) — quantum technologies and PQC](https://www.bsi.bund.de/EN/Themen/Unternehmen-und-Organisationen/Informationen-und-Empfehlungen/Quantentechnologien-und-Post-Quanten-Kryptografie/quantentechnologien-und-post-quanten-kryptografie_node.html) — recommendations that differ from NIST in useful ways, notably on hybrid modes.
- **NSA CNSA 2.0**, **CISA Quantum Readiness**, and **NIST NCCoE migration** guidance are primary migration sources, but `nsa.gov`, `cisa.gov` and `nccoe.nist.gov` return HTTP 403 to automated clients, so their URLs are not listed here as verified links. Reach them from the [NIST PQC project page](https://csrc.nist.gov/Projects/post-quantum-cryptography) or [veorq's list](https://github.com/veorq/awesome-post-quantum#migration-guidelines).

## Test vectors and conformance

The part most implementers underestimate. An implementation is not correct because it round-trips with itself.

- [`usnistgov/ACVP-Server`](https://github.com/usnistgov/ACVP-Server) — NIST's ACVP vectors. The `gen-val/json-files/` tree holds `internalProjection.json` files carrying **both inputs and expected outputs** for `ML-KEM-keyGen-FIPS203`, `ML-KEM-encapDecap-FIPS203`, `ML-DSA-{keyGen,sigGen,sigVer}-FIPS204` and `SLH-DSA-{keyGen,sigGen,sigVer}-FIPS205`. This is the ground truth for byte-exact conformance.
- [Falcon round-3 KATs](https://falcon-sign.info/) — the submission package ships `KAT/falcon{512,1024}-KAT.rsp`. Since FIPS 206 has no vectors, these are the only known-answer tests for FN-DSA.
- [`mupq/pqm4`](https://github.com/mupq/pqm4) — PQC on Cortex-M4, with testing and benchmarking harnesses.

## Reference implementations

- [`pq-crystals/kyber`](https://github.com/pq-crystals/kyber) — reference and optimised ML-KEM ([site](https://pq-crystals.org/kyber/)).
- [`pq-crystals/dilithium`](https://github.com/pq-crystals/dilithium) — reference and optimised ML-DSA ([site](https://pq-crystals.org/dilithium/)).
- [`sphincs/sphincsplus`](https://github.com/sphincs/sphincsplus) — reference SLH-DSA ([site](https://sphincs.org/)).
- [Falcon](https://falcon-sign.info/) — reference FN-DSA, including the floating-point Gaussian sampler that makes constant-time implementation hard.
- [HQC](https://pqc-hqc.org/) — code-based KEM, selected March 2025 as a backup to ML-KEM with different hardness assumptions.
- [`PQClean/PQClean`](https://github.com/PQClean/PQClean) — clean, portable, test-covered C implementations intended for integration into other libraries.

## Libraries

### Multi-algorithm

- [`open-quantum-safe/liboqs`](https://github.com/open-quantum-safe/liboqs) — the broadest C library ([project](https://openquantumsafe.org/)). Bindings: [Python](https://github.com/open-quantum-safe/liboqs-python), [Rust](https://github.com/open-quantum-safe/liboqs-rust), [Go](https://github.com/open-quantum-safe/liboqs-go).
- [`open-quantum-safe/oqs-provider`](https://github.com/open-quantum-safe/oqs-provider) — OpenSSL 3 provider exposing PQC and hybrid algorithms to anything that speaks OpenSSL.

### General-purpose crypto libraries with PQC

- [`openssl/openssl`](https://github.com/openssl/openssl) — native ML-KEM, ML-DSA and SLH-DSA since [3.5](https://openssl-library.org/post/2025-04-08-openssl-35-final-release/).
- [`aws/aws-lc`](https://github.com/aws/aws-lc) — AWS's BoringSSL fork, FIPS-validated branches.
- [`google/boringssl`](https://github.com/google/boringssl) — where Chrome's ML-KEM lives.
- [`bcgit/bc-java`](https://github.com/bcgit/bc-java) — Bouncy Castle, the most complete JVM PQC support.
- [`randombit/botan`](https://github.com/randombit/botan) — C++ with broad PQC coverage.
- [`wolfSSL/wolfssl`](https://github.com/wolfSSL/wolfssl) — embedded-oriented TLS with PQC.

### Rust and Go

- [`RustCrypto/KEMs`](https://github.com/RustCrypto/KEMs) — pure-Rust ML-KEM.
- [`RustCrypto/signatures`](https://github.com/RustCrypto/signatures) — pure-Rust ML-DSA and SLH-DSA.
- [`rustpq/pqcrypto`](https://github.com/rustpq/pqcrypto) — Rust bindings over PQClean.
- [`cloudflare/circl`](https://github.com/cloudflare/circl) — Go PQC and hybrid primitives, used in production at Cloudflare.

## Protocol integration and deployment

- [Signal PQXDH](https://signal.org/blog/pqxdh/) — X25519 + ML-KEM-1024 for initial key agreement; the first large-scale PQC messaging deployment.
- [OpenSSH](https://www.openssh.com/releasenotes.html) — `mlkem768x25519-sha256` is the default key exchange from OpenSSH 10.0; `sntrup761x25519-sha512` has shipped since 9.0.
- [`open-quantum-safe/openssh`](https://github.com/open-quantum-safe/openssh) — experimental OQS-enabled OpenSSH for algorithms not upstream.
- [`aws/s2n-tls`](https://github.com/aws/s2n-tls) — TLS implementation with hybrid PQC key exchange.
- [Cloudflare PQC reports](https://blog.cloudflare.com/pq-2025/) — the best public measurements of real-world PQC adoption; see also [the 2024 edition](https://blog.cloudflare.com/pq-2024/).

## Blockchain and consensus

Chains hit PQC problems the web does not, and — importantly — not the *same*
problem as each other. Bitcoin's is public-key exposure on an immutable ledger
under rough-consensus governance; Ethereum's is signature size at validator
scale, which is why its flagship artifact is a zkVM rather than a signature
library; Cosmos's is key-type negotiation across interoperable chains. Progress
inverts exposure: the chain with the sharpest exposure has specified no PQ
signature scheme, and the least-discussed of the three has one in shipped code.

**Ethereum.** Hash-based signatures rest on the most conservative assumption
available, but at roughly 3 KB each they cannot go on chain one per validator,
so most of the work is *aggregation*.

- [Post-Quantum Ethereum](https://pq.ethereum.org/) — the hub for Ethereum's post-quantum effort, and the fastest way to see current status.
- [Ethereum quantum-resistance roadmap](https://ethereum.org/roadmap/future-proofing/quantum-resistance/) — why the consensus layer is changing, in protocol terms.
- [`leanEthereum/leanVM`](https://github.com/leanEthereum/leanVM) — "minimal hash-based zkVM, for a Post-Quantum Ethereum", built for recursive aggregation of post-quantum signatures. This is the piece that makes hash-based signatures affordable at validator scale.
- [`leanEthereum/leanSig`](https://github.com/leanEthereum/leanSig) — Rust prototype of the proposed signature scheme, built on tweakable hash functions and incomparable encodings. Explicitly unaudited and not for production.
- [`b-wagn/hash-sig`](https://github.com/b-wagn/hash-sig) — the upstream research implementation leanSig grew out of, with the accompanying paper ([eprint 2025/055](https://eprint.iacr.org/2025/055)).

**Bitcoin.** Two Draft BIPs, neither activated. Note that BIP-360 does *not*
introduce a post-quantum signature scheme — it removes Taproot's key-path spend
so no bare public key is exposed — and BIP-361 formally `Requires: TBD Post
Quantum Signature BIP`, a document that does not yet exist.

- [BIP-360, Pay-to-Merkle-Root (P2MR)](https://github.com/bitcoin/bips/blob/master/bip-0360.mediawiki) — soft-fork output type defending against long-exposure attacks. Explicitly not short-exposure, and explicitly not a signature scheme.
- [BIP-361, Post Quantum Migration and Legacy Signature Sunset](https://github.com/bitcoin/bips/blob/master/bip-0361.mediawiki) — phased sunset of legacy ECDSA/Schnorr. States that as of 1 March 2026 over 34% of all bitcoin have revealed a public key on chain.
- [Bitcoin Optech: quantum resistance](https://bitcoinops.org/en/topics/quantum-resistance/) — the least breathless running summary of where the debate stands.

**Cosmos.** The one place a NIST scheme is already in shipped consensus code,
rather than in a proposal.

- [Cosmos SDK `UPGRADING.md`](https://github.com/cosmos/cosmos-sdk/blob/main/UPGRADING.md) — v0.55 registers ML-DSA-65 (FIPS 204) as a validator consensus key type ([PR #26436](https://github.com/cosmos/cosmos-sdk/pull/26436)), opt-in behind a genesis parameter. Read the IBC warning: light clients verify commit signatures with the *counterparty's* compiled-in crypto, so enabling a new key type before counterparties can verify it stops packet flow and eventually expires the client.
- [Post-quantum keys](https://docs.cosmos.network/sdk/latest/keys/post-quantum-keys) and [Migrate a validator to ML-DSA](https://docs.cosmos.network/sdk/latest/keys/migrate-validator-ml-dsa) — the operator guides.


## Learning

- **[Applied Post-Quantum Cryptography](https://appliedpqc.io/)** ([PDF](https://appliedpqc.io/apqc.pdf), [source](https://github.com/AppliedPQC/AppliedPQC)) — a book building PQC from first principles to deployment, with worked SageMath throughout.
  - Complete, byte-exact SageMath implementations, each covering **every numbered algorithm** of its standard and verified against the NIST ACVP vectors:
    [`fips203_mlkem.sage`](https://github.com/AppliedPQC/AppliedPQC/blob/main/sage/fips203_mlkem.sage) (21/21 algorithms) ·
    [`fips204_mldsa.sage`](https://github.com/AppliedPQC/AppliedPQC/blob/main/sage/fips204_mldsa.sage) (49/49) ·
    [`fips205_slhdsa.sage`](https://github.com/AppliedPQC/AppliedPQC/blob/main/sage/fips205_slhdsa.sage) (25/25, all 12 parameter sets) ·
    [`fips206_fndsa.sage`](https://github.com/AppliedPQC/AppliedPQC/blob/main/sage/fips206_fndsa.sage) (18/18, tracking the Falcon submission)
  - [`test_kat.sage`](https://github.com/AppliedPQC/AppliedPQC/blob/main/sage/test_kat.sage) — the known-answer test runner, and [`fetch_vectors.sh`](https://github.com/AppliedPQC/AppliedPQC/blob/main/sage/fetch_vectors.sh) to download the vectors. [Notes on the approach](https://github.com/AppliedPQC/AppliedPQC/blob/main/sage/README.md).
- [PQCrypto conference](https://pqcrypto.org/) — the field's main venue; the site also hosts a long-running bibliography.
- [Open Quantum Safe](https://openquantumsafe.org/) — project documentation, and a good map of what is implementable today.

## Other curated lists

Credit where due, and useful when this list is too narrow:

- [`veorq/awesome-post-quantum`](https://github.com/veorq/awesome-post-quantum) — the canonical general list. Broadest coverage of standards, papers and policy.
- [`bro256/Awesome-PQC-Resources`](https://github.com/bro256/Awesome-PQC-Resources) — strong on books, talks and migration guides.
- [`QuantumVillage/awesome-quantum-security`](https://github.com/QuantumVillage/awesome-quantum-security) — wider quantum-and-security scope.
- [`qosf/awesome-quantum-software`](https://github.com/qosf/awesome-quantum-software) — quantum *computing* software, the adjacent field.

## Verification

Awesome lists rot. This one records how and when it was checked so you can judge how much to trust it.

**Method (2026-07-31).** GitHub projects were resolved through the GitHub API, confirming the repository exists and is not archived, and recording its last-push date; renames and transfers were followed to their current canonical names. Non-GitHub links were fetched and required HTTP 200 after redirects. For standards documents, the claim was checked against the document itself, not against a search summary.

**Currency.** All but one GitHub entry had commits within the last five months, most within days. The exception is `ietf-wg-pquip/state-of-protocols-and-pqc`, last updated June 2025, which is flagged inline above rather than quietly listed alongside actively maintained projects.

**What that caught.** Two entries were dropped for not existing at all. Two candidate lists turned out to be the same repository under a former name, and another had been transferred to a different owner. Most importantly, a widely repeated summary had RFC 9881 and RFC 9935 assigned to the wrong algorithms; reading the RFCs shows 9881 is ML-DSA and 9935 is ML-KEM.

**Limits.** `nsa.gov`, `cisa.gov` and `nccoe.nist.gov` return HTTP 403 to automated clients, so their guidance is described but not linked as verified. HTTP 200 proves a URL resolves, not that its content is still accurate. Star counts and commit dates are deliberately not recorded per entry, because they are stale the day after they are written.

The larger limit is coverage, not liveness. The first edition of this list was
searched along five axes — existing lists, standards bodies, implementations,
protocol deployment, and learning material — and had no axis for consensus-layer
work, so it missed Ethereum's post-quantum effort entirely despite that being
one of the largest PQC deployments underway. Link checking cannot find a section
that was never written. If a whole area is missing, please open an issue.

## Contributing

PRs welcome. Please keep entries alphabetical within a section, write one line on *why* an entry earns its place rather than restating its tagline, and check your link before submitting. Entries that are unmaintained or superseded are removed, not annotated.

## License

[CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/) — to the extent possible under law, contributors have waived all copyright and related rights to this work.
