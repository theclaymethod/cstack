---- MODULE Tutor ----
EXTENDS TLC
VARIABLES phase, paused, scope, approved, checked, independent
v == <<phase, paused, scope, approved, checked, independent>>
Init == /\ phase = "Choose workflow" /\ paused = FALSE /\ scope = "unset"
        /\ approved = FALSE /\ checked = FALSE /\ independent = FALSE
Select == /\ phase = "Choose workflow" /\ scope' \in {"empty","existing"}
          /\ phase' = "Review scenario" /\ UNCHANGED <<approved,checked,independent>>
Approve == /\ phase = "Review scenario" /\ approved' = TRUE /\ phase' = "Run case"
           /\ UNCHANGED <<scope,checked,independent>>
Run == /\ phase = "Run case" /\ approved /\ checked' = TRUE /\ phase' = "Read fresh trace"
       /\ UNCHANGED <<scope,approved,independent>>
Help == /\ phase = "Read fresh trace" /\ phase' = "Discuss attempt"
        /\ UNCHANGED <<scope,approved,checked,independent>>
Fresh == /\ phase = "Discuss attempt" /\ phase' = "Read fresh trace"
         /\ UNCHANGED <<scope,approved,checked,independent>>
Explain == /\ phase = "Read fresh trace" /\ checked /\ independent' = TRUE
           /\ phase' = "Choose next skill" /\ UNCHANGED <<scope,approved,checked>>
Choose == /\ phase = "Choose next skill" /\ independent /\ phase' = "Finished"
          /\ UNCHANGED <<scope,approved,checked,independent>>
Coach == /\ phase = "Choose next skill" /\ phase' = "Discuss workflow"
         /\ UNCHANGED <<scope,approved,checked,independent>>
Retry == /\ phase = "Discuss workflow" /\ phase' = "Choose next skill"
         /\ UNCHANGED <<scope,approved,checked,independent>>
Active == phase \notin {"Finished","Partial"}
TimeUp == /\ Active /\ phase' = "Partial" /\ UNCHANGED <<scope,approved,checked,independent>>
Pause == /\ Active /\ paused' = ~paused /\ UNCHANGED <<phase,scope,approved,checked,independent>>
Done == /\ ~Active /\ UNCHANGED v
Next == (~paused /\ UNCHANGED paused /\ (Select \/ Approve \/ Run \/ Help \/ Fresh \/ Explain \/ Choose \/ Coach \/ Retry \/ TimeUp)) \/ Pause \/ Done
ApprovalFirst == checked => approved
SupportedFinish == phase = "Finished" => approved /\ checked /\ independent
WorkflowAfterEval == phase \in {"Choose next skill","Discuss workflow","Finished"} => independent
====
