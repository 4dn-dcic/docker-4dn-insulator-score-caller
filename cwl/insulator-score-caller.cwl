#!/usr/bin/env cwl-runner 

class: CommandLineTool

cwlVersion: v1.0

requirements:
- class: DockerRequirement
  dockerPull: "4dndcic/4dn-insulator-score-caller:v6.6"

- class: "InlineJavascriptRequirement"

inputs:
  mcoolfile:
    type: File
    inputBinding:
      position: 1
  outdir:
    type: string
    inputBinding:
      position: 2
    default: "."
    
outputs:
  bwfile:
    type: File
    outputBinding:
      glob: "$(inputs.outdir + '/' + '*.bw')"
      
baseCommand: ["run-insulator-score-caller.sh"]
