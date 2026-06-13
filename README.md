# Scripts

A simple home for personal Python scripts.

## Purpose

This repository is just a place for my scripts to live, be used, and updated over time. It will be fun to watch this repo grow and improve over the next few years. If you have a script you would like to add - feel free to make a pull-request or just clone the repo and add your own.

## Run a Script

From the python directory:

```bash
python script_name.py
```

## If you are feeling fancy

In your .bashrc
```bash
shopt -s nullglob
scripts=(path/to/scripts/python/*.py)
shopt -u nullglob

if ! test -d "$HOME/.local/bin"; then
        mkdir -p $HOME/.local/bin
fi

for i in "${scripts[@]}"; do
        chmod +x "$i"
        ln -sf "$i" "$HOME/.local/bin/$(basename "$i" .py)"
done

export PATH="$HOME/.local/bin:$PATH"
```

Or - In your .zshrc

```bash
# Python scripts - make sure to add the end '*.py(.N)'
scripts=(/path/to/scripts/*.py(.N))

# Check if .local/bin exists - if not then make one
if ! test -d "$HOME/.local/bin"; then
	mkdir -p $HOME/.local/bin
fi

# Link scripts
for i in $scripts; do
	chmod +x $i
	ln -sf "$i" "$HOME/.local/bin/${${i:t}%.py}"
done

# Export path 
export PATH="$HOME/.local/bin:$PATH"
```

Then run from anywhere in your terminal:
    - mkproj hello_world -r
    - cmp_sha hello.txt -c 'hash-to-compare'

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).