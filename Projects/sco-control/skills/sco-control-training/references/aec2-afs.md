# AEC2 And AFS

## AEC2 Queries

```bash
sco aec2 clusters list
sco aec2 clusters describe --name "$AEC2"
sco aec2 clusters list-workerspec --workspace-name "$WORKSPACE" --aec2-name "$AEC2"
sco aec2 clusters usage --help
```

If `sco aec2 clusters list` returns `SUBSCRIPTION_NAME_REQUIRED`, the profile lacks subscription context. Use the user's configured profile or pass explicit global `--subscription` and `--resource-group`; do not invent or persist these values in the skill.

Common worker spec examples seen in templates. Treat these as examples only; query the target cluster for the authoritative list:

```text
n6ls.iu.i40.1.22c240g
n6ls.iu.i40.2.44c480g
n6ls.iu.i40.4.88c960g
n6ls.iu.i40.8.176c1920g
n6ls.iu.i40.1.8c128g
n6ls.iu.i40.1.4c64g
n6ls.iu.i40.2.8c128g
n6ls.iu.i40.2.16c256g
n6ls.iu.i40.4.16c256g
n6ls.iu.i40.4.32c512g
n6ls.iu.i40.8.32c512g
n6ls.iu.i40.8.64c1024g
n6ls.iu.i40.0.2c4g
n6ls.iu.i40.0.2c8g
n6ls.iu.i40.0.64c256g
n6ls.iu.i40.0.16c64g
n6ls.iu.i40.0.8c32g
n6ls.iu.i40.0.4c16g
```

Less common cluster operations:

```bash
sco aec2 clusters add-node --aec2-name "$AEC2" --acn-name "$ACN"
sco aec2 clusters delete-node --aec2-name "$AEC2" --acn-name "$ACN"
sco aec2 clusters disable-node --aec2-name "$AEC2" --acn-name "$ACN"
sco aec2 clusters enable-node --aec2-name "$AEC2" --acn-name "$ACN"
```

Only create/delete clusters when explicitly requested:

```bash
sco aec2 clusters create --display_name "$DISPLAY_NAME"
sco aec2 clusters delete --name "$AEC2"
```

## AFS Queries

```bash
sco afs volume list
sco afs volume list -i "$VOLUME_ID"
sco afs volume ls -i "$VOLUME_ID" -d /
sco afs volume ls -i "$VOLUME_ID" -d /project
```

## AFS Quota

```bash
sco afs dir-quota list -i "$VOLUME_ID"
sco afs dir-quota list -i "$VOLUME_ID" -d /project
sco afs dir-quota create -i "$VOLUME_ID" -d /project --files 100000 --capacity 1024
sco afs dir-quota update -i "$VOLUME_ID" -d /project --files 100000 --capacity 2048
sco afs dir-quota delete -i "$VOLUME_ID" -d /project
```

## AFS ACL

```bash
sco afs dir-acl list -i "$VOLUME_ID"
sco afs dir-acl list -i "$VOLUME_ID" -d /project
sco --profile "$OWNER_PROFILE" afs dir-acl create -i "$VOLUME_ID" -d "$INPUT_DIR" -p r -u "$READER_USER_ID"
sco --profile "$OWNER_PROFILE" afs dir-acl create -i "$VOLUME_ID" -d "$INPUT_DIR" -p r -g "$READER_GROUP_ID"
sco --profile "$OWNER_PROFILE" afs dir-acl create -i "$VOLUME_ID" -d "$OUTPUT_DIR" -p rw -g "$WRITER_GROUP_ID"
```

Use paths inside the AFS volume for `INPUT_DIR` and `OUTPUT_DIR`. Keep run outputs writable by their owner and grant write access to a named group if that group also manages the outputs. Check the workspace's AFS identity setting when relying on per-user permissions. When identity recognition is enabled, workload file operations are checked as the submitter. With it disabled, workloads access mounted AFS as root. Verify effective permissions under the recipient's own ACP identity. [SenseCore workspace settings](https://www.sensecore.cn/help/docs/cloud-foundation/compute/aec2/userGuide/workspaceManage)

ACP storage mount format is `volume_id[:subdir]:container_path`, for example `<afs-volume-id>:/data`.

CCI YAML mount uses `type: PV_AFS`, `id`, `mount_path`, optional `subdir`, `zone`, and `display_name`.
