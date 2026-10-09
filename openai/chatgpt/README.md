# Use in ChatGPT

There are two ways to use the same workflows. Availability depends on the ChatGPT surface and your
workspace settings; publishing a GitHub repository does not list a plugin in the public directory.

## Installed plugin or skill

The repository contains a portable plugin manifest and a local marketplace catalog. In the desktop
app, open the cloned repository as a project and use its local plugin source, where supported.
Select **YouTube Agent Pro** from the available plugins, then ask for the desired workflow.
In ChatGPT, `@` selects available plugins or skills. Codex CLI uses `$yt`, `$yt-script`, etc.

For a ChatGPT workspace that supports Plugin Creator, provide the instructions below and the
generated workflow file as reference material, then use the workspace's creation and testing flow.
That creates a workspace plugin separately; this repository does not automatically deploy it.
See [OpenAI's plugin creation guide](https://learn.chatgpt.com/docs/build-plugins).

## Portable prompt and files

This works without installing a plugin, provided your ChatGPT experience supports the required
files. Download the assets from the [latest release](https://github.com/ahmedsakri/youtube-agent-pro/releases/latest),
or run `python3 scripts/build_release.py` from its `openai/` directory (or an extracted plugin root).

1. Paste `ChatGPT-INSTRUCTIONS.md` into a conversation, or use it as project instructions where
   available.
2. Attach `ChatGPT-WORKFLOWS.md` and your transcript or analytics export. Attach your own `voice.md`
   if you have one. You can also paste one relevant workflow when file upload is unavailable.
3. For computed scores, attach `youtube-agent-pro-openai-chatgpt.zip` and use a mode that can execute
   Python and access/extract uploaded files. Keep the extracted `skills/` directories together.
   Otherwise ask for a qualitative review; uploading Markdown alone does not execute Python.
4. Ask for a concrete result, for example: "Use yt-shorts to propose three standalone clips from
   this transcript. Preserve source timecodes and write the new opening lines in English."

The generated workflow file includes all 24 workflows, the shared operating guide, the voice
template and hook formulas. It is generated from the canonical skills so updates do not drift.

## Capabilities and limits

| Task | Required input or capability |
| --- | --- |
| Scripts, title options, descriptions, content plans | The topic or source material; no code tool required |
| Hook/title/concept scores, CSV analysis | Bundled files plus Python execution, or outputs from running them locally |
| Current trend research or policy checks | Web access and source verification |
| Reviewing actual footage or making images | Appropriate media tools supplied by the host |
| Uploading or changing a YouTube account | A separately available, authorized integration; none bundled |

No API key is required by this pack. ChatGPT plan limits and tool availability still apply.
