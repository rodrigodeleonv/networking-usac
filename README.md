# Networking USAC

## Software requirements

- Linux based distro
- Python 3.12+
- UV
- Git

```bash
# Install UV

# https://docs.astral.sh/uv/getting-started/installation/
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install specific Python version
uv python install 3.13

# Optional (Shell autocompletion)
echo 'eval "$(uv generate-shell-completion bash)"' >> ~/.bashrc
echo 'eval "$(uvx --generate-shell-completion bash)"' >> ~/.bashrc

uv init
uv run which python
```

## WSL2

Mirrored mode networking: <https://learn.microsoft.com/en-us/windows/wsl/networking#mirrored-mode-networking>

## References

Asyncio server implementations

- <https://poehlmann.dev/post/async-python-server/>
- <https://superfastpython.com/asyncio-server/>
