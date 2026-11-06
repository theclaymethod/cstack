---------------- MODULE CrossExamine ----------------
EXTENDS Naturals
CONSTANTS IndependentReview, EvidenceBased, PreserveValid, PreserveIntent, Repairs

Good == {"answer-A", "answer-B"}
Bad == "unsupported"
InitialPolicy == Good \cup {Bad}
Roles == {"independent", "attacker", "defender", "optimizer"}
Kinds == {"Sound", "RejectAll", "ExactMatch", "RewriteIntent", "FabricateEvidence"}
Phases == {"Frame", "Attack", "ReplayAttack", "ReviewFinding", "Defend",
           "ReplayRepair", "ReviewRepair", "Record", "Done"}
VARIABLES phase, policy, intent, candidate, observedCredit, replayed,
          reviewer, authorized, finding, repairKind, repairReplayed, repair,
          ledger, lesson
vars == <<phase, policy, intent, candidate, observedCredit, replayed,
          reviewer, authorized, finding, repairKind, repairReplayed, repair,
          ledger, lesson>>

Init == /\ phase = "Frame" /\ policy = InitialPolicy /\ intent = Good
        /\ candidate = Bad /\ observedCredit = FALSE /\ replayed = FALSE
        /\ reviewer \in Roles /\ authorized \in BOOLEAN
        /\ finding = "UNREVIEWED" /\ repairKind = "None"
        /\ repairReplayed = FALSE /\ repair = "UNREVIEWED"
        /\ ledger = FALSE /\ lesson = FALSE

Independent == ~IndependentReview \/ reviewer = "independent"
ActualGap == observedCredit # (candidate \in Good)
FindingHolds == Independent /\ (IF EvidenceBased THEN replayed /\ ActualGap ELSE TRUE)
RepairHolds == Independent
               /\ (IF EvidenceBased THEN repairReplayed /\ Bad \notin policy ELSE TRUE)
               /\ (IF PreserveValid THEN Good \subseteq policy ELSE TRUE)
               /\ (IF PreserveIntent THEN intent = Good ELSE TRUE)

Frame == /\ phase = "Frame" /\ phase' = "Attack"
         /\ UNCHANGED <<policy, intent, candidate, observedCredit, replayed, reviewer,
                        authorized, finding, repairKind, repairReplayed, repair, ledger, lesson>>
\* Every attacker claims success; trusted replay, not that claim, decides acceptance.
Attack == /\ phase = "Attack" /\ phase' = "ReplayAttack"
          /\ candidate' \in InitialPolicy
          /\ UNCHANGED <<policy, intent, observedCredit, replayed, reviewer, authorized,
                         finding, repairKind, repairReplayed, repair, ledger, lesson>>
ReplayAttack == /\ phase = "ReplayAttack" /\ phase' = "ReviewFinding"
                /\ observedCredit' = (candidate \in policy) /\ replayed' = TRUE
                /\ UNCHANGED <<policy, intent, candidate, reviewer, authorized, finding,
                               repairKind, repairReplayed, repair, ledger, lesson>>
ReviewFinding == /\ phase = "ReviewFinding"
                 /\ finding' = IF ~Independent THEN "UNREVIEWED"
                                ELSE IF FindingHolds THEN "CONFIRMED" ELSE "NOT_CONFIRMED"
                 /\ phase' = IF FindingHolds /\ authorized THEN "Defend" ELSE "Record"
                 /\ UNCHANGED <<policy, intent, candidate, observedCredit, replayed, reviewer,
                                authorized, repairKind, repairReplayed, repair, ledger, lesson>>
\* The defender may propose an invalid repair. Rejection, not a well-behaved defender,
\* must protect the audit's acceptance decision.
Defend == /\ phase = "Defend" /\ phase' = "ReplayRepair" /\ repairKind' \in Repairs
          /\ policy' = CASE repairKind' = "RejectAll" -> {}
                         [] repairKind' = "ExactMatch" -> {"answer-A"}
                         [] repairKind' = "FabricateEvidence" -> InitialPolicy
                         [] OTHER -> Good
          /\ intent' = IF repairKind' = "RewriteIntent" THEN {"answer-A"} ELSE Good
          /\ UNCHANGED <<candidate, observedCredit, replayed, reviewer, authorized,
                         finding, repairReplayed, repair, ledger, lesson>>
\* Proposed artifact claims are all positive; collection preserves the actual policy.
ReplayRepair == /\ phase = "ReplayRepair" /\ phase' = "ReviewRepair"
                /\ repairReplayed' = TRUE
                /\ UNCHANGED <<policy, intent, candidate, observedCredit, replayed, reviewer,
                               authorized, finding, repairKind, repair, ledger, lesson>>
ReviewRepair == /\ phase = "ReviewRepair" /\ phase' = "Record"
                /\ repair' = IF ~Independent THEN "UNREVIEWED"
                               ELSE IF RepairHolds THEN "ACCEPTED" ELSE "REJECTED"
                /\ UNCHANGED <<policy, intent, candidate, observedCredit, replayed, reviewer,
                               authorized, finding, repairKind, repairReplayed, ledger, lesson>>
Record == /\ phase = "Record" /\ phase' = "Done" /\ ledger' = TRUE
          /\ lesson' = (finding = "CONFIRMED")
          /\ UNCHANGED <<policy, intent, candidate, observedCredit, replayed, reviewer,
                         authorized, finding, repairKind, repairReplayed, repair>>
Done == /\ phase = "Done" /\ UNCHANGED vars
Next == Frame \/ Attack \/ ReplayAttack \/ ReviewFinding \/ Defend
        \/ ReplayRepair \/ ReviewRepair \/ Record \/ Done
Spec == Init /\ [][Next]_vars /\ WF_vars(Next)

TypeOK == /\ phase \in Phases /\ policy \subseteq InitialPolicy /\ intent \subseteq Good
          /\ candidate \in InitialPolicy /\ reviewer \in Roles /\ repairKind \in Kinds \cup {"None"}
          /\ finding \in {"UNREVIEWED", "CONFIRMED", "NOT_CONFIRMED"}
          /\ repair \in {"UNREVIEWED", "ACCEPTED", "REJECTED"}
          /\ \A b \in {observedCredit, replayed, authorized, repairReplayed, ledger, lesson}: b \in BOOLEAN
ReviewIsIndependent == (finding = "CONFIRMED" \/ repair = "ACCEPTED") => reviewer = "independent"
FindingNeedsReplay == finding = "CONFIRMED" => replayed /\ ActualGap
RepairNeedsFinding == repair = "ACCEPTED" => finding = "CONFIRMED" /\ authorized
RepairNeedsObservedRejection == repair = "ACCEPTED" => repairReplayed /\ Bad \notin policy
ValidAlternativesRemain == repair = "ACCEPTED" => Good \subseteq policy
OriginalIntentPreserved == repair = "ACCEPTED" => intent = Good
EvidenceBeforeLessons == lesson => finding = "CONFIRMED"
ReportIsRecorded == phase = "Done" => ledger
EventuallyReported == <> (phase = "Done")
======================================================
