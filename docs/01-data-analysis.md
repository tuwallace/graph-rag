# 01. Data analysis: Anthropic Interviewer transcripts

Source: [Anthropic/AnthropicInterviewer](https://huggingface.co/datasets/Anthropic/AnthropicInterviewer) on Hugging Face. Measured on the downloaded CSVs by `spike/01_profile.py`
(the data itself is git-ignored under `data/raw/`; fetch it at setup).

**License and attribution.** The dataset card's front matter says `license: mit`, but its body says "Data released under CC-BY, code released under MIT". The two disagree.
Treat the data as **CC-BY** (the stricter reading): attribute Anthropic and link the dataset in the README. Participants "provided informed consent for public release of their raw interview transcripts" (card).

## Shape

| Split | Rows | File |
|---|---|---|
| `workforce` | 1,000 | `interview_transcripts/workforce_transcripts.csv` |
| `creatives` | 125 | `.../creatives_transcripts.csv` |
| `scientists` | 125 | `.../scientists_transcripts.csv` |

Columns: `transcript_id` (`work_NNNN`, `creativity_NNNN`, `science_NNNN`), `text`. No duplicate ids, no null text. Total about 11 MB.

| Measure | Value |
|---|---|
| Characters per transcript | min 4,837, median 8,674, mean 9,126, max 26,826 |
| Approx. tokens per transcript | about 2,300 mean (4 chars per token, rough) |
| Turns per transcript | min 15, median 23, max 55 |
| Speaker labels | `User` 14,495, `AI` 14,495, `Assistant` 1,250 (the opening turn); a handful of stray labels inside quoted text |
| Question/answer pairs | about 14,495 (one per `User` turn) |

## Structure

Every transcript is a fixed-guide interview of about 10 minutes: consent, "how does AI fit your workday", follow-ups, tasks done alone, triggers for using AI, interaction
style, social influence, a critical incident, skills, the future. So the segments have a **predictable discourse role**, which is useful for retrieval and typed classification.

## What a graph can add here

Relationships live in prose, not in columns: a participant's tasks, how they use AI for them, concerns, attitude, and the group they belong to. Unlike the helpdesk data,
LLM extraction is justified here, because nothing structured exists to load. The only structured fields are the split (group) and the id.

## Risks specific to this corpus

| Risk | Detail |
|---|---|
| Quality of local extraction | Measured in [spike 01](spike-01-extraction.md). |
| Vocabulary explosion | Free-text names rarely repeat: in the first spike, 92 of 98 distinct task names appeared once. Counting requires entity normalisation. |
| Prompt contamination | Examples in the extraction prompt were copied into results. See the spike. |
| No ground truth | There are no labels. Evaluation needs hand-labelled segments ([06](06-evaluation-and-roadmap.md)). |
| Personal data | Regex found no emails or phone numbers and 3 URLs in 1,250 transcripts. Regex cannot find names or employers; the check for those is not done. The dataset card describes no anonymisation. |
| Over-claiming | Interviews are conducted by an AI interviewer on a self-selected sample. Counts describe the sample, not workers in general. |
| Role-label oddities | The interviewer label changes from `Assistant` to `AI` after the opener, and quoted chat logs inside answers can contain stray labels. The turn parser must key on line-start labels and tolerate both. |

Earlier helpdesk-based analysis is archived in [archive/helpdesk](archive/helpdesk/README.md).
