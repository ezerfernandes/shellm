#!/bin/zsh

# This ZSH plugin reads the text from the current buffer
# and uses a Python script to complete the text.

create_completion() {
    # Get the text typed until now.
    text=${BUFFER}
    completion=$(echo -n "$text" | $SHELLM_CLI_PATH/src/shellm.py)
    # Add completion to the current buffer.
    BUFFER="${completion}"
    # Put the cursor at the end of the line.
    CURSOR=${#BUFFER}
}

# Bind the create_completion function to a key.
zle -N create_completion

setopt interactivecomments
