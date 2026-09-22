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

## Rule: everything under BASE_PATH

Fleet apps are served behind a proxy at `BASE_PATH=/direct/<agent>:<port>`, and the prefix
is forwarded **unchanged** — it is NOT stripped before it reaches the app. Every route,
redirect, asset URL and docs URL an app emits has to carry `$BASE_PATH`.

**This repo has no HTTP surface** — it is a training project, not a service, `START_CMD` is empty and nothing listens on
`$PORT` — so the rule is about anything added later, not about the code shipped here.

If you add an HTTP endpoint, read `BASE_PATH` from the environment (normalise it to `''`
or `/leading/no-trailing-slash`) and mount the whole app under it with the framework's own
mechanism: FastAPI — one `APIRouter(prefix=BASE_PATH)` that every other router is included
into, plus `docs_url`/`redoc_url`/`openapi_url` set with the prefix; Flask — `DispatcherMiddleware`
so `url_for()` emits the prefix; Django — `FORCE_SCRIPT_NAME` plus `{% url %}` / `{% static %}`.
Never hard-code a leading-slash path in a template, a redirect or a fetch. Also set `PORT`,
`HEALTH_PATH` (un-prefixed — the fleet prepends `$BASE_PATH`) and `START_CMD` in `fleet.conf`.
