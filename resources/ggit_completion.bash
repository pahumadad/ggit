#!/usr/bin/env bash

ggit_completion() {
    prev_arg="${COMP_WORDS[COMP_CWORD-1]}";
    curr_arg="${COMP_WORDS[COMP_CWORD]}";

    if [[ "$prev_arg" == "add"  || "$prev_arg" == "commit" ||\
          "$prev_arg" == "diff" || "$prev_arg" == "restore" ]]; then
        local sug=($(compgen -W "$(fd --hidden --no-ignore-vcs --type f)" "$curr_arg"))

        if [ "${#sug[@]}" == "1" ]; then
            local envi=${sug[0]/%\ */}
            COMPREPLY=("$envi")
        else
            COMPREPLY=("${sug[@]}")
        fi
    elif [[ "$prev_arg" == "ggit" ]]; then
        COMPREPLY=($(compgen -W "add commit diff push restore status" "${curr_arg//-/\\\-}"))
    fi
}

complete -F ggit_completion ggit
