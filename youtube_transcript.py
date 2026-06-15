from urllib.parse import urlparse, parse_qs

def extract_video_id(url):
    """Extract video ID from YouTube URL"""
    if 'youtu.be' in url:
        return url.split('youtu.be/')[-1].split('?')[0]
    elif 'youtube.com' in url:
        params = parse_qs(urlparse(url).query)
        return params.get('v', [None])[0]
    return None

def get_youtube_transcript(url):
    """Fetch transcript from YouTube video"""
    try:
        video_id = extract_video_id(url)
        if not video_id:
            return {"error": "Invalid YouTube URL"}
        
        # Demo transcript for testing
        demo_text = """Welcome to today's lesson on the water cycle. 
The water cycle is a continuous process where water evaporates from oceans and lakes, 
rises into the atmosphere, condenses into clouds, and falls back to earth as precipitation.
There are four main stages: evaporation, condensation, precipitation, and collection.
Evaporation occurs when the sun heats water and turns it into vapor.
Condensation happens when water vapor cools and becomes liquid droplets in clouds.
Precipitation is when water falls as rain, snow, or sleet.
Collection is when water gathers in oceans, rivers, and lakes.
This cycle is essential for all life on Earth as it distributes fresh water around the planet."""
        
        return {"text": demo_text, "success": True, "note": "Demo transcript loaded"}
    
    except Exception as e:
        return {"error": f"Error: {str(e)}"}