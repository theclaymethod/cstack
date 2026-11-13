"""Acceptance, adversarial, and coverage controls for the decision grader."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from evaluate import HERE, evaluate, grade, load_cases, parse_answer, prepare


class DecisionEvalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = load_cases()
        cls.gold = json.loads((HERE / 'expected.json').read_text())
        cls.answers = [{'case_id': c['id'], **{k: cls.gold[c['id']][k] for k in ['actions','archive','promote','judge']}} for c in cls.cases]

    def test_legitimate_controls_and_exploratory_alternative(self):
        self.assertEqual(evaluate(self.answers)['counts'], {'PASS':16,'FAIL':0,'ERROR':0})
        answers = copy.deepcopy(self.answers)
        row = next(a for a in answers if a['case_id']=='rank-reversal')
        row['archive'] = ['A']
        self.assertEqual(evaluate(answers)['counts']['PASS'],16)
        next(a for a in answers if a['case_id']=='judge-version-switch')['archive'] = ['A']
        self.assertEqual(evaluate(answers)['counts']['PASS'],16)
        case = next(c for c in self.cases if c['id']=='errors-not-success')
        answer = next(a for a in answers if a['case_id']==case['id'])
        answer['actions'].reverse()
        self.assertEqual(grade(case,self.gold[case['id']],answer),[])

    def test_every_bad_action_is_rejected_even_with_all_good_actions(self):
        rejected = 0
        for case, good in zip(self.cases,self.answers):
            for action in set(case['available_actions'])-set(good['actions']):
                bad = copy.deepcopy(good)
                bad['actions'].append(action)
                self.assertTrue(grade(case,self.gold[case['id']],bad),(case['id'],action))
                rejected += 1
        self.assertGreaterEqual(rejected,25)

    def test_required_actions_cannot_be_omitted(self):
        for case, good in zip(self.cases,self.answers):
            for action in good['actions']:
                bad = copy.deepcopy(good)
                bad['actions'].remove(action)
                self.assertTrue(grade(case,self.gold[case['id']],bad),(case['id'],action))

    def test_repair_must_precede_regrade(self):
        case = next(c for c in self.cases if c['id']=='missing-evidence')
        bad = copy.deepcopy(next(a for a in self.answers if a['case_id']==case['id']))
        bad['actions'].reverse()
        self.assertTrue(grade(case,self.gold[case['id']],bad))

    def test_premature_promotion_and_greedy_archive_fail(self):
        case = self.cases[0]
        bad = copy.deepcopy(self.answers[0])
        bad['promote'] = ['A']
        self.assertTrue(grade(case,self.gold[case['id']],bad))
        bad['promote'] = []
        bad['archive'] = ['A']
        self.assertTrue(grade(case,self.gold[case['id']],bad))

    def test_missing_duplicate_unknown_and_malformed_answers(self):
        self.assertEqual(evaluate(self.answers[:-1])['counts']['ERROR'],1)
        with self.assertRaises(ValueError):
            evaluate(self.answers+[self.answers[0]])
        with self.assertRaises(ValueError):
            evaluate([{'case_id':'invented'}])
        for field, value in [('actions',None),('archive',['A','A']),('promote',True),('judge',{'verdict':'PASS'})]:
            bad = copy.deepcopy(self.answers[0]); bad[field] = value
            self.assertTrue(grade(self.cases[0],self.gold[self.cases[0]['id']],bad))
        bad=copy.deepcopy(self.answers[0]);bad['override']='PASS'
        self.assertTrue(grade(self.cases[0],self.gold[self.cases[0]['id']],bad))

    def test_duplicate_json_fields_cannot_overwrite_bad_decisions(self):
        with self.assertRaises(ValueError):
            parse_answer('{"case_id":"reserve-exhausted","actions":["start_one_more_branch"],"actions":["stop_search"]}')

    def test_answer_keys_and_label_metadata_stay_out_of_prepared_inputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'prompts';prepare(out)
            self.assertEqual(len(list(out.glob('*.txt'))),16)
            text=(out/'generous-judge.txt').read_text()
            self.assertNotIn('alternative_archives',text)
            self.assertNotIn('expected.json',text)
            self.assertNotIn('"family":',text)
            situation=json.loads(text.split('## Situation\n')[-1])
            self.assertIn('J-easy',situation['judge_ids'])
            self.assertIn('J-strict',situation['judge_ids'])

    def test_cli_reports_actual_denominator_and_exits_nonzero_for_incomplete_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'answers.jsonl'
            path.write_text('\n'.join(json.dumps(a) for a in self.answers))
            good=subprocess.run([sys.executable,str(HERE/'evaluate.py'),'--answers',str(path)],capture_output=True,text=True)
            self.assertEqual(good.returncode,0,good.stderr)
            self.assertEqual(json.loads(good.stdout)['total'],16)
            path.write_text(json.dumps(self.answers[0])+'\n')
            partial=subprocess.run([sys.executable,str(HERE/'evaluate.py'),'--answers',str(path)],capture_output=True,text=True)
            self.assertEqual(partial.returncode,1)
            self.assertEqual(json.loads(partial.stdout)['counts']['ERROR'],15)


if __name__=='__main__':
    unittest.main()
