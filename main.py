import gradio as gr
from app.scraper import TrendScraper
from app.llm import TrendsToStory  # Import the TrendsToStory class

# Initialize TrendsToStory instance
story_generator = TrendsToStory()

# Define valid sources and themes
VALID_SOURCES = {
    "Google News": "news",
    "Youtube": "youtube",
    "Google Trends": "google"
}

VALID_THEMES = [
    "Comedy",
    "Tragedy",
    "Sarcasm",
    "Drama",
    "Adventure",
    "Horror",
    "Romance",
    "Mystery"
]

async def fetch_trends(trend_source):
    # Validate trend source
    if not trend_source:
        return "Please select a trend source."
    
    if trend_source not in VALID_SOURCES:
        return f"Invalid trend source. Please select from: {', '.join(VALID_SOURCES.keys())}"
    
    # Fetch trending topics based on selected source
    scraper = TrendScraper()
    source_key = VALID_SOURCES[trend_source]
    
    try:
        trends = await scraper.get_trends(source_key)
        if not trends:
            return "No trending topics found for the selected source."
        return trends
    except Exception as e:
        return f"Error fetching trends: {str(e)}"

async def generate_story_interface(trends_text, theme):
    # Validate theme
    if not theme:
        return "Please select a theme."
    
    if theme not in VALID_THEMES:
        return f"Invalid theme. Please select from: {', '.join(VALID_THEMES)}"
    
    # Validate trends text
    if not trends_text or trends_text.startswith("Error") or trends_text.startswith("Please"):
        return "Please fetch valid trends first."
    
    try:
        # Generate a story from the selected trend and theme using the LLM
        story = await story_generator.generate_story(trends=trends_text, theme=theme)
        
        if not story:
            return "Error generating the story. Please try again."
        return story
    except Exception as e:
        return f"Error generating story: {str(e)}"

def create_gradio_interface():
    # Gradio interface setup with custom layout
    with gr.Blocks() as interface:
        with gr.Column():  # Column for entire layout
            # Top half (1/3 for inputs and button, 2/3 for trends)
            with gr.Row(equal_height=True):
                with gr.Column(scale=1):  # Input fields and generate button (1/3 of the top)
                    trend_dropdown = gr.Dropdown(
                        label="Select Trend Source",
                        choices=list(VALID_SOURCES.keys()),
                        value=None,  # No default value
                        allow_custom_value=False
                    )
                    theme_dropdown = gr.Dropdown(
                        label="Select Theme",
                        choices=VALID_THEMES,
                        value=None,  # No default value
                        allow_custom_value=False
                    )
                    generate_button = gr.Button("Generate Story")
                    
                    # add an empty textbox
                    gr.Textbox(visible=False)
                
                with gr.Column(scale=2):  # Scraped trends (2/3 of the top)
                    trends_output = gr.Textbox(
                        label="Trending Topics",
                        placeholder="Select a trend source to fetch trending topics...",
                        interactive=False,
                        lines=8,
                        max_lines=8
                    )
            
            # Bottom half (Story output)
            story_output = gr.Textbox(
                label="Generated Story",
                placeholder="Select a theme and click 'Generate Story' to create a story...",
                interactive=False
            )

        # Fetch trends when trend source changes
        trend_dropdown.change(fetch_trends, inputs=trend_dropdown, outputs=trends_output)
        
        # When the button is clicked, generate the story using the fetched trends and selected theme
        generate_button.click(generate_story_interface, inputs=[trends_output, theme_dropdown], outputs=story_output)

    return interface

if __name__ == "__main__":
    interface = create_gradio_interface()
    interface.launch(server_name="0.0.0.0", server_port=8001)
