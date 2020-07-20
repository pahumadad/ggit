#!/usr/bin/env bash

ggit_completion() {
    prev_arg="${COMP_WORDS[COMP_CWORD-1]}";
    curr_arg="${COMP_WORDS[COMP_CWORD]}";

    if [[ "$prev_arg" == "ggit" ]]; then
        COMPREPLY=($(compgen -W "add commit diff push restore status" "${curr_arg//-/\\\-}"))
    fi
}

complete -F ggit_completion ggit
