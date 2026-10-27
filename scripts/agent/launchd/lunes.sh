#!/bin/zsh
# Lunes: Medidor -> Analista -> Estratega, secuencial (orden garantizado)
S=/Users/reginaelizondo/kinedu-landing-agent/schedule/run_routine.sh
"$S" landing-lunes-medidor
"$S" landing-lunes-analista
"$S" landing-lunes-estratega
