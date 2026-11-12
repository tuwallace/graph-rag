UPLOAD CHECKLIST (nothing here has been uploaded; that is up to you)
1. Upload graph-rag-video.mp4. Start as PRIVATE or UNLISTED and watch it fully, with headphones, before making it public.
2. Thumbnail: thumbnail.png (1280x720). Captions: captions.srt (English). Tags: tags.txt. Description: description.txt (chapters are generated from the real clip timings).
3. Under "Altered content" answer YES: the narration is a synthetic voice.
4. Listen for mispronounced words (A I, rag, Neo for J, ollmcp, nimble, GitHub). If any are wrong: edit PRONOUNCE in narration/build_narration.py,
   re-run it, re-render the clips (npm run render:all in docs/video/anim), then re-run docs/video/finalize.py.
5. Check the dataset terms (the card is inconsistent; the project owner decided to treat it as MIT, attribution to Anthropic is kept) and the Remotion and Kokoro licences.
