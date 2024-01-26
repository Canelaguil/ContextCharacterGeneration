# ContextCharacterGeneration
## Premise
The premise of this project is to apply systemic storytelling to character
generation on a large scale. While the seed of this character generator may be completely
random, after a few generations the people still alive truly are the causal product of everything
that happened before the simulation stopped. The causality problem problem is thus addressed
by having most data be the result of actual causality, and leaving the rest up to be interpreted
through apophenia. The oatmeal problem is addressed in the following ways:

1. The modeled events are abstract representations of universal human themes that any character can experience in any fiction: family, friendship, love, grief, trauma, etc.
2. Events gain meaning through their context, and because every character has a different context (a causal result of their history), this results in many stories with few actual variations in events.2
3. If developers do wish to use specific event descriptions, the abstract versions can be fleshed out algorithmically or manually in post-processing. It is easier to take causality into account with this project as input over randomly generated biographies, because the provided context can serve as natural constraints to the information selected.

Characters take decisions motivated by who they are, who other are, chance and for authored
reasons3. Story arcs are experienced by having different systems interact with each other. Ex-
amples of this are the death of a parent causing the other parent to have to work (leaving the
child neglected) or grief causing a personality change. These arcs are often not set in stone but
subject to chance: not every death will cause a personality change, and the actual change is
chosen from a normal distribution. Apophenia is meant to be triggered by these (technically)
random events as well. The following reasoning might result from generated events: ”she was
so close to her sibling that their death affected her way more than her mother’s death! Must be
because she was neglected as a child and that sibling was her actual caretaker”. Even though
the stronger reaction was a coincidence cause by different numbers being chosen from the normal
distribution, and the neglect not actually influencing any chance.
4.2 The framework
Figure 4.1 shows the set-up of the model. It is designed to be modular: all communication
between agents happens through the community model, and likewise all support classes of the
agents are addressed through their respective agents. As a result, all support classes can easily
be replaced by treating them as APIs.
In addition to that, existing systems within the model can be adjusted to a project’s need.
Take the faction system for example: ”factions” can be used to represent:

1. religious factions
2. medieval guilds
3. political leanings
4. fantasy races

This leaves the developer with the following personalization options:
1. Provide project-specific input files (like names and the city set-up)
2. Adjusting the config file with project-specific settings
3. Adjusting distributions in the code to the developer’s preference
4. Exchanging support classes for other classes
5. Interpreting the output as desired during post-processing


## Runing the code
```
 # run simulation with input specified in /input/
python generation.py

# turn output into biographies easely read by humans through basic post-processing
python output/post_processing.py

# view a random or specific file / processed biography 
python view_output.py

# generate analysis graphs in the output folder
python output/output_analysis.py [experiment name]
```



