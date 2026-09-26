# PyTorch template

Provisioned from [`Qode-Platform/fleet-template-v1`](https://github.com/Qode-Platform/fleet-template-v1) — the fleet
lifecycle contract (`bin/`, `fleet.conf`, deploy workflows) with a
PyTorch starter laid on top.

## Origin

    hand-written (library, no generator) — model/data/train split

Generated 2026-09-21 on Node v22.12.0 / Python 3.12.3. **Dependencies were
never installed and this has never been built or run.** Boot it once before
trusting it.

## Fleet lifecycle

`fleet.conf` drives every script in `bin/`:

| step | command |
|---|---|
| install | `python3 -m venv .venv && .venv/bin/pip install --upgrade pip -r requirements.txt` |
| build | `(none)` |
| start | `(none — not a service)` |

    ./bin/run       # install, build, start in the foreground
    ./bin/start     # start from existing build artifacts
    ./bin/restart   # rebuild and restart
    ./bin/stop      # stop whatever holds the port

**This repo is not a service.** `START_CMD` is empty, so `./bin/run` will
install and then stop at the start step with the template's own error. That
is intentional — there is nothing to listen on `$PORT`.

## What differs from stock output

- NOT A SERVICE: START_CMD is empty by design; bin/run will stop at the start step.
- Train with: .venv/bin/python -m src.train --config configs/default.yaml

---

# PyTorch scaffold

Hand-written — PyTorch is a library, not a framework, and ships no generator.
This is the conventional research-project split: model / data / train, with
run settings in YAML instead of argparse sprawl.

    python -m venv .venv && . .venv/bin/activate
    pip install -r requirements.txt
    python -m src.train --config configs/default.yaml
    pytest            # shape + gradient tests, no dataset download

Downloads MNIST to `./data` on first train run. Checkpoints land in
`./checkpoints`, one per epoch.

## Serving over HTTP

Fleet apps are served at the root of their own hostname
(`https://<hash>.<FLEET_APP_DOMAIN>/`), so every route, redirect and asset URL is a plain
root path.

**This repo has no HTTP surface** — it is a training project, not a service, `START_CMD` is empty and nothing listens on
`$PORT`.

If you add an HTTP endpoint, listen on `$PORT` (the fleet injects it, along with
`DATABASE_URL`) and serve at `/`. Also set `PORT`, `HEALTH_PATH` and `START_CMD` in
`fleet.conf`.
