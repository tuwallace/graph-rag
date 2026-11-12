I built a graph RAG over 500 AI interviews, entirely on my laptop, and spent most of the time checking it.

What held up: on count and comparison questions, plain vector search got 0 of 17 right and the graph got 13.

What didn't: a looser prompt meant to raise recall produced new facts that were only 49% correct in a random sample. Filtering them and testing on a fresh sample brought that to 76%. A small model in ollmcp skipped the tool and invented quotes in 3 of 5 runs.

Every score is judged by a larger model, one run each, on 500 of 1,250 interviews.

#GraphRAG #LocalLLM #AIEngineering

Video: https://youtu.be/Ewr40PPcdpA
