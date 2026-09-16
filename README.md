# youtube-automation-daily-cartoons

Automated YouTube channel workflow for daily cartoon content (one long video + one short).

## What runs daily

The workflow in `/home/runner/work/youtube-automation-daily-cartoons/youtube-automation-daily-cartoons/.github/workflows/main.yml` runs:

- Daily at `16:00 UTC` via cron
- On manual trigger via **Run workflow** (`workflow_dispatch`)

Pipeline steps:
1. Generate a topic (`scripts/generate_topic.py`)
2. Generate a script (`scripts/generate_script.py`)
3. Render long and short videos with `ffmpeg`
4. Upload build artifacts
5. Upload to YouTube when `publish=true`

## Required GitHub secrets (for upload)

Set these repository secrets in **Settings → Secrets and variables → Actions**:

- `YT_CLIENT_ID`
- `YT_CLIENT_SECRET`
- `YT_REFRESH_TOKEN`

If `publish=true` and any secret is missing, the workflow fails with a clear error.

> Do **not** commit OAuth credentials or token files to the repository.

## Local validation

From repository root (`/home/runner/work/youtube-automation-daily-cartoons/youtube-automation-daily-cartoons`):

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m compileall scripts
python -m unittest discover -s tests -p 'test_*.py'
```

Optional local generation/render check (requires `ffmpeg` installed):

```bash
mkdir -p out
python scripts/generate_topic.py --output out/topic.txt
python scripts/generate_script.py --topic-file out/topic.txt --output out/script.txt
python scripts/render_video.py --script-file out/script.txt --out out/video.mp4
python scripts/render_short.py --script-file out/script.txt --out out/short.mp4
```

## Manual workflow testing without credentials

Use **Run workflow** with `publish=false`.

That validates generation/rendering/artifact upload without requiring YouTube secrets.
