# Concurrent Programming Examples

This repository contains examples and exercises related to concurrent programming in Python, including threading, multiprocessing, and pipeline-based data processing.

## Structure

- `lesssons/`
  - `async/` — Async programming examples.
  - `multiprocessing/` — Multiprocessing examples:
    - `main_partial.py` — Using `functools.partial` with multiprocessing pools.
    - `main_varying.py` — Passing varying arguments to multiprocessing pools.
  - `threading/`
    - `01_threading_vs_multiprocess/` — Comparison of threading and multiprocessing for CPU and IO-bound tasks.
    - `02_worker/`, `03_locks/` — Additional threading examples.
- `threading/`
  - `main.py` — Runs a configurable pipeline using YAML and worker threads.
  - `main_simple.py` — Simple pipeline using multiprocessing workers.
  - `yaml_reader.py` — Loads and executes pipelines defined in YAML.
  - `pipelines/`
    - `main.py`, `wiki_yahoo_db_pipe.yaml` — Pipeline configuration and logic.
  - `utils/`
    - `db.py`, `wiki.py`, `yahoo.py` — Utility modules for database, Wikipedia, and Yahoo Finance data.
  - `worker/` — Worker implementation.
  - `init_db.sh` — Script to initialize the local database.
  - `.env-local` — Example environment variable file.
  - `local.db` — Local SQLite database.

## Requirements

- Python 3.12+
- See [requirements.txt](requirements.txt) for dependencies.

Install dependencies:

```sh
pip install -r requirements.txt
```

## Usage

### Threading vs Multiprocessing Example

Run the comparison script:

```sh
python lesssons/threading/01_threading_vs_multiprocess/main.py
```

### Pipeline Example (using threading)

1. Initialize the database:

    ```sh
    cd pipeline_runner
    ./init_db.sh
    ```

2. Set environment variables:

    ```sh
    source .env-local
    ```

3. Run the pipeline:

    ```sh
    python pipeline_runner/main.py
    ```

## Notes

- The pipeline is configured via YAML files in `pipeline_runner/pipelines/`.
- Worker logic is modular and can be extended via the `utils/` and `worker/` directories.

## License

This project is for educational purposes.
