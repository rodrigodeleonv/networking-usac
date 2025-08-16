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