# Dotie - Dotfiles linker

# Uses dotie_map.toml to link source config files to its target

# Commands
dotie install - installs all apps (excludes one mentioned in dotie_map.toml)
dotie install [app1] [app2] [app3] ...
dotie uninstall - uninstalls all apps (confirm first)
dotie uninstall [app1] [app2] ...
dotie generate [source_dir] [target_dir] - generates a dotie_map.toml template for the dirs

--dry-run - dont makes changes to files/links

# dotie_map.toml template

[app1]
    "app1 file path in dotfiles dir" - "target file to link"
    ..

[app2]
    ...
    ...

...
