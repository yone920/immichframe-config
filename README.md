# ImmichFrame Config

A simple web UI for managing [ImmichFrame](https://github.com/immichFrame/ImmichFrame) settings. Edit display options, manage albums, and customize appearance without touching `Settings.json` by hand.

## Features

- Add/remove Immich albums from a dropdown
- Configure display, appearance, and weather settings
- Mobile-friendly dark theme
- No auth required (designed for local network)

## Setup

This app needs access to ImmichFrame's `Settings.json` file. Both containers should share the same settings directory via a volume mount so that changes made here are picked up by ImmichFrame.

### 1. Create your albums.json

Create an `albums.json` file in your ImmichFrame settings directory with your album names and IDs:

```json
{
  "My Album Name": "<album-id>",
  "Another Album": "<album-id>"
}
```

You can find album IDs in the URL when viewing an album in your Immich web UI.

### 2. Create a docker-compose.yml

```yaml
services:
  immichframe-config:
    image: ghcr.io/yone920/immichframe-config:latest
    container_name: immichframe-config
    ports:
      - "5050:5000"
    volumes:
      - /path/to/your/immichframe:/config
    restart: unless-stopped
```

The volume should point to the same directory that contains your ImmichFrame `Settings.json`.

### 3. Run

```bash
docker compose up -d
```

Access the UI at `http://your-server-ip:5050`.

### Building from source

If you prefer to build locally instead of using the pre-built image:

```bash
git clone https://github.com/yone920/immichframe-config.git
cd immichframe-config
docker compose up -d --build
```

## How It Works

- **Albums** are saved immediately when you click Add or Remove.
- **General settings** (display, appearance, weather) are saved when you click Save Settings.
- The app reads and writes directly to `Settings.json` on disk. All fields not shown in the UI are preserved.

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/settings` | Get current settings |
| `POST` | `/api/settings` | Update general settings |
| `POST` | `/api/albums/add` | Add an album by ID |
| `POST` | `/api/albums/remove` | Remove an album by ID |

## License

MIT
