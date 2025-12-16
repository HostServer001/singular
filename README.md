# Singular

**Singular** is a high-performance file analysis and deduplication daemon that scans the filesystem, fingerprints files using SHA-256, and maintains a persistent metadata database to detect duplicates efficiently over time.

Support long-running background operation, and allow future extensibility without being constrained by rigid SQL schemas.

---

## Key Features

-  **Duplicate file detection** using SHA-256 hashing  
-  **Performance-oriented design**
  - Metadata reuse across runs
  - Reduced re-hashing for unchanged files
-  **Persistent metadata store** (JSON-based, schema-flexible)
-  **Daemon / service mode** support (systemd)
-  **Rust-accelerated file I/O** for critical paths
-  Modular, extensible architecture

---

## Project Structure
.
├── deamon.sh
├── LICENSE
├── pyproject.toml
├── README.md
├── singular
│   ├── analysis_pulgins
│   ├── analysis.py
│   ├── cli_texts.py
│   ├── config.py
│   ├── data_base
│   │   └── __init__.py
│   ├── data_base_manager.py
│   ├── file_io.rs
│   ├── file.py
│   ├── __init__.py
│   ├── logger.py
│   ├── __main__.py
│   ├── process.py
│   └── utils.py
├── singular_config.json
└── singular.service

---

## How It Works (High Level)

1. **Filesystem Scan**
   - Files are discovered and passed through the processing pipeline.
   - Processing pipeline is optimized to process the discovered non-registerd files in parallel
   - Processing pipeline uses rust to read bytes increasing the speed

2. **Hashing & Metadata Collection**
   - SHA-256 hash is computed.
   - File size, path, and processing time are recorded.

3. **Persistent Storage**
   - Metadata is stored in a JSON-based database.
   - Existing entries are reused to avoid unnecessary disk reads.

4. **Analysis**
   - Files with identical hashes are grouped as duplicates.
   - Missing or deleted files are handled gracefully.

---

[include](CONFIGURATION.md)

---

## Running Singular

### Run Manually
```bash
python -m singular

Run as a Daemon (systemd)

sudo cp singular.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable singular
sudo systemctl start singular


---

Design Philosophy

Avoid SQL when flexibility matters
JSON storage allows evolving metadata without migrations.

Disk I/O is the real bottleneck
The system is optimized to reduce repeated reads and writes.

Composable internals
Each component (scanner, database, analyzer) can evolve independently.

Future-proof
Rust is used selectively where Python overhead becomes significant.



---

Current Status

Early but functional

Actively evolving

Performance characteristics already measurable and improving



---

Roadmap

Batched database writes

Incremental filesystem monitoring (watchdog/inotify)

Configurable hash algorithms

Rich CLI output & reporting

Optional SQLite / alternative backends



---

License

Licensed under the terms specified in the LICENSE file.


---

Author Notes

Singular is built as a systems-level learning project with real-world constraints in mind: performance, correctness, and long-running reliability.

Contributions, reviews, and architectural discussions are welcome.

---

If you want, I can also:
- Tighten this into a **Debian-quality README**
- Add a **DESIGN.md** explaining internals
- Write a **man page**
- Rewrite it in a **more minimal / hacker-style README**

Just say the word.