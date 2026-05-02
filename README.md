# tray-telegram-backup
![Utility icon (Stable Diffusion)](icon.png)

> Send yourself backups in a chat with Telegram bot via the system tray. The utility is written in Python and Bash, and works **only** on Linux.

## Installation
> The instructions for your distro may be different!

1. Install packages for viewing logs:
   ```sh
   $ sudo apt install kitty lnav
   ```
   You can change terminal emulator and viewer in `main.py`. In this case, skip this step.

2. Clone this repo. Go to its directory.

3. Create `.env` file. Add the bot TOKEN and your ID to it as follows:
   ```
   TOKEN=
   CHAT_ID=
   ```

4. Create backup scripts in `backup_scripts` folder. Use this template:
   ```bash
   #!/bin/bash
   7z a $1 ~/your/dir -xr!exclude_folder -xr!.*
   ```
   These scripts are actually commands for creating 7-Zip archives. My utility will scan the folder with them itself. **Don't forget to make scripts executable!** (`chmod +x script.sh`)

4. Create a virtual environment and install dependencies:
   ```sh
   $ python3 -m venv .venv
   $ source ./.venv/bin/activate
   $ pip install -r requirements.txt
   # or requirements_unversioned.txt
   ```

5. Run `run.sh`. You can add it to system startup (e.g., through KDE settings).

## Notes for me
Lint and format `main.py`:
```sh
$ make ruff
```

Create a file with unversioned dependencies:
```sh
$ pip freeze | sed 's/==.*$//' > requirements_unversioned.txt
```
