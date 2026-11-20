# news-image-20261120 — THE WORLD TODAY

[![make.fun](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/lycann666/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/lycann666/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120)

Entry for the [make.fun bounty "Sum up 20 November's world news in one image"](https://make.fun/bounty/news-image-20261120).

## What it is

`main.py` draws a one-page newspaper front page — **THE WORLD TODAY**,
Friday 20 November 2026 — entirely procedurally: a hand-written 5x7 bitmap
font, a pure-stdlib PNG encoder, and drawing code for the masthead, the three
flags of the United States, China and Russia, a cyclone spiral and a globe.
No images, fonts or data are read from disk and no network is used at
runtime, so the output is byte-identical on every run.

## The news on the page

- **Trump, Xi and Putin sign a historic peace declaration** after the
  first-ever trilateral meeting in China
- **Myanmar guilty of genocide**, the UN's top court rules
- **Trump: no rush on Iran** — decision pushed to 2027
- **Cyclone Akvan** hits India's east coast; 300,000 evacuated in Odisha
- **Voyager 1** reaches one light-day from Earth
- **Anthropic up 17%** on its market debut
- **Europe ready for Russia talks** on ending the war in Ukraine
- Also: World Children's Day, a record $190.4M Van Gogh sale, GTA 6 sales
  past $1.8 billion, Nicholls 113\* for New Zealand

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# writes out/entry.png — 1024x1024 PNG, under 1 MiB, deterministic
```

Python 3.13, standard library only.

## License

MIT — see [LICENSE](LICENSE).
