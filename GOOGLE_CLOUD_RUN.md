# Deploy Hangman to Google Cloud Run

This keeps `app.py` and `storage.py` unchanged. The Cloud Run entrypoint points the existing JSON storage at a writable Cloud Storage bucket mount.

## Before deploying

- Install the Google Cloud CLI and sign in with `gcloud init`.
- Select or create a Google Cloud project, enable billing, and enable the Cloud Run, Cloud Build, and Artifact Registry APIs.
- Review Cloud Run and Cloud Storage pricing. Google Cloud may charge for resources even when the service is not being actively used.
- The service is public after the final step. The uploaded `data.json`, team details, and game history can be viewed or changed by anyone using the game.
- The game currently has one shared `data.json` and one active round for all visitors; it does not give each visitor a separate game.

## Prepare persistent data

Choose a globally unique bucket name and create a bucket in the same region as the service:

```powershell
gcloud storage buckets create gs://YOUR_UNIQUE_BUCKET --location=asia-southeast1 --uniform-bucket-level-access
gcloud storage cp data.json gs://YOUR_UNIQUE_BUCKET/data.json
```

The second command copies the current game history. Skip it only if you intentionally want to start with an empty history.

## Deploy privately first

From the project folder, deploy the source without making it public yet:

```powershell
gcloud run deploy hangman --source . --region asia-southeast1 --no-allow-unauthenticated --max 1 --concurrency 1
```

If prompted to enable the Cloud Run, Cloud Build, or Artifact Registry APIs, approve the prompts. The `Procfile` starts Gunicorn using Cloud Run's `PORT`.

## Attach the data bucket

In Google Cloud Console, open **Cloud Run → hangman → Edit and deploy new revision**. Under **Volumes**:

1. Add a **Cloud Storage bucket** volume and select `YOUR_UNIQUE_BUCKET`.
2. Set its mount path to `/mnt/game-data` and leave it writable.
3. Under **Variables & Secrets**, add `GAME_DATA_DIR` with value `/mnt/game-data`.
4. Deploy the revision.

Grant the service's runtime service account the **Storage Object User** (`roles/storage.objectUser`) role on the bucket. Without this permission, the game cannot read or save `data.json`.

## Make it public

Only after the bucket is mounted and the private service responds successfully, allow public requests:

```powershell
gcloud run services add-iam-policy-binding hangman --region asia-southeast1 --member=allUsers --role=roles/run.invoker
```

Get the public URL with:

```powershell
gcloud run services describe hangman --region asia-southeast1 --format="value(status.url)"
```

Append `/page1` to that URL to open the game. Google Search may take additional time to index a newly published URL; the direct Cloud Run URL works first.

## Important limitation

Cloud Storage volume mounts do not provide file locking. This deployment limits the service to one instance and one concurrent request to reduce write races, but every visitor still shares the same active game and history. For separate games per player, the application would need a per-player data model and session handling before public launch.