import boto3
import logging
import os
from datetime import datetime, timedelta, timezone

log = logging.getLogger()
log.setLevel(logging.INFO)

ec2 = boto3.client("ec2")


RETENTION_DAYS = int(os.getenv("RETENTION_DAYS", "365"))
DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"
REQUIRED_TAG = os.getenv("REQUIRED_TAG", "AutoCleanup")


def lambda_handler(event, context):
    cutoff = datetime.now(timezone.utc) - timedelta(days=RETENTION_DAYS)

    log.info(f"starting snapshot cleanup | retention={RETENTION_DAYS} days | dry_run={DRY_RUN}")

    try:
        paginator = ec2.get_paginator("describe_snapshots")

        for page in paginator.paginate(OwnerIds=["self"]):
            for snap in page.get("Snapshots", []):
                snapshot_id = snap["SnapshotId"]
                start_time = snap["StartTime"]

                if start_time >= cutoff:
                    continue

                
                tags = {t["Key"]: t["Value"] for t in snap.get("Tags", [])}

                if REQUIRED_TAG and tags.get(REQUIRED_TAG) != "true":
                    log.info(f"skipping {snapshot_id} (missing required tag)")
                    continue

                # delete 
                if DRY_RUN:
                    log.info(f"[dry-run] would delete snapshot {snapshot_id}")
                    continue

                try:
                    log.info(f"deleting snapshot {snapshot_id}")
                    ec2.delete_snapshot(SnapshotId=snapshot_id)
                except Exception as e:
                    log.error(f"failed to delete {snapshot_id}: {e}")

    except Exception as e:
        log.error(f"error during snapshot cleanup: {e}")
        raise

    return {"status": "done"}