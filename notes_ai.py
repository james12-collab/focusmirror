def process_notes(text, mode):
    """
    Process notes in 3 modes (demo version)
    """
    
    if mode == "basic":
        # Demo: Extract first 3 sentences as bullet points
        sentences = text.split('.')[:3]
        result = "\n".join([f"• {s.strip()}" for s in sentences if s.strip()])
        return result or "• No content to process"
    
    elif mode == "summarized":
        # Demo: First sentence
        first_sentence = text.split('.')[0].strip()
        return first_sentence if first_sentence else "No content to summarize"
    
    elif mode == "detailed":
        # Demo: Show word count and key info
        words = text.split()
        sentences = text.split('.')
        result = f"""ANALYSIS:
Content Length: {len(words)} words, {len(sentences)} sentences

Main Topic:
{text[:200]}...

Key Insights:
- This text covers important concepts
- Multiple ideas are presented
- Suitable for detailed study

Note: Using demo mode. Upgrade your Anthropic API credits for AI-powered summaries."""
        return result
    
    else:
        return "Invalid mode"